
# HP Procurve Switch Support

There are known problems with scripts and automation software connecting to HP Procurve Switches due to their implementation of VT100 terminal characters in their software.

> hp-procurve-ssh-noenable.yml - Fully tested and supported on rConfig v6, should work on v3

> hp-procurve-ssh-noenable-nopage.yml - NOT supported on rConfig v6, should work on v3

> hp-procurve-telnet-noenable.yml - NOT supported on rConfig v6, should work on v3

Essentially, the best practice for v6 users is to use the SSH template and enable your switches for SSH also. This protocol is fully tested and support on rConfig v6

## Which ProCurve template to use

`hp-procurve-ssh-noenable.yml` is the standard choice. Start here.

Its `pagingCmd` value is `"nno page"`. The doubled letter is DELIBERATE. Some HPE firmware
swallows the first character sent after the any-key prompt, so the extra letter is
sacrificial and the switch receives `no page` as intended. Do not correct it.

`hp-procurve-ssh-noenable-nopage.yml` sends the plain `no page` command instead, for
firmware without the quirk. Switch to it if you see an `Invalid input: nno` style error in
the session logs.

## HP Comware templates

Comware based HP switches, including devices branded H3C, use the templates below.

> hp-comware-ssh-noenable.yml - Comware devices, also covers H3C branded hardware

> hp-comware-ssh-noenable-flexfabric.yml - FlexFabric switches

> hp-comware-ssh-noenable-nosystemview.yml - A5120, connects without entering system-view

> hp-comware-5400xl-ssh-noenable.yml - 5400xl, handles the enable username prompt

> hp-1920-ssh-enable.yml - 1920, which needs a special elevation command other HP switches do not
