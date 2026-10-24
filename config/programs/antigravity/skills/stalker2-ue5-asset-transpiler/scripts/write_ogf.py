"""Write aisha.ogf (rigid one-bone OGF v4) from aisha_mesh.json using a game OGF as the container template.
Usage: write_ogf.py MESH_JSON TEMPLATE_OGF OUT_OGF [texture] [shader]"""
import json, struct, sys
mesh_json, tpl_path, out_path = sys.argv[1:4]
tex = sys.argv[4] if len(sys.argv) > 4 else "actors\\aisha_body"
shader = sys.argv[5] if len(sys.argv) > 5 else "models\\model"
m = json.load(open(mesh_json)); P, N, UV, T = m["positions"], m["normals"], m["uvs"], m["triangles"]
tpl = open(tpl_path, "rb").read()

def chunks(b, o, end):
    r = []
    while o + 8 <= end:
        i, s = struct.unpack_from("<II", b, o); r.append((i, b[o + 8:o + 8 + s])); o += 8 + s
    return r
def pack(cs): return b"".join(struct.pack("<II", i, len(d)) + d for i, d in cs)

# winding: match the template (check sign of geometric normal vs stored normal, in the same left-handed space)
tc = dict(chunks(tpl, 0, len(tpl)))
kids = chunks(tc[9], 0, len(tc[9]))
kc = dict(kids[-1][1] and chunks(kids[-1][1], 0, len(kids[-1][1])))
tv = kc[3]; cnt = struct.unpack_from("<I", tv, 4)[0]
tvs = [struct.unpack_from("<15f", tv, 8 + 60 * i) for i in range(cnt)]
ti = kc[4]; n = struct.unpack_from("<I", ti, 0)[0]; idx = struct.unpack_from(f"<{n}H", ti, 4)
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def dot(a, b): return sum(x * y for x, y in zip(a, b))
a, b, c = (tvs[i] for i in idx[:3])
tpl_sign = dot(cross(sub(b[:3], a[:3]), sub(c[:3], a[:3])), a[3:6])
mine = [tuple(t) for t in T]
a, b, c = (P[i] for i in mine[0]); 
my_sign = dot(cross(sub(b, a), sub(c, a)), N[mine[0][0]])
if (tpl_sign > 0) != (my_sign > 0): mine = [(t[0], t[2], t[1]) for t in mine]
print("template winding sign", tpl_sign > 0, "mine", my_sign > 0, "-> flipped" if (tpl_sign > 0) != (my_sign > 0) else "")

# vertices: pos, normal, tangent, binormal, uv, bone  (60 bytes)
def norm(v):
    l = dot(v, v) ** .5 or 1.0; return tuple(x / l for x in v)
vb = bytearray(struct.pack("<II", 0x12071980, len(P)))
for p, nn, uv in zip(P, N, UV):
    nn = norm(nn); t = norm(cross((0, 1, 0), nn)) if abs(nn[1]) < .99 else (1.0, 0.0, 0.0); bn = norm(cross(nn, t))
    vb += struct.pack("<14fI", *p, *nn, *t, *bn, uv[0], uv[1], 0)
assert len(vb) == 8 + 60 * len(P)
ib = struct.pack("<I", len(mine) * 3) + b"".join(struct.pack("<3H", *t) for t in mine)
lo = [min(p[i] for p in P) for i in range(3)]; hi = [max(p[i] for p in P) for i in range(3)]
ctr = [(l + h) / 2 for l, h in zip(lo, hi)]; half = [(h - l) / 2 for l, h in zip(lo, hi)]
rad = max(dot(sub(p, ctr), sub(p, ctr)) ** .5 for p in P)
def hdr(t): return struct.pack("<BBH6f4f", 4, t, 0, *lo, *hi, *ctr, rad)
swi = bytes(16) + struct.pack("<IIHH", 1, 0, len(mine), len(P))
child = pack([(1, hdr(4)), (2, tex.encode() + b"\0" + shader.encode() + b"\0"), (3, bytes(vb)), (4, ib), (6, swi)])

# bone obb: rot(9f) trans(3f) half(3f) -> keep the template rotation, set the box to the model
def patch_box(b, off):
    b = bytearray(b); struct.pack_into("<6f", b, off + 36, *ctr, *half); return bytes(b)
bones = bytearray(tc[13]); bones = patch_box(bones, 4 + len(b"bone01\0") + 1)
ik = bytearray(tc[16]); mat_end = 4 + ik[4:].index(0) + 1
ik = patch_box(ik, mat_end + 4)
root = pack([(1, hdr(0x0a)), (18, tc[18]), (9, pack([(0, child)])), (13, bones), (16, ik)])
open(out_path, "wb").write(root)
print("wrote", out_path, len(root), "bytes", len(P), "verts", len(mine), "tris; bbox", [round(x, 3) for x in lo], [round(x, 3) for x in hi])
