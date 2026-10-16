---
name: godot-shader-vfx
description: Authoring 2D and 3D visual shaders, canvas item shaders, spatial shaders, particle systems, and screen-reading post-processing effects in Godot Engine 4.
---

# Godot 4 Shader Architecture & Visual VFX Guide

This skill governs writing high-performance visual shaders, screen-space effects, interactive water, foliage wind swaying, and GPU compute particle systems in **Godot Engine 4 (GDShader)**.

---

## 1. GDShader Types & Execution Pipeline

Godot provides dedicated shader types for different rendering domains:
- `shader_type spatial;`: 3D PBR materials, custom lighting models, vertex displacement.
- `shader_type canvas_item;`: 2D sprites, UI components, fullscreen 2D screen reading.
- `shader_type particles;`: GPU-accelerated particle movement and physics simulation.
- `shader_type fog;`: Volumetric fog density and scattering.

---

## 2. High-Performance Screen-Space Distortion (Heat Haze / Shockwaves)

Screen-reading shaders read from `SCREEN_TEXTURE` to distort the world behind an object:

```glsl
shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture, filter_linear_mipmap;
uniform sampler2D noise_texture : repeat_enable;
uniform float distortion_strength : hint_range(0.0, 0.1) = 0.02;
uniform float speed : hint_range(0.0, 5.0) = 1.0;

void fragment() {
    vec2 uv_offset = texture(noise_texture, UV + vec2(TIME * speed * 0.1, 0.0)).rg * 2.0 - 1.0;
    vec2 distorted_screen_uv = SCREEN_UV + (uv_offset * distortion_strength);
    
    vec4 screen_color = texture(screen_texture, distorted_screen_uv);
    COLOR = screen_color;
}
```

---

## 3. Vertex Displacement: 3D Foliage & Grass Wind Sway

Avoid animating individual bones for vegetation. Displace vertices on the GPU in the `vertex()` stage:

```glsl
shader_type spatial;
render_mode cull_disabled;

uniform sampler2D wind_noise;
uniform float wind_strength : hint_range(0.0, 2.0) = 0.3;
uniform float wind_speed : hint_range(0.0, 5.0) = 1.5;

void vertex() {
    // Only sway vertices above the root (UV.y represents vertical height)
    float height_factor = 1.0 - UV.y;
    
    vec2 world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xz;
    float wind_sample = texture(wind_noise, (world_pos * 0.1) + vec2(TIME * wind_speed * 0.05)).r;
    
    VERTEX.x += (wind_sample * 2.0 - 1.0) * wind_strength * height_factor;
    VERTEX.z += (wind_sample * 2.0 - 1.0) * wind_strength * height_factor;
}
```
