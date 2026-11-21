---
name: Hardware mismatch / doesn't boot on my board
about: The build completes, but the board doesn't behave like the docs describe
title: ""
labels: hardware
---

**Which board** (this repository is for the PlutoSky R2, XC7Z020-CLG484; say
how you know yours is one, and which variant: AD9361 or AD9363, with or without
a power amplifier. A PlutoSky R1 belongs in the other repository):

**What you built and how it got onto the board** (the commit, the timing
summary of the FPGA build, and: a whole card with `write-card`, files copied
from a card reader, or `./devkit flash`):

**Serial console output** (a full boot log is the most useful thing you
can attach: the `DEBUG` socket, 115200 baud, the second of its two serial
ports; `screen -L /dev/ttyUSB1 115200` captures it):

**What you expected vs. what actually happened:**
