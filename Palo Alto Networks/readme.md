
# Palo Alto Networks Support

Some Palo Alto devices require some special configurations to work with rConfig.

Some commands issued to a terminal may yield ANSI escape codes. eg. ^[[K. These provide the terminal with information on the formating of the characters and their positioning.
Set connection to use ANSI decoded for older VT100 term emulator based consoles such as HP switches.
```sh
    # Set SSH connection to set AnsiHost connection for VT100 type connections
    AnsiHost: "yes"
```

Sets the number of columns and rows for the terminal window size. setWindowSize(int $columns = 80, int $rows = 24)
```sh
    # Sets the number of columns and rows for the terminal window size
    setWindowSize: [240, 2048]
```

> panos-ssh-9x.yml - Fully tested and supported on rConfig v5

Essentially, the best practice for V5 users is to use the attached SSH templates and enable your firewalls for SSH also. This protocol is fully tested and support on rConfig v5
