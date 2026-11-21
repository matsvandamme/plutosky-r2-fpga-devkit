---
icon: material/ip-network-outline
description: Pin the board to a fixed address, go back to DHCP, or change the name it answers to.
---

# Change the IP address or name

Out of the card, Ethernet takes its address from your router (DHCP) and the
board answers to `fishball.local`. Both are ordinary Debian settings.

```bash
# run from: the repo root
./devkit net                          # what is it doing now?
./devkit net find                     # look for the board without knowing its address
```

To change them, log in and use Debian's own tools: the address is in
`/etc/network/interfaces`, and the name is set with
`hostnamectl set-hostname mysdr`, after which the board answers to
`mysdr.local`. `./devkit net static`, `dhcp` and `name` are for the R1's
Buildroot firmware; on Debian they refuse and print the command to run instead.

| Good to know | |
|---|---|
| a DHCP reservation in your router is usually the better answer | the board keeps its gateway and DNS |
| the serial console on `DEBUG` does not depend on the network | it is the way back in after a wrong address |
| the USB network at `192.168.2.1` does not change with these | on a PC with an RNDIS driver; on a Mac, once the board is [switched to `ncm`](use-a-mac.md#reach-the-board-over-the-usb-cable) (from v0.2) |

Every route and recovery from a lock-out, written for the R1:
[networking reference](../networking.md).
