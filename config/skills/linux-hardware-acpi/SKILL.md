---
name: linux-hardware-acpi
description: Linux kernel ACPI module development, DSDT/SSDT table analysis, hwmon sensor interfaces, thermal fan curves, and systemd D-Bus daemons.
---

# Linux Hardware Engineering & ACPI Subsystems

This skill guides the development and debugging of Linux kernel ACPI modules, custom WMI drivers, thermal fan control daemons, and hardware telemetry services (e.g. for HP OMEN laptops).

---

## 💻 1. Kernel ACPI & WMI Architecture

### 1. Decompiling DSDT / SSDT Firmware Tables
Extract and disassemble the machine's ACPI tables to inspect vendor methods:
```bash
# Dump raw ACPI tables
sudo acpidump > acpidump.dat
acpixtract -a acpidump.dat

# Disassemble to readable ASL (ACPI Source Language)
iasl -d dsdt.dat ssdt*.dat
```
Search the resulting `.dsl` files for WMI GUIDs, thermal zones (`_TZ`), and embedded controller methods (`EC0`).

### 2. Linux Kernel Driver Skeleton (`omen-acpi`)
* Use standard kernel module macros and WMI event handlers:
  ```c
  #include <linux/init.h>
  #include <linux/module.h>
  #include <linux/wmi.h>
  #include <linux/hwmon.h>
  #include <linux/hwmon-sysfs.h>

  MODULE_LICENSE("GPL");
  MODULE_AUTHOR("Eric Parsley");
  MODULE_DESCRIPTION("HP OMEN ACPI / Thermal Platform Driver");
  ```
* Register standard `/sys/class/hwmon/` sysfs nodes for:
  * Fan RPM readouts (`fan1_input`, `fan2_input`).
  * Target PWM duty cycle (`pwm1`, `pwm2`).
  * Temperature sensors (`temp1_input`).

---

## 🌪️ 2. Thermal Management & Fan Curve Daemons (`omen-space`)

* **Low-Overhead Daemon:** Run background fan management as a systemd service (`omen-space.service`).
* **Hysteresis Smoothing:** Implement temperature hysteresis (e.g. 3°C delta) to prevent rapid fan speed oscillations (revving up and down repeatedly).
* **D-Bus Control Interface:** Expose fan profiles (Quiet, Balanced, Performance, Max) over system D-Bus (`org.freedesktop.omen`) so unprivileged desktop UIs can adjust profiles without requiring `sudo`.

---

## 🛡️ 3. Safety Safeguards

* **Hardware Failsafe:** Never disable kernel thermal emergency cutoffs. If communication with the embedded controller drops, default immediately to 100% fan duty cycle to protect the CPU/GPU from thermal damage.
* **DKMS Verification:** Always test building against current kernel headers (`dkms status`) before triggering reboots.
