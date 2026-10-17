---
name: pbr-radiometry-color-dsp-math
description: Physically Based Rendering (Cook-Torrance GGX BRDF), legacy X-Ray gloss-to-PBR roughness bijective mapping, IEC 61966-2-1 sRGB/Linear colorimetry, ACES Filmic tonemapping, Spherical Harmonics irradiance, and audio/texture DSP math.
---

# PBR Radiometry, Shader Colorimetry, Spherical Harmonics & DSP Math

## When to Use
Activate this skill whenever:
- Writing or porting HLSL/GLSL/Slang shaders (`xray-dx11-shader-modernization`, UE5-to-OGSR PBR material transpilation).
- Converting legacy S.T.A.L.K.E.R. `_bump` / `_bump#` specular gloss maps into modern PBR Roughness/Metallic/AO (`ORM`) maps or vice versa.
- Balancing HDR weather lighting, sun shafts, bloom luminance thresholds, ACES Filmic tonemapping, or Spherical Harmonics ambient sky irradiance.
- Processing audio dB/LUFS attenuation curves or alpha-tested foliage mipmap coverage integrals.

---

## 1. Cook-Torrance Microfacet BRDF & Energy Conservation

The physically based reflectance equation for outgoing radiance $L_o(\mathbf{v})$ from light direction $\mathbf{l}$, view vector $\mathbf{v}$, surface normal $\mathbf{n}$, and half-vector $\mathbf{h} = \frac{\mathbf{l} + \mathbf{v}}{\|\mathbf{l} + \mathbf{v}\|}$:
$$f_r(\mathbf{l}, \mathbf{v}) = (1 - F(\mathbf{v}, \mathbf{h}))(1 - m)\frac{\mathbf{c}_{\text{albedo}}}{\pi} + \frac{D_{\text{GGX}}(\mathbf{n}, \mathbf{h}, \alpha) \, F_{\text{Schlick}}(\mathbf{v}, \mathbf{h}, F_0) \, G_{\text{Smith}}(\mathbf{n}, \mathbf{v}, \mathbf{l}, \alpha)}{4 (\mathbf{n}\cdot\mathbf{l})(\mathbf{n}\cdot\mathbf{v}) + \epsilon}$$
where perceptual roughness $r \in [0.04, 1.0]$ maps to microfacet roughness $\alpha = r^2$:
1. **Trowbridge-Reitz GGX Normal Distribution ($D_{\text{GGX}}$):**
   $$D_{\text{GGX}}(\mathbf{n}, \mathbf{h}, \alpha) = \frac{\alpha^2}{\pi \left((\mathbf{n}\cdot\mathbf{h})^2 (\alpha^2 - 1) + 1\right)^2}$$
2. **Schlick Fresnel Approximation ($F_{\text{Schlick}}$):**
   $$F_0 = \text{mix}(0.04,\; \mathbf{c}_{\text{albedo}},\; m), \qquad F(\mathbf{v}, \mathbf{h}, F_0) = F_0 + (1 - F_0)\left(1 - \max(\mathbf{v}\cdot\mathbf{h}, 0)\right)^5$$
3. **Height-Correlated Smith-GGX Visibility Function ($V = \frac{G_2}{4(\mathbf{n}\cdot\mathbf{l})(\mathbf{n}\cdot\mathbf{v})}$):**
   $$V_{\text{SmithGGX}}(NdotL, NdotV, \alpha) = \frac{0.5}{\text{lerp}(2 \, NdotL \, NdotV,\; NdotL + NdotV,\; \alpha)}$$

### Legacy Blinn-Phong / X-Ray Gloss $\leftrightarrow$ PBR Roughness Mapping
To convert between Blinn-Phong specular power $s \in [2, 2048]$, legacy X-Ray gloss $g \in [0, 1]$, and PBR perceptual roughness $r \in [0, 1]$:
$$r = \left(\frac{2}{s + 2}\right)^{1/4} \approx 1 - g, \qquad s = \frac{2}{\max(r, 0.04)^4} - 2$$

---

