---
icon: material/lan-connect
description: Both USB-C sockets for power, Ethernet for the network, then fishball.local.
---

# Connect and find the board

Both USB-C sockets for power, Ethernet for the network, about half a minute,
then the board answers at `fishball.local`.

![The PlutoSky R2's three sockets and where each goes. ETH goes to your router, which hands out the address; from your PC, ssh root@fishball.local. DEBUG goes to USB power and is also the serial console. USB2.0 goes to USB power as the second socket. Connect both USB-C sockets: one alone can be short of power. The BOOT switch is set to SD.](../img/start-connect-light.svg#only-light)
![The PlutoSky R2's three sockets and where each goes. ETH goes to your router, which hands out the address; from your PC, ssh root@fishball.local. DEBUG goes to USB power and is also the serial console. USB2.0 goes to USB power as the second socket. Connect both USB-C sockets: one alone can be short of power. The BOOT switch is set to SD.](../img/start-connect-dark.svg#only-dark)

<figure markdown>
![The PlutoSky R2 in its silver aluminium case, ports end: a small coaxial socket labelled 10M_IN, an RJ45 Ethernet jack, and two USB-C sockets labelled DEBUG and USB2.0; the JP5 header shows through a slot in the top of the case](../img/plutosky-r2-ports.jpg){ width="420" }
<figcaption>The ports end of the case. Photo: OpenSourceSDRLab.</figcaption>
</figure>


1. With the board unpowered, put the card in.
2. Set the **`BOOT`** switch to SD: both sliders away from `ON`. A wrong
   position is silent: nothing appears even on the serial console.
3. Connect Ethernet to your router.
4. Connect **both** USB-C sockets, `DEBUG` and `USB2.0`. The vendor's manual
   says one alone can be short of power.
5. Wait about half a minute. On the test board a login prompt was there 23 s
   after power-on.

![A two-slider DIP switch marked ON along one edge, with both sliders at the opposite edge: SD card boot, what this firmware boots from. Set it with the board off. A wrong position is silent: nothing appears, not even on the serial console.](../img/start-boot-switch-light.svg#only-light)
![A two-slider DIP switch marked ON along one edge, with both sliders at the opposite edge: SD card boot, what this firmware boots from. Set it with the board off. A wrong position is silent: nothing appears, not even on the serial console.](../img/start-boot-switch-dark.svg#only-dark)

*Step 2, as a drawing: it shows where the sliders go, not what the R2's
switch looks like.*

Then reach it:

| Route | Address | State on the R2 |
|---|---|---|
| **Ethernet** | your router hands it an address (DHCP), and it answers at `fishball.local` | works: 1 Gbit/s, ping both ways |
| **The serial console** on `DEBUG` | 115200 baud, the second of the two serial ports | works; the way in when the network is not up |
| **The USB network** on `USB2.0` | `192.168.2.1` | with release v0.1 the board enumerates; the address was not tried, because the test PC was a Mac and macOS has no RNDIS driver. With firmware from the next release, switched to `ncm`: works from a Mac |

```bash
# run from: your HOST
ssh root@fishball.local     # password: analog
```

From a clone of the repository, `./devkit net find` looks for the board
without knowing its address.

**You should see:** a login prompt over ssh. SDR software reaches the board at
`ip:fishball.local`.

!!! note "On a Mac, `192.168.2.1` does not answer by default"
    The board's USB network is RNDIS, and macOS has no driver for it. Use
    Ethernet (`ssh root@fishball.local`). With firmware from the next
    release the board can be switched to `ncm`, which was tested on an R2
    with a Mac:
    [reach the board over the USB cable](use-a-mac.md#reach-the-board-over-the-usb-cable).

??? question "Nothing answers?"
    - Open the serial console on `DEBUG` and power-cycle. No text at all: check
      the `BOOT` switch and that the card is seated.
    - Text, then a freeze or a restart: connect the second USB-C socket.
    - A login prompt on the console but no address: `ip addr show eth0` there.
      The kernel prints `unable to generate target frequency: 125000000 Hz`
      when the link comes up; on the test board the link worked regardless.
    - Then see [troubleshooting](../troubleshooting.md) and the
      [networking reference](../networking.md), both written for the R1.

!!! warning "Do not send a serial BREAK to the console"
    On the test board it flooded the console with NUL bytes until a power
    cycle.

**Next:** [check what it runs](check-the-firmware.md).
