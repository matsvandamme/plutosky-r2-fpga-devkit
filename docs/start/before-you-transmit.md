---
icon: material/alert-octagon-outline
description: The R2 transmits at low power, tested; its full power is unmeasured. Four rules that keep the receiver and the bench intact.
---

# Before you transmit

!!! danger "The R2's transmit power has not been measured"
    One R2 has transmitted with this firmware, on 2026-11-21, on both channels,
    always through attenuators and never above 30 dB of attenuation setting.
    At that level everything behaved: clean tones, a linear attenuator, and a
    transmitter that mutes when its program stops, is killed or stops sending.
    What nobody has measured is how much power it puts out. The loopback
    showed about 7.5 dB more gain than the same test expects on an R1, so the
    R1's numbers on this page may be too low for the R2. Raise power in steps,
    into an attenuator, watching the receiver's level.

On the R1, with its power amplifier: about **+19 dBm** out, against a receiver
that survives **+2.5 dBm**. The R2 is sold with and without an amplifier.

![Two rows. With the attenuator: TX1, whose power is not measured, goes through an attenuator of 20 dB, better 30, so that much less reaches RX1, whose limit is about +2.5 dBm. Without it: everything the transmitter puts out goes straight into RX1, which can be destroyed.](../img/start-attenuator-light.svg#only-light)
![Two rows. With the attenuator: TX1, whose power is not measured, goes through an attenuator of 20 dB, better 30, so that much less reaches RX1, whose limit is about +2.5 dBm. Without it: everything the transmitter puts out goes straight into RX1, which can be destroyed.](../img/start-attenuator-dark.svg#only-dark)

*No level is drawn for the transmitter because nobody has measured the R2's. The receiver's limit is the AD9361's, as on the R1; 20 dB is the R1's minimum, and the R2 may need more. It was tested through 30 dB on one channel and 20 dB on the other, at low power.*

| Rule | |
|---|---|
| **1. Put at least 20 dB of attenuation in any TX→RX loop** | without it, a transmitter with an amplifier destroys its own receiver |
| **2. Terminate every transmit port**, or leave it unused | never transmit at power into an open port |
| **3. No antenna on a transmit port you do not want radiating at power-on** | on the R1 every power-on emits a ~4 ms burst on both transmit ports, before any software runs. Not measured on the R2 |
| **4. Affirm the channel before raising it** | `./devkit tx-guard affirm 0` for TX1, `1` for TX2, after looking at that port |

```bash
# run from: the repo root
./devkit tx-guard affirm 0        # only after LOOKING at the TX1 port
./devkit tx-guard revoke both     # withdraw, and force maximum attenuation
```

What carries over by construction: the R2's device tree inherits the R1's
transmit attenuation default (89.75 dB, the muted state), and CI checks the
built tree for it. On the board, both channels read 89.75 dB after boot. The
power-on burst the R1 emits (rule 3) has not been looked for on the R2.

Writing your own transmit code? Two more rules apply: set the attenuation
**after** the buffer starts and read it back, and mute **before** tearing the
buffer down. Why, with the R1's measurements:
[transmitter safety reference](../transmitter-safety.md).

**Next:** use the radio: [capture IQ](../capturing-iq.md) or [SDR++](../sdrpp.md).
