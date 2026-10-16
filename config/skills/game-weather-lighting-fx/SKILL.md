---
name: game-weather-lighting-fx
description: Dynamic game weather cycles, HDR tonemapping, sun shafts/god rays, skybox balance, and blinding glare/light-bleed suppression (S.T.A.L.K.E.R. X-Ray/OGSR & RPG engines).
---

# Game Weather & Lighting FX Engineering (`game-weather-lighting-fx`)

The `game-weather-lighting-fx` skill provides specialized architectural guidelines, parameter calibrations, and automated audit tools for balancing weather cycles, environmental lighting, sun glare, HDR tonemapping, and shadow bleed in game engines (especially **S.T.A.L.K.E.R. X-Ray / OGSR / S.T.A.L.K.E.R. 2** and similar deferred/forward+ renderers).

---

## 1. Core Visual Anomalies & Root Causes

### A. Blinding Sun Glare & Overblown Bloom
- **Symptom:** Looking toward the sun or bright horizons completely washes out the viewport with blinding white light, obscuring terrain and geometry.
- **Root Cause:**
  - High `r2_sun_lumscale` (> 1.8) combined with high `r2_ls_bloom_kernel_scale` and low `r2_ls_bloom_threshold`.
  - Overblown `sun_color` RGB values in weather LTX files (e.g. `sun_color = 2.5, 2.4, 2.2`).
- **Calibration Target:**
  ```ini
  r2_sun_lumscale 1.0           ; Range: 0.8 - 1.2
  r2_sun_lumscale_hemi 0.85     ; Hemispheric sky bounce
  r2_sun_lumscale_amb 0.45      ; Ambient fill
  r2_ls_bloom_threshold 0.65    ; Pixels brighter than 0.65 trigger bloom
  r2_ls_bloom_kernel_scale 0.7  ; Bloom blur kernel spread
  ```

### B. Sun Shafts Bleeding Through Terrain & World Geometry
- **Symptom:** Volumetric light rays (god rays) pierce through solid hills, mountains, and building roofs.
- **Root Cause:**
  - Incorrect shadow map depth bias (`r2_sun_bias`), causing back-buffer geometry acne or self-shadowing detachment.
  - Insufficient shadow map resolution (`r2_sun_near`, `r2_sun_far` cascade partition distance too shallow).
- **Resolution:**
  ```ini
  r2_sun_shafts 1               ; 1 = Screen-space volumetric rays (stable); 2 = Compute depth shafts
  r2_sun_bias 0.0005            ; Prevents shadow acne and terrain bleed
  r2_sun_near 20.0              ; High-precision near shadow cascade distance (meters)
  r2_sun_far 180.0              ; Max shadow rendering distance
  r2_sun_tsm on                 ; Trapezoidal Shadow Maps for perspective-aligned resolution
  ```

### C. HDR Tonemapping & Exposure Pumping
- **Symptom:** Walking out of a dark bunker or tunnel into daylight causes sudden jarring exposure swings ("exposure pumping") or leaves dark areas pitch black for multiple seconds.
- **Resolution:**
  ```ini
  r2_tonemap on
  r2_tonemap_middlegray 1.0     ; Target luminance exposure adaptation
  r2_tonemap_low_lum 0.0001     ; Minimum scene luminance clamp (prevents pure black adaptation stall)
  r2_tonemap_amount 0.7         ; Tonemap weight (0.0 = linear clip, 1.0 = full logarithmic curve)
  ```

### D. Cutscene Intro Camera Flashes (e.g. Pre-Death Truck Sidorovich Flash)
- **Symptom:** Starting a new game renders the NPC in their bunker for 1 frame before transitioning to the intro cutscene truck.
- **Root Cause:** Engine renders the default spawn actor camera position before `game_cameras.start()` or cutscene script invokes `level.set_cam_custom_position()`.
- **Script Solution:** Delay world visual rendering or fade-in from pure black during the first 500ms of level load in `bind_stalker.net_Spawn`.

---

## 2. CLI Tooling: `weather-lighting-tuner`

The companion helper script `weather_lighting_tuner.py` automates inspecting weather configs and generating balanced user lighting settings:

```bash
# Audit weather LTX files for blinding glare:
python3 config/skills/game-weather-lighting-fx/scripts/weather_lighting_tuner.py audit gamedata/config/weathers/

# Auto-clamp overblown RGB parameters in weather LTX:
python3 config/skills/game-weather-lighting-fx/scripts/weather_lighting_tuner.py audit gamedata/config/weathers/ --fix

# Generate balanced user.ltx lighting configuration:
python3 config/skills/game-weather-lighting-fx/scripts/weather_lighting_tuner.py gen-config --out gamedata/user_balanced_lighting.ltx
```

---

## 3. Best Practices Checklist

1. `[ ]` **Clamp Sun Colors:** Never set `sun_color` RGB higher than `1.4, 1.4, 1.3` in weather LTX files.
2. `[ ]` **Separate Direct vs Hemi Light:** Keep `hemi_color` at ~60-70% of `sun_color` to maintain readable shadows.
3. `[ ]` **Test at Low Sun Angles:** Verify sunrise (06:00) and sunset (19:00) weather frames where sun shafts intersect low geometry.
4. `[ ]` **Preserve Atmospheric Contrast:** Cloud overcast frames should reduce `r2_sun_lumscale` and elevate ambient fill.
