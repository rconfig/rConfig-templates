
# HP Procurve Switch Support

There are known problems with scripts and automation software connecting to HP Procurve Switches due to their implementation of VT100 terminal characters in their software.

> hp-procurve-ssh-noenable-v2.yml - Fully tested and supported on rConfig v6, should work on v3

> hp-procurve-ssh-noenable.yml - NOT supported on rConfig v6, should work on v3

> hp-procurve-telnet-noenable.yml - NOT supported on rConfig v6, should work on v3

Essentially, the best practice for v6 users is to use the SSH template and enable your switches for SSH also. This protocol is fully tested and support on rConfig v6
