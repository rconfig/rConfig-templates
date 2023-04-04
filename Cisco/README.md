# Cisco WLC Controllers
There are known problems with scripts and automation software connecting to Cisco WLC Controllers due to their implementation of SSH/ Telnet protocols in their software.

> You may only use the ciscowlc-ssh-noenable.yml template in this repository.

> You may only use SSH, please configure your devices accordingly.

> You may not run the 'shwo run-config' command, as it takes far to long to print out. You may use the 'show run-config commands' instead for running configuration

Essentially, the best practice for v6 users is to use the SSH template and enable your switches for SSH also. This protocol is fully tested and support on rConfig v6

Related Cisco WLC Information: [https://quickview.cloudapps.cisco.com/quickview/bug/CSCve45024](https://quickview.cloudapps.cisco.com/quickview/bug/CSCve45024)