
# Mikrotik Support

Mikrotik devices require some special configurations to work with rConfig due to the peculiar nature of their CLI implementation.

> mikrotek-ssh-noenable_v2.yml - Fully tested and supported on rConfig v6

1. The device username must have '+cte' appended to it i.e. ```admin+cte```. This is in all cases. See vendor information here [https://wiki.mikrotik.com/wiki/Manual:Console_login_process#Console_login_options](https://wiki.mikrotik.com/wiki/Manual:Console_login_process#Console_login_options)

2. The template, per example in this repo, must have the command per below in the Config section. Please use the updated *mikrotik-ssh-noenable_v2.yml* template first. This template has been validated in our lab. If this fails, fall back to the original template. 

3. When adding the device in rConfig, Core or Professional, please input a prompt in the 'Main Prompt' field, but this actually not used. Again, due to the peculiar nature of their CLI implementation, rConfig actually strips out the prompt. rConfig waits for the template timeout to send the next command to the device. 

4. The default timeout on the template is 10 seconds. This will be suitable for most deployments. You may need to adjust up for longer configs, or down if you want the download jobs to complete faster.

The specific command for Mikrotik devices, in the v2 template is below. 

```php
    # Set device type to Mikrotik for special download instructions
    isMikrotik: yes
```


Information below related to *mikrotik-ssh-noenable.yml* - which is not the preferred template for Mikrotik RouterOS based devices.

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
