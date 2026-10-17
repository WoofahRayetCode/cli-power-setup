---
name: network-protocol-engineering
description: Packet inspection with tshark and tcpdump, binary serialization with Protobuf and FlatBuffers, custom TCP/UDP client-servers, and Linux TUN/TAP network routing.
---

# Network Protocol Engineering & Packet Diagnostics

This skill governs network systems engineering, binary wire protocols, packet capture analysis (`pcap`), and virtual network interface routing (TUN/TAP, VPNs, and network tethering).

---

## 📡 1. Packet Capture & Traffic Triage (`tshark`)

Analyze network packets directly from the terminal without launching Wireshark GUI:

```bash
# Capture and decode HTTP / DNS / TCP handshakes on interface eth0
tshark -i eth0 -f "tcp port 80 or udp port 53" -T fields -e frame.time_relative -e ip.src -e ip.dst -e _ws.col.Info -c 20

# Inspect TLS SNI (Server Name Indication) domains
tshark -r capture.pcap -Y "tls.handshake.extensions_server_name" -T fields -e tls.handshake.extensions_server_name | sort -u
```

---

## 🔌 2. Linux TUN/TAP & Virtual Network Routing

Directly applicable to projects like `tetherfusenet` and local VPNs:

```bash
# Create persistent TUN interface
ip tuntap add dev tun0 mode tun user $USER
ip addr add 10.0.0.1/24 dev tun0
ip link set dev tun0 up

# Enable kernel IP forwarding and NAT iptables masquerade
sysctl -w net.ipv4.ip_forward=1
iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
iptables -A FORWARD -i tun0 -o wlan0 -j ACCEPT
```

---

## 🔄 Interoperability & Handoffs

* **Handoff to `android-app-engineering`:** For implementing VpnService and USB tethering tunnels in Kotlin.
* **Handoff to `linux-systems-engineering`:** For non-blocking epoll sockets and high-performance I/O loops.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`network-packet-stream-condenser`**: Network packet stream and PCAP trace condenser. Flattens verbose tshark and tcpdump protocol dissection trees ...
- **`binary-re-workflows`**: Orchestrates reverse engineering tools (REA MCP, Ghidra, JADX, TShark, objdump, hex analysis) with Superpowers...
- **`standalone-binary-re`**: Standalone binary reverse engineering without external MCP servers. Uses native Linux CLI utilities (objdump, ...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.
