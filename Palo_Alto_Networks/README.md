
# Palo Alto Networks Support

Some Palo Alto devices require some special configurations to work with rConfig.

NOTE: If there are any issues downloading from Palo Altos using this template (such as partial configs) try removing the entire 'Options:' section from the template. 

Some commands issued to a terminal may yield ANSI escape codes. eg. ^[[K. These provide the terminal with information on the formating of the characters and their positioning.
Set connection to use ANSI decoded for older VT100 term emulator based consoles such as HP switches.
```sh
    # Set SSH connection to set AnsiHost connection for VT100 type connections
    AnsiHost: "yes"
```

Sets the number of columns and rows for the terminal window size. setTerminalDimensions(int $columns = 260, int $rows = 1000)
```sh
    # Sets the number of columns and rows for the terminal window size
    setTerminalDimensions: [260, 1000]
```

> panos-ssh-9x.yml - Fully tested and supported on rConfig v6

For Palo Altos with very large configurations, you may need to increase the setTerminalDimensions 2nd value from 1000, to a value that represents the number of lines. We have seen increases up to 50000. If this value does need to be increased, you may need to increase the PHP server memory limit also to cope with the large downloads. 

The default memory limit is 256M, which is usually more than sufficient for most needs. If you need to raise this limit, you must edit the /etc/php.ini file. 
Find and update the following line. There are no hard recommendations, but if you have a server with 4GB of RAM, this can safely be increase to 2 (2048MB) or 3 GB (3072MB). If in doubt, contact rConfig support if you have a valid support agreement.

```bash
memory_limit = 256M
```

Essentially, the best practice for v6 users is to use the attached SSH templates and enable your firewalls for SSH also. 

Other PA implementations require a special login sequence so an edit to the connection template enableCmd parameter is required. instead of the follow sequence, 
```bash
  enable: off
  # set enable mode command. Must be in quotes
  enableCmd: "enable"
```

You may need to adjust this to
```bash
  # Set enable mode on or off
  enable: on
  # set enable mode command. Must be in quotes
  enableCmd: "set cli config-output-format set\nset cli pager off"
...
    paging: off
```

These approaches are fully tested and supported on rConfig v6.
