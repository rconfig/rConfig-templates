
# Mikrotik Support

Mikrotik devices require some special configurations to work with rConfig.

1. The device username must have '+cte' appended to it i.e. ```admin+cte```. This is in all cases.
2. The template, per example in this repo, must have the command per below in the Config section.

```
config:
    # AnsiHost required in special cases for HP and Mikrotik devices. Consult rConfig support team for more information
    AnsiHost: "yes"
```

> mikrotek-ssh-noenable.yml - Fully tested and supported on rConfig v5

Essentially, the best practice for V5 users is to use the SSH template and enable your switches for SSH also. This protocol is fully tested and support on rConfig v5
