---
icon: material/alert-octagon-outline
description: Transmit is untested on the R2. Four rules, written for the R1, that keep the receiver and the bench intact.
---

# Before you transmit

!!! danger "Transmit has not been tested on the R2"
    With this firmware, no R2 has transmitted, and nothing here has measured an
    R2's output power, its power-on behaviour, or whether the firmware's mute
    works on it. Every number on this page was measured on a PlutoSky **R1**.
    The rules still apply, because the radio chip and its receive limit are the
    same; treat the first transmission as an experiment, into a dummy load.

On the R1, with its power amplifier: about **+19 dBm** out, against a receiver
that survives **+2.5 dBm**. The R2 is sold with and without an amplifier.

![Two rows. With the attenuator: TX1A at about +19 dBm, through a 20 dB attenuator, reaches RX1A at about -1 dBm, under its +2.5 dBm limit. Without it: +19 dBm goes straight into RX1A, about 16 dB over the limit, and destroys it.](../img/start-loopback-light.svg#only-light)
![Two rows. With the attenuator: TX1A at about +19 dBm, through a 20 dB attenuator, reaches RX1A at about -1 dBm, under its +2.5 dBm limit. Without it: +19 dBm goes straight into RX1A, about 16 dB over the limit, and destroys it.](../img/start-loopback-dark.svg#only-dark)

*The R1's figures.*

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
built tree for it. What that does on the board has not been measured.

Writing your own transmit code? Two more rules apply: set the attenuation
**after** the buffer starts and read it back, and mute **before** tearing the
buffer down. Why, with the R1's measurements:
[transmitter safety reference](../transmitter-safety.md).

**Next:** use the radio: [capture IQ](../capturing-iq.md) or [SDR++](../sdrpp.md).
