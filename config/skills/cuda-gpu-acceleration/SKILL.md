---
name: cuda-gpu-acceleration
description: High-performance NVIDIA GPU engineering, CUDA 13.4 kernel development, nvcc compilation, Tensor Core acceleration, PyTorch CUDA extensions, and OptiX ray-tracing for modern NVIDIA GPUs (RTX 5060/Blackwell).
---

# NVIDIA CUDA GPU Acceleration & Kernel Engineering

This skill provides specialized standards for writing, profiling, and deploying GPU-accelerated software using **NVIDIA CUDA 13.4**, TensorRT, and OptiX on modern NVIDIA GPUs (including RTX 50-series Blackwell architecture).

---

## 🎯 When to Activate

* **CUDA Kernel Authoring:** Writing and optimizing custom `__global__` and `__device__` CUDA C++ functions.
* **GPU Memory Optimization:** Eliminating uncoalesced global memory accesses, maximizing shared memory (`__shared__`) reuse, and preventing warp divergence.
* **PyTorch / C++ Extensions:** Authoring custom CUDA C++ extensions using `torch.utils.cpp_extension` or LibTorch.
* **Tensor Core & Numerical Acceleration:** Utilizing FP16, BF16, and FP8 precision on Tensor Cores for deep learning, simulation, or signal processing.
* **Headless OptiX / Ray Tracing:** Accelerating 3D geometry rendering and spatial BVH tree traversal.

---

## 🛠️ Compilation & Development Toolchain

* **Compiler:** `/opt/cuda/bin/nvcc`
* **Target Architecture Flags:**
  * For RTX 5060 Mobile / Blackwell (compute capability 10.0 / sm_100 or sm_90 fallback):
    ```bash
    nvcc -O3 -arch=native -Xcompiler -O3,-fPIC kernel.cu -o kernel
    ```
* **Memory Hierarchy Checklist:**
  1. **Global Memory:** Ensure 128-byte aligned, coalesced memory transactions across threads in a warp (consecutive threads access consecutive memory addresses).
  2. **Shared Memory (`__shared__`):** Stage frequently accessed global data into 32-bank on-chip shared memory to avoid high-latency DRAM trips. Avoid bank conflicts (`stride != 32`).
  3. **Warp Uniformity:** Keep control flow (`if/else`) uniform across groups of 32 threads (`warp`) to eliminate branch serialization.

---

## 📊 Summary Output Format

When reporting GPU build and benchmark metrics, report in 1-line indicators:
* `nvcc: [✓] Compiled kernel.cu (sm_native, 0 errors, 28 registers/thread)`
* `cuda benchmark: [✓] Bandwidth: 224.5 GB/s (92% peak), Latency: 0.14ms`
