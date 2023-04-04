
# Mikrotik Support

Mikrotik devices require some special configurations to work with rConfig.

1. The device username must have '+cte' appended to it i.e. ```admin+cte```. This is in all cases. See vendor information here [https://wiki.mikrotik.com/wiki/Manual:Console_login_process#Console_login_options](https://wiki.mikrotik.com/wiki/Manual:Console_login_process#Console_login_options)
2. The template, per example in this repo, must have the command per below in the Config section.

Some commands issued to a terminal may yield ANSI escape codes. eg. ^[[H. These provide the terminal with information on the formating of the characters and their positioning.
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

> mikrotek-ssh-noenable.yml - Fully tested and supported on rConfig v6

Essentially, the best practice for v6 users is to use the SSH template and enable your switches for SSH also. This protocol is fully tested and support on rConfig v6