## 2. Exact Colorimetry, sRGB Transfer Functions & ACES Tonemapping

### Exact IEC 61966-2-1 sRGB $\leftrightarrow$ Linear Radiance
Never use a naive `pow(c, 2.2)` when exact dark-shadow precision is required; use the piecewise standard (or fast polynomial):
$$\text{sRGB\_to\_Linear}(c) = \begin{cases} \dfrac{c}{12.92}, & c \le 0.04045 \\[6pt] \left(\dfrac{c + 0.055}{1.055}\right)^{2.4}, & c > 0.04045 \end{cases}$$
$$\text{Linear\_to\_sRGB}(l) = \begin{cases} 12.92 \, l, & l \le 0.0031308 \\[6pt] 1.055 \, l^{1/2.4} - 0.055, & l > 0.0031308 \end{cases}$$

### ITU-R BT.709 Relative Luminance (For Bloom Thresholds & Exposure Metering)
$$Y = 0.2126 \, R_{\text{lin}} + 0.7152 \, G_{\text{lin}} + 0.0722 \, B_{\text{lin}}$$

### Narkowicz ACES Filmic Tonemapping Curve (HDR $\rightarrow$ SDR $[0, 1]$)
For pre-exposed linear HDR color $x$:
$$\text{ACES}(x) = \text{saturate}\!\left(\frac{x(2.51 x + 0.03)}{x(2.43 x + 0.59) + 0.14}\right)$$

---

## 3. Spherical Harmonics ($L_2$) Irradiance for Skybox & Hemi Lighting

A 9-coefficient 2nd-order real Spherical Harmonics basis $Y_{lm}(\mathbf{n})$ approximates diffuse sky irradiance $E(\mathbf{n}) = \int_{\Omega} L(\omega)\max(\mathbf{n}\cdot\omega, 0)\,d\omega$ in a single vertex/pixel shader evaluation:
$$E(\mathbf{n}) = c_1 L_{22}(x^2 - y^2) + c_2 L_{20}(3z^2 - 1) + c_3 L_{10} z + c_4 L_{00} - c_5 L_{20} + 2c_1(L_{2,-2}xy + L_{21}xz + L_{2,-1}yz) + 2c_3(L_{11}x + L_{1,-1}y)$$
where $c_1 = 0.429043, c_2 = 0.511664, c_3 = 0.743125, c_4 = 0.886227, c_5 = 0.247708$.

---

## 4. Foliage Alpha-Coverage Preservation Across Mipmap Levels

Standard box-filter mipmapping averages alpha values toward $0.5$, causing alpha-tested (`alpha_ref = 0.5`) S.T.A.L.K.E.R. trees and bushes to vanish at a distance!
Given base mip $0$ coverage fraction $C_0 = \frac{1}{N_0}\sum \mathbb{I}(\alpha_i^{(0)} > \tau_{\text{ref}})$, scale each mip level $k$'s alpha channel by $s_k$ via binary search so its coverage matches $C_0$:
$$C_k(s_k) = \frac{1}{N_k}\sum_{j=1}^{N_k} \mathbb{I}\!\left(\text{clamp}(s_k \cdot \alpha_j^{(k)}, 0, 1) > \tau_{\text{ref}}\right) \equiv C_0$$

---

## 5. Audio Distance Attenuation & Decibel Math (GSC Ogg Vorbis)

- **Linear Amplitude $A \leftrightarrow \text{dBFS}$:**
  $$L_{\text{dB}} = 20 \log_{10}(A), \qquad A = 10^{L_{\text{dB}} / 20}$$
- **X-Ray Inverse Clamped Distance Falloff (`min_dist` $d_{\min}$, `max_dist` $d_{\max}$):**
  $$G(d) = \begin{cases} 1.0, & d \le d_{\min} \\[4pt] \dfrac{d_{\min}}{d} \cdot \dfrac{d_{\max} - d}{d_{\max} - d_{\min}}, & d_{\min} < d < d_{\max} \\[4pt] 0.0, & d \ge d_{\max} \end{cases}$$
