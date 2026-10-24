#!/usr/bin/env python3
"""
S.T.A.L.K.E.R. 2 Heart of Chornobyl -> OGSR Complete Vegetation Bark Transpiler
================================================================================
Decodes UE5 Virtual Texture (.uexp + .ubulk) PBR bark sets (_D, _N, _RHA) extracted
from S.T.A.L.K.E.R. 2 via retoc, color-grades diffuse albedo to match X-Ray Zone
lighting/tone, bakes pixel-aligned X-Ray _bump.dds (Gloss + Normal ZYX) and
_bump#.dds (Parallax Height) DXT5 maps with full mipmaps, and preserves .thm files.
"""
import io
import os
import struct
import sys
from pathlib import Path
import numpy as np
from PIL import Image

sys.path.insert(0, "/home/ericparsley/Documents/GitHub/zoneforge/src")
from zoneforge.xdb import XdbArchive

ROOT = Path("/home/ericparsley/Documents/GitHub/ogsr-complete-merge")
S2_EXTRACT = Path("/tmp/s2_extract")
OUT_DIR = ROOT / "gamedata/textures/trees"


def _encode_dxt1_blocks(rgb_u8: np.ndarray) -> bytes:
    h, w, _ = rgb_u8.shape
    blocks = rgb_u8.reshape(h // 4, 4, w // 4, 4, 3).transpose(0, 2, 1, 3, 4).reshape(-1, 16, 3).astype(np.int32)
    luma = blocks[:, :, 0] * 77 + blocks[:, :, 1] * 150 + blocks[:, :, 2] * 29
    max_idx = np.argmax(luma, axis=1)
    min_idx = np.argmin(luma, axis=1)
    n_blk = blocks.shape[0]
    ar = np.arange(n_blk)
    c0 = blocks[ar, max_idx]
    c1 = blocks[ar, min_idx]

    def to565(c):
        return ((c[:, 0] >> 3) << 11) | ((c[:, 1] >> 2) << 5) | (c[:, 2] >> 3)

    w0 = to565(c0).astype(np.uint16)
    w1 = to565(c1).astype(np.uint16)
    swap = w0 < w1
    w0_s = np.where(swap, w1, w0)
    w1_s = np.where(swap, w0, w1)
    c0_s = np.where(swap[:, None], c1, c0)
    c1_s = np.where(swap[:, None], c0, c1)
    same = w0_s == w1_s

    p0 = c0_s
    p1 = c1_s
    p2 = (2 * c0_s + c1_s + 1) // 3
    p3 = (c0_s + 2 * c1_s + 1) // 3
    pal = np.stack([p0, p1, p2, p3], axis=1)
    diff = blocks[:, :, None, :] - pal[:, None, :, :]
    dist = np.sum(diff * diff, axis=-1)
    idx = np.argmin(dist, axis=-1).astype(np.uint32)
    idx = np.where(same[:, None], 0, idx)
    shifts = (np.arange(16, dtype=np.uint32) * 2)[None, :]
    bits = np.sum(idx << shifts, axis=1, dtype=np.uint32)

    out = np.empty((n_blk, 2), dtype=np.uint32)
    out[:, 0] = w0_s.astype(np.uint32) | (w1_s.astype(np.uint32) << 16)
    out[:, 1] = bits
    return out.tobytes()


def _encode_dxt5_alpha(a_u8: np.ndarray) -> np.ndarray:
    h, w = a_u8.shape
    blocks = a_u8.reshape(h // 4, 4, w // 4, 4).transpose(0, 2, 1, 3).reshape(-1, 16).astype(np.int32)
    a0 = np.max(blocks, axis=1)
    a1 = np.min(blocks, axis=1)
    same = a0 == a1
    pal = np.stack(
        [
            a0,
            a1,
            (6 * a0 + 1 * a1 + 3) // 7,
            (5 * a0 + 2 * a1 + 3) // 7,
            (4 * a0 + 3 * a1 + 3) // 7,
            (3 * a0 + 4 * a1 + 3) // 7,
            (2 * a0 + 5 * a1 + 3) // 7,
            (1 * a0 + 6 * a1 + 3) // 7,
        ],
        axis=1,
    )
    dist = np.abs(blocks[:, :, None] - pal[:, None, :])
    idx = np.argmin(dist, axis=-1).astype(np.uint64)
    idx = np.where(same[:, None], 0, idx)
    shifts = (np.arange(16, dtype=np.uint64) * 3)[None, :]
    bits48 = np.sum(idx << shifts, axis=1, dtype=np.uint64)
    word64 = a0.astype(np.uint64) | (a1.astype(np.uint64) << 8) | (bits48 << 16)
    return word64.view(np.uint32).reshape(-1, 2)


def write_dds_dxt5(rgba_u8: np.ndarray, out_path: str | Path):
    out_path = Path(out_path)
    h, w, _ = rgba_u8.shape
    mips = []
    cur = Image.fromarray(rgba_u8, "RGBA")
    cw, ch = w, h
    while True:
        arr = np.array(cur, dtype=np.uint8)
        pw = max(4, (cw + 3) // 4 * 4)
        ph = max(4, (ch + 3) // 4 * 4)
        if pw != cw or ph != ch:
            pad = np.zeros((ph, pw, 4), dtype=np.uint8)
            pad[:ch, :cw] = arr
            arr = pad
        a_words = _encode_dxt5_alpha(arr[:, :, 3])
        c_words = np.frombuffer(_encode_dxt1_blocks(arr[:, :, :3]), dtype=np.uint32).reshape(-1, 2)
        interleaved = np.hstack([a_words, c_words])
        mips.append(interleaved.tobytes())
        if cw == 1 and ch == 1:
            break
        cw = max(1, cw // 2)
        ch = max(1, ch // 2)
        cur = cur.resize((cw, ch), Image.Resampling.LANCZOS)

    flags = 0x1 | 0x2 | 0x4 | 0x1000 | 0x20000 | 0x80000
    pitch = max(1, (w + 3) // 4) * 16
    header = struct.pack(
        "<7I44x8I5I",
        124, flags, h, w, pitch, 0, len(mips),
        32, 0x4, struct.unpack("<I", b"DXT5")[0], 0, 0, 0, 0, 0,
        0x8 | 0x1000 | 0x400000, 0, 0, 0, 0,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(b"DDS ")
        f.write(header)
        for m in mips:
            f.write(m)


def write_dds_dxt1(rgb_u8: np.ndarray, out_path: Path):
    """Fast vectorized DXT1 encoder with full mipmap chain."""

    h, w, _ = rgb_u8.shape
    mips = []
    cur = Image.fromarray(rgb_u8, "RGB")
    cw, ch = w, h
    while True:
        arr = np.array(cur, dtype=np.uint8)
        pw = max(4, (cw + 3) // 4 * 4)
        ph = max(4, (ch + 3) // 4 * 4)
        if pw != cw or ph != ch:
            pad = np.zeros((ph, pw, 3), dtype=np.uint8)
            pad[:ch, :cw] = arr
            arr = pad
        mips.append(_encode_dxt1_blocks(arr))
        if cw == 1 and ch == 1:
            break
        cw = max(1, cw // 2)
        ch = max(1, ch // 2)
        cur = cur.resize((cw, ch), Image.Resampling.LANCZOS)

    flags = 0x1 | 0x2 | 0x4 | 0x1000 | 0x20000 | 0x80000
    pitch = max(1, (w + 3) // 4) * 8
    pf_flags = 0x4
    fourcc = b"DXT1"
    caps1 = 0x8 | 0x1000 | 0x400000
    header = struct.pack(
        "<7I44x8I5I",
        124, flags, h, w, pitch, 0, len(mips),
        32, pf_flags, struct.unpack("<I", fourcc)[0], 0, 0, 0, 0, 0,
        caps1, 0, 0, 0, 0,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(b"DDS ")
        f.write(header)
        for m in mips:
            f.write(m)


def morton2d(x: int, y: int) -> int:
    z = 0
    for i in range(16):
        z |= ((x & (1 << i)) << i) | ((y & (1 << i)) << (i + 1))
    return z


def decode_s2_vt(uexp_path: Path, max_height: int = 2048) -> np.ndarray:
    """Decode UE5 FVirtualTextureBuiltData (.uexp + .ubulk) into an RGB uint8 array."""
    ubulk_path = uexp_path.with_suffix(".ubulk")
    uexp = uexp_path.read_bytes()
    ubulk = ubulk_path.read_bytes()

    idx = uexp.find(b"PF_")
    if idx < 0:
        raise ValueError(f"No PF_ format found in {uexp_path}")
    pf = uexp[idx : idx + 12].split(b"\x00")[0].decode("ascii")
    after = struct.unpack("<16I", uexp[idx + len(pf) + 1 : idx + len(pf) + 65])
    tile_sz = after[7]
    border = after[8]
    tile_bytes = after[10]
    w = after[12]
    h = after[13]

    phys = tile_sz + 2 * border
    # If texture is huge (e.g. 2048x8192 or 2048x4096), we can decode a vertical crop or downsample
    # Wait: in Morton order, all tiles of Mip 0 are present; if we only need a 1:4 or 1:1 crop or full decode:
    ntx = w // tile_sz
    nty = h // tile_sz
    coords = sorted([(morton2d(tx, ty), tx, ty) for ty in range(nty) for tx in range(ntx)])

    if pf == "PF_DXT1":
        dds_hdr = b"DDS " + struct.pack(
            "<7I44x8I5I",
            124, 0x1007, phys, phys, tile_bytes, 0, 1,
            32, 4, int.from_bytes(b"DXT1", "little"), 0, 0, 0, 0, 0,
            0x1000, 0, 0, 0, 0,
        )
    elif pf == "PF_BC7":
        dds_hdr = b"DDS " + struct.pack(
            "<7I44x8I5I5I",
            124, 0x1007, phys, phys, tile_bytes, 0, 1,
            32, 4, int.from_bytes(b"DX10", "little"), 0, 0, 0, 0, 0,
            0x1000, 0, 0, 0, 0,
            98, 3, 0, 1, 0,
        )
    elif pf == "PF_DXT5":
        dds_hdr = b"DDS " + struct.pack(
            "<7I44x8I5I",
            124, 0x1007, phys, phys, tile_bytes, 0, 1,
            32, 4, int.from_bytes(b"DXT5", "little"), 0, 0, 0, 0, 0,
            0x1000, 0, 0, 0, 0,
        )
    else:
        raise ValueError(f"Unsupported PF format {pf} in {uexp_path}")

    canvas = np.zeros((h, w, 3), dtype=np.uint8)
    off = 4
    for _, tx, ty in coords:
        tile_raw = ubulk[off : off + tile_bytes]
        off += tile_bytes
        im = Image.open(io.BytesIO(dds_hdr + tile_raw)).convert("RGB")
        arr = np.array(im, dtype=np.uint8)[border : border + tile_sz, border : border + tile_sz]
        canvas[ty * tile_sz : (ty + 1) * tile_sz, tx * tile_sz : (tx + 1) * tile_sz] = arr

    if h > max_height:
        scale = max_height / h
        nw = max(256, int(round(w * scale)))
        canvas = np.array(
            Image.fromarray(canvas).resize((nw, max_height), Image.Resampling.LANCZOS),
            dtype=np.uint8,
        )
    return canvas


def load_s2_bark_set(rel_stem: str):
    """Load and decode (_D, _N, _RHA) for an S2 bark set."""
    base = S2_EXTRACT / "Stalker2/Content/_Stalker_2/nature" / rel_stem
    d_arr = decode_s2_vt(Path(str(base) + "_D.uexp"), max_height=4096)
    th, tw, _ = d_arr.shape

    n_path = Path(str(base) + "_N.uexp")
    if n_path.exists():
        n_arr = decode_s2_vt(n_path, max_height=4096)
        if n_arr.shape[:2] != (th, tw):
            n_arr = np.array(Image.fromarray(n_arr).resize((tw, th), Image.Resampling.BILINEAR))
    else:
        n_arr = np.full((th, tw, 3), (128, 128, 255), dtype=np.uint8)

    rha_path = Path(str(base) + "_RHA.uexp")
    if rha_path.exists():
        rha_arr = decode_s2_vt(rha_path, max_height=4096)
        if rha_arr.shape[:2] != (th, tw):
            rha_arr = np.array(Image.fromarray(rha_arr).resize((tw, th), Image.Resampling.BILINEAR))
    else:
        rha_arr = np.full((th, tw, 3), (200, 128, 220), dtype=np.uint8)

    return d_arr, n_arr, rha_arr


def grade_and_resize(
    d_arr: np.ndarray,
    n_arr: np.ndarray,
    rha_arr: np.ndarray,
    ref_rgb: np.ndarray,
    target_w: int,
    target_h: int,
    roll_x: float = 0.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Resize S2 (_D, _N, _RHA) to (target_w, target_h) preserving natural macro bark scale,
    bake S2 AO into diffuse, and color-grade toward ref_rgb using scalar luminance contrast
    (preventing per-channel chromatic hue shifts).
    """
    sh, sw, _ = d_arr.shape
    # S2 virtual textures cover a full 3-4m trunk circumference; cropping half-width/height
    # (256x1024 from 512x2048, or 512x2048 from 1024x4096) matches SoC's 1.2m UV tile scale.
    if target_w == target_h:
        crop_w = min(max(256, sw // 2), 512)
        crop_h = crop_w
    else:
        crop_w = min(max(256, sw // 2), 512)
        crop_h = min(max(1024, sh // 2), 2048)

    x0 = int(round((sw - crop_w) * (roll_x % 1.0))) if sw > crop_w else 0
    y0 = int(round((sh - crop_h) * ((roll_x * 1.7) % 1.0))) if sh > crop_h else 0
    d_sub = d_arr[y0 : y0 + crop_h, x0 : x0 + crop_w]
    n_sub = n_arr[y0 : y0 + crop_h, x0 : x0 + crop_w]
    r_sub = rha_arr[y0 : y0 + crop_h, x0 : x0 + crop_w]

    d_res = np.array(Image.fromarray(d_sub).resize((target_w, target_h), Image.Resampling.LANCZOS), dtype=np.float32)
    n_res = np.array(Image.fromarray(n_sub).resize((target_w, target_h), Image.Resampling.BILINEAR), dtype=np.float32)
    r_res = np.array(Image.fromarray(r_sub).resize((target_w, target_h), Image.Resampling.BILINEAR), dtype=np.float32)

    if roll_x != 0.0 and sw <= crop_w:
        shift = int(round(target_w * roll_x))
        d_res = np.roll(d_res, shift, axis=1)
        n_res = np.roll(n_res, shift, axis=1)
        r_res = np.roll(r_res, shift, axis=1)

    # Bake 28% of S2 Ambient Occlusion (channel B of RHA) into diffuse for deep crevice shadow
    ao = np.clip(r_res[:, :, 2] / 255.0, 0.20, 1.0)
    ao_factor = (0.72 + 0.28 * ao)[:, :, None]
    d_ao = d_res * ao_factor

    # Desaturate any excess chromatic noise in S2 albedo before matching target bark palette
    src_luma = (0.299 * d_ao[:, :, 0] + 0.587 * d_ao[:, :, 1] + 0.114 * d_ao[:, :, 2])[:, :, None]
    d_clean = src_luma * 0.55 + d_ao * 0.45

    # Match scalar luminance contrast + smoothly blend toward reference low-frequency color field
    ref_im_resized = Image.fromarray(ref_rgb).resize((target_w, target_h), Image.Resampling.BILINEAR)
    # Low-frequency spatial color field (preserves vertical trunk base darkening if any)
    ref_low = np.array(
        ref_im_resized.resize((max(4, target_w // 32), max(4, target_h // 32)), Image.Resampling.BOX).resize(
            (target_w, target_h), Image.Resampling.BILINEAR
        ),
        dtype=np.float32,
    )
    ref_f = np.array(ref_im_resized, dtype=np.float32)
    ref_luma_std = float(np.maximum((0.299 * ref_f[:, :, 0] + 0.587 * ref_f[:, :, 1] + 0.114 * ref_f[:, :, 2]).std(), 8.0))
    src_luma_std = float(np.maximum(src_luma.std(), 8.0))

    contrast_scale = np.clip((0.65 * ref_luma_std + 0.35 * src_luma_std) / src_luma_std, 0.65, 1.45)
    src_mean = d_clean.mean(axis=(0, 1), keepdims=True)
    ref_mean = ref_f.mean(axis=(0, 1), keepdims=True)

    # Blend 55% spatial low-freq reference + 35% global reference mean + 10% native S2 mean
    base_color = 0.55 * ref_low + 0.35 * ref_mean + 0.10 * src_mean
    graded = (d_clean - src_mean) * contrast_scale + base_color
    # Prevent cold blue-cyan spots on natural warm/neutral bark
    graded[:, :, 2] = np.minimum(graded[:, :, 2], graded[:, :, 1] + 2.0)
    graded_u8 = np.clip(graded, 0, 255).astype(np.uint8)
    return graded_u8, n_res.astype(np.uint8), r_res.astype(np.uint8)


def make_xray_bumps(n_u8: np.ndarray, rha_u8: np.ndarray, bump_w: int, bump_h: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Build X-Ray _bump.dds (R=Gloss, G=Nz, B=Ny, A=Nx) and _bump#.dds (R=128, G=128, B=128, A=Height).
    """
    if n_u8.shape[:2] != (bump_h, bump_w):
        n_u8 = np.array(Image.fromarray(n_u8).resize((bump_w, bump_h), Image.Resampling.BILINEAR), dtype=np.uint8)
        rha_u8 = np.array(Image.fromarray(rha_u8).resize((bump_w, bump_h), Image.Resampling.BILINEAR), dtype=np.uint8)

    nx = n_u8[:, :, 0]
    ny = 255 - n_u8[:, :, 1]
    nz = n_u8[:, :, 2]

    roughness = rha_u8[:, :, 0].astype(np.float32)
    height = rha_u8[:, :, 1]

    # X-Ray tree bark specular gloss is subtle (mean ~8-16)
    gloss = np.clip((255.0 - roughness) * 0.14 + 4.0, 2.0, 36.0).astype(np.uint8)

    bump = np.stack([gloss, nz, ny, nx], axis=-1)
    neutral = np.full_like(height, 128, dtype=np.uint8)
    bump_sharp = np.stack([neutral, neutral, neutral, height], axis=-1)
    return bump, bump_sharp


# Mapping of 28 pure tileable bark textures in gamedata.db5 -> (S2 rel_stem, target_w, target_h, roll_x)
# Excludes UV-island unwraps (trees_far_ponbark2, trees_vec_kora_02, trees_far_birchbark, trees_far_birchbark1)
BARK_MAP = {
    "trees_bark_sosna_01": ("Trees/Pine/tex/T_tre_til_pine_01", 512, 2048, 0.0),
    "trees_bark_sosna_02": ("Trees/Pine/tex/T_tre_til_pine_01", 512, 2048, 0.5),
    "trees_atp_pine_bark": ("Trees/Pine/tex/T_tre_til_pine_01", 512, 2048, 0.25),
    "trees_bark_sosna": ("Trees/Pine/tex/T_tre_til_pine_01", 512, 512, 0.0),
    "trees_bark_sosna_big": ("Trees/Pine/tex/T_tre_til_pine_01", 256, 2048, 0.0),
    "trees_bark_sosna_burned": ("Trees/Pine/tex/T_tre_til_pine_01", 512, 2048, 0.75),
    "trees_far_ponbark": ("Trees/Pine/tex/T_tre_til_pine_01", 512, 512, 0.5),
    "trees_dub_bark": ("Trees/poplar/tex/T_tre_til_poplar_01", 512, 2048, 0.0),
    "trees_bark_a_01": ("Trees/willow/Textures/T_tre_til_willow_01", 512, 2048, 0.5),
    "trees_bark_a_011": ("Trees/akacia/tex/T_tre_til_akacia_01", 512, 2048, 0.0),
    "trees_bark_a_02": ("Trees/akacia/tex/T_tre_til_akacia_b", 512, 2048, 0.0),
    "trees_bark_a_03": ("Trees/elm/tex/T_tre_elm_til", 512, 2048, 0.0),
    "trees_bark_a_04": ("Trees/linden/tex/T_tre_til_linden", 512, 2048, 0.0),
    "trees_bark_a_05": ("Trees/maple/tex/T_tre_maple_til", 512, 2048, 0.0),
    "trees_elkabark": ("Trees/fir/tex/T_tre_til_fir", 512, 512, 0.0),
    "trees_far_hembark": ("Trees/fir/tex/T_tre_til_fir", 1024, 1024, 0.0),
    "trees_far_hembark2": ("Trees/chestnut/tex/T_tre_til_chestnut_01", 1024, 1024, 0.0),
    "trees_bark_topol": ("Trees/poplar/tex/T_tre_til_poplar_01", 512, 512, 0.0),
    "trees_bark": ("Trees/poplar/tex/T_tre_til_poplar_01", 512, 512, 0.5),
    "trees_far_dead_coniferbark": ("Trees/willow/Textures/T_tre_til_willow_01", 1024, 1024, 0.0),
    "trees_bark_sux": ("Trees/willow/Textures/T_tre_til_willow_01", 512, 512, 0.0),
    "trees_bark_sux1": ("roots/Textures/T_tre_til_root_01", 512, 512, 0.0),
    "trees_bark_sux2": ("Trees/beech/tex/T_tre_til_beech", 512, 512, 0.0),
    "trees_bark_sux3": ("Trees/cherry/tex/T_tre_til_cherry", 512, 512, 0.0),
    "trees_bark_mox": ("Trees/beech/tex/T_tre_til_beech", 512, 512, 0.5),
    "trees_bark_mox1": ("roots/Textures/T_tre_til_root_01", 512, 512, 0.5),
    "trees_bark_sux_mox": ("roots/Textures/T_tre_til_root_01", 512, 2048, 0.0),
    "trees_bark_sux_mox_alt": ("roots/Textures/T_tre_til_root_01", 512, 2048, 0.5),
    "trees_bak_wood": ("Trees/poplar/tex/T_tre_til_poplar_01", 512, 1024, 0.25),
    "trees_bak_wood_ded": ("Trees/willow/Textures/T_tre_til_willow_01", 512, 1024, 0.25),
    "trees_byaka1": ("Trees/akacia/tex/T_tre_til_akacia_01", 512, 512, 0.25),
    "trees_det1": ("Trees/elm/tex/T_tre_elm_til", 512, 512, 0.0),
}

DET_OUT_DIR = ROOT / "gamedata/textures/det"
DET_MAP = {
    "det_listya": "grass/Textures/T_gra_forest_cover_02",
    "det_listya_green": "grass/Textures/T_gra_forest_cover_02",
    "det_plant_leaves": "grass/Textures/T_gra_forest_cover_02",
    "det_plant_leaves1": "grass/Textures/T_gra_forest_cover_02",
    "det_1_trava": "grass/Textures/T_gra_trava_24_01_b",
    "det_2_trava": "grass/Textures/T_gra_trava_24_01_b",
    "det_2_trava2": "grass/Textures/T_gra_trava_24_01_b",
    "det_3_trava": "grass/Textures/T_gra_trava_24_01_b",
    "det_6_trava": "grass/Textures/T_gra_trava_24_01_b",
    "det_7_trava3": "grass/Textures/T_gra_trava_24_01_b",
    "det_travzel": "grass/Textures/T_gra_trava_24_01_b",
    "det_1_krapiva": "grass/Textures/T_gra_urtica_diotica_a_01",
    "det_krapiva": "grass/Textures/T_gra_urtica_diotica_a_01",
    "det_3_lebeda": "grass/Textures/T_gra_orach",
    "det_7_lebeda": "grass/Textures/T_gra_orach",
    "det_lebeda": "grass/Textures/T_gra_orach",
}


def upgrade_det_texture(ref_rgba: np.ndarray, s2_rgb: np.ndarray) -> np.ndarray:
    """
    Upscale gamedata.db3 detail foliage texture 2x and inject high-frequency S.T.A.L.K.E.R. 2
    photogrammetry leaf/blade micro-detail while preserving 100% of the exact UV alpha silhouette.
    """
    rh, rw, _ = ref_rgba.shape
    tw, th = rw * 2, rh * 2
    ref_up = np.array(Image.fromarray(ref_rgba, "RGBA").resize((tw, th), Image.Resampling.LANCZOS), dtype=np.float32)

    # Extract high-frequency micro-contrast from S2 grass/foliage texture
    sh, sw, _ = s2_rgb.shape
    s2_crop = s2_rgb[: min(sh, th * 2), : min(sw, tw * 2)]
    s2_res = np.array(Image.fromarray(s2_crop).resize((tw, th), Image.Resampling.LANCZOS), dtype=np.float32)
    s2_low = np.array(
        Image.fromarray(s2_crop)
        .resize((max(8, tw // 16), max(8, th // 16)), Image.Resampling.BOX)
        .resize((tw, th), Image.Resampling.BILINEAR),
        dtype=np.float32,
    )
    s2_luma = 0.299 * s2_res[:, :, 0] + 0.587 * s2_res[:, :, 1] + 0.114 * s2_res[:, :, 2]
    s2_low_luma = 0.299 * s2_low[:, :, 0] + 0.587 * s2_low[:, :, 1] + 0.114 * s2_low[:, :, 2]
    micro_detail = np.clip((s2_luma - s2_low_luma) * 0.55, -28.0, 28.0)[:, :, None]

    out_rgb = np.clip(ref_up[:, :, :3] + micro_detail, 0.0, 255.0).astype(np.uint8)
    out_a = np.clip(ref_up[:, :, 3], 0.0, 255.0).astype(np.uint8)
    return np.dstack([out_rgb, out_a])


def build_diffuse_thm(w: int, h: int, bump_name: str, det_name: str = "trees\\trees_det1") -> bytes:
    """Build a valid X-Ray THM descriptor linking a diffuse bark texture to its S2 bump and detail map."""
    def chunk(cid: int, payload: bytes) -> bytes:
        return struct.pack("<II", cid, len(payload)) + payload

    c_ver = chunk(0x0810, struct.pack("<H", 0x0012))
    c_type = chunk(0x0813, struct.pack("<I", 1))
    # fmt=0 (DXT1), flags=0x04800001 (mipmaps), border=0, fade_color=0x00808080, fade_amount=0, mip_filter=14, width=w, height=h
    c_param = chunk(0x0812, struct.pack("<8I", 0, 0x04800001, 0, 0x00808080, 0, 14, w, h))
    c_ttype = chunk(0x0814, struct.pack("<I", 0))  # ttImage
    c_det = chunk(0x0815, det_name.encode("ascii") + b"\x00" + struct.pack("<f", 2.0))
    c_mat = chunk(0x0816, struct.pack("<If", 1, 0.80))
    c_bump = chunk(0x0817, struct.pack("<fI", 0.05, 2) + bump_name.encode("ascii") + b"\x00")
    c_ext = chunk(0x0818, b"\x00")
    c_mip = chunk(0x0819, b"\x00")
    return c_ver + c_type + c_param + c_ttype + c_det + c_mat + c_bump + c_ext + c_mip


def build_bump_thm(w: int, h: int) -> bytes:
    """Build a valid X-Ray THM descriptor for a _bump.dds normal/specular map."""
    def chunk(cid: int, payload: bytes) -> bytes:
        return struct.pack("<II", cid, len(payload)) + payload

    c_ver = chunk(0x0810, struct.pack("<H", 0x0012))
    c_type = chunk(0x0813, struct.pack("<I", 1))
    c_param = chunk(0x0812, struct.pack("<8I", 2, 0x02000100, 0, 0, 0, 0, w, h))
    c_ttype = chunk(0x0814, struct.pack("<I", 2))  # ttBumpMap
    c_det = chunk(0x0815, b"\x00" + struct.pack("<f", 1.0))
    c_mat = chunk(0x0816, struct.pack("<If", 1, 0.0))
    c_bump = chunk(0x0817, struct.pack("<fI", 0.05, 1) + b"\x00")
    c_ext = chunk(0x0818, b"\x00")
    c_mip = chunk(0x0819, b"\x00")
    return c_ver + c_type + c_param + c_ttype + c_det + c_mat + c_bump + c_ext + c_mip


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DET_OUT_DIR.mkdir(parents=True, exist_ok=True)
    s2_cache = {}

    with XdbArchive(ROOT / "gamedata.db5") as db5:
        entries_by_path = {e.path: e for e in db5.entries if e.path.startswith("textures/trees/")}

        comparisons = []
        installed_dds = 0
        installed_bumps = 0
        installed_thms = 0

        for name, (s2_stem, tw, th, roll_x) in BARK_MAP.items():
            dds_rel = f"textures/trees/{name}.dds"
            if dds_rel not in entries_by_path:
                print(f"[!] Missing in db5: {dds_rel}")
                continue

            if s2_stem not in s2_cache:
                print(f"[*] Decoding S2 VT set: {s2_stem} ...")
                s2_cache[s2_stem] = load_s2_bark_set(s2_stem)
            d_s2, n_s2, rha_s2 = s2_cache[s2_stem]

            ref_bytes = db5.read(entries_by_path[dds_rel])
            ref_im = Image.open(io.BytesIO(ref_bytes)).convert("RGB")
            ref_rgb = np.array(ref_im, dtype=np.uint8)

            graded_rgb, n_res, rha_res = grade_and_resize(d_s2, n_s2, rha_s2, ref_rgb, tw, th, roll_x)
            out_dds = OUT_DIR / f"{name}.dds"
            write_dds_dxt1(graded_rgb, out_dds)
            installed_dds += 1

            # Save comparison sample for first 8 species
            if len(comparisons) < 8 and roll_x == 0.0:
                comparisons.append((name, ref_im.resize((256, 512)), Image.fromarray(graded_rgb).resize((256, 512))))

            # Generate pixel-aligned S2 _bump.dds and _bump#.dds + .thm for every bark texture
            # (skipping trees_det1 itself since trees_det1 is the detail texture)
            if name != "trees_det1":
                bw, bh = max(256, tw // 2), max(256, th // 2)
                bump_prefix = f"{name}_bump"
                bump_rgba, bump_sharp_rgba = make_xray_bumps(n_res, rha_res, bw, bh)
                write_dds_dxt5(bump_rgba, str(OUT_DIR / f"{bump_prefix}.dds"))
                write_dds_dxt5(bump_sharp_rgba, str(OUT_DIR / f"{bump_prefix}#.dds"))
                installed_bumps += 2

                (OUT_DIR / f"{bump_prefix}.thm").write_bytes(build_bump_thm(bw, bh))
                (OUT_DIR / f"{name}.thm").write_bytes(build_diffuse_thm(tw, th, f"trees\\{bump_prefix}"))
                installed_thms += 2
            else:
                bw, bh = 256, 256
                bump_prefix = "trees_det1_bump"
                bump_rgba, bump_sharp_rgba = make_xray_bumps(n_res, rha_res, bw, bh)
                write_dds_dxt5(bump_rgba, str(OUT_DIR / f"{bump_prefix}.dds"))
                write_dds_dxt5(bump_sharp_rgba, str(OUT_DIR / f"{bump_prefix}#.dds"))
                installed_bumps += 2

        # Build comparison contact sheet
        if comparisons:
            sheet_w = len(comparisons) * 256
            sheet_h = 1024
            sheet = Image.new("RGB", (sheet_w, sheet_h))
            for i, (name, before_im, after_im) in enumerate(comparisons):
                sheet.paste(before_im, (i * 256, 0))
                sheet.paste(after_im, (i * 256, 512))
            sheet_path = ROOT / "docs/shots/s2_bark_comparison.png"
            sheet_path.parent.mkdir(parents=True, exist_ok=True)
            sheet.save(sheet_path)
            print(f"[+] Saved comparison sheet: {sheet_path}")

        print(
            f"[+] Installed {installed_dds} diffuse DDS, {installed_bumps} bump/bump# DDS, "
            f"and {installed_thms} THM descriptors into {OUT_DIR}"
        )

    # Upgrade detail foliage textures in gamedata/textures/det/
    det_cache = {}
    installed_det = 0
    with XdbArchive(ROOT / "gamedata.db3") as db3:
        det_entries = {e.path: e for e in db3.entries if e.path.startswith("textures/det/")}
        for det_name, s2_gra_stem in DET_MAP.items():
            det_rel = f"textures/det/{det_name}.dds"
            if det_rel not in det_entries:
                continue
            if s2_gra_stem not in det_cache:
                uexp_p = S2_EXTRACT / "Stalker2/Content/_Stalker_2/nature" / f"{s2_gra_stem}_D.uexp"
                print(f"[*] Decoding S2 grass VT: {s2_gra_stem} ...")
                det_cache[s2_gra_stem] = decode_s2_vt(uexp_p, max_height=2048)
            ref_im = Image.open(io.BytesIO(db3.read(det_entries[det_rel]))).convert("RGBA")
            up_rgba = upgrade_det_texture(np.array(ref_im, dtype=np.uint8), det_cache[s2_gra_stem])
            write_dds_dxt5(up_rgba, DET_OUT_DIR / f"{det_name}.dds")
            installed_det += 1
    print(f"[+] Installed {installed_det} upgraded detail foliage DDS textures into {DET_OUT_DIR}")


if __name__ == "__main__":
    main()
