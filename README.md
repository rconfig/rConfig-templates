
# rConfig-templates

## Overview
A repo to store community submitted connection templates for rConfig

File format should be as follows;
> Dell / dell-6248-telnet-enable.yml

All templates to be stored in individual vendor named directorys 

File names are;
*vendorName-ModelNumber-ConnectionType-isEnableModeOrNot.yml*
i.e. 
> dell-6248-telnet-enable.yml



## Yaml Decsriptors

Always read the notes section at the top of each template, as there maybe specific options or device setup instructions not required in other templates.
```sh
# rConfig connection template - DO NOT EDIT DIRECTLY
## Notes: 
    ## Remember to update permissions for the templates folder after uploading new template files.
    ## run 'chown -R apache /home/rconfig' on your rconfig server CLI
    ## all items below that contain free text should be contained within quotation marks " "
    ## For new community submitted templates visit: https://github.com/rconfig/rConfig-templates
```

### Options - main: 
Simple name and description for the template. If submitting templates to rconfig git repo, please follow naming convention below for *name:* option
```sh
  name: "Cisco IOS - SSH - Enable"
  desc: "Cisco IOS SSH based connection with enable mode"
```

### Options - connect: 
Section for connection options to devices

Specifies time in seconds before rConfig will forceably terminate a connection to a device if no data returned from device
```sh
  # connection timeout in seconds
  timeout: 60
```

Specify *telnet* or *ssh* type connection. Must be in lowercase
```sh
  # type either telnet or ssh - must be in lowercase
  protocol: ssh
```

Specify port number for telnet or ssh connections. Range is form 1 to 65535
```sh
  # type port number for connection protocol choose from 1 - 65535
  port: 22
```

### Options - auth: 
Section for authentication options to devices.

Set case sensitive *usename* prompt for device authentication. If left blank, *usename* will not be sent.
```sh
  # Set username name prompt. Must be in quotes. If left blank, username will not be sent.
  username: "Username:"
```

Set case sensitive *password* prompt for device authentication. If left blank, *password* will not be sent.
```sh
  # Set password name prompt. Must be in quotes
  password: "Password:"
```

If your authentication requires enable or elevated mode to run required commands, set this option to on. Do not use quotes for this option. Options are *on* or *off*
```sh
  # Set enable mode on or off
  enable: off
```

If your authentication requires enable or elevated mode to run required commands, set this option to required command. Make sure your text is wrapped in double quotes.
```sh
  # set enable mode command. Must be in quotes
  enableCmd: "enable"
```

Set case sensitive enable *password* prompt for device authentication. If left blank, enable *password* will not be sent.
```sh
  # set enable mode password prompt. Must be in quotes
  enablePassPrmpt: "Password:"
```

This option is very specific to certain HP devices where *press any key* is a required part of the login process. Do not use quotes for this option. Options are *on* or *off*
```sh
  # set HP 'press any key' status. Is 'on' or 'off'
  hpAnyKeyStatus: off
```

If the previous HP option is set to on, enter the case sensitive *any key* prompt here.
```sh
  # set HP 'press any key' prompt. 
  hpAnyKeyPrmpt: "Press any key to continue"  
```
### Options - config: 
Section for configuration options to devices.

Option specifies line break or carriage return for scripts when send commands to devices. Vast majority will be set to *"n"*. In some cases, such as Mikrotek, there CLIs require carriage returns to invoke a command *"r"*. [EXPERIMENTAL]
```sh
	# Carriage return or NewLine for commands. i.e. MikroTek ssh requires \r. Options: 'r' or 'n' (may use rn in future if required)
    linebreak: "n"
```
Set to disable paging for devices. Do not use quotes for this option. Options are *on* or *off*
```sh
   # Disable config scrolling/ paging command. on/off
    paging: on
```

Actual command to disable paging on the device. Some devices use multiple commands for this, and line breaks may work. i.e. *"conf t\n disable paging\end"*
```sh
    # Disable config scrolling/ paging command. Leave blank, or set as required. Must place command in quotations
    pagingCmd: "terminal length 0"
```

Actual command to re-enable paging on the device. Some devices use multiple commands for this, and line breaks may work. i.e. *"conf t\n enable paging\end"*
```sh
    # re-enable config scrolling/ paging command. Leave blank, or set as required. Must place command in quotations
    resetPagingCmd: "terminal length 40"
```

Some devices have a requirement for press space, or other key to continue paging. Copy exact text from your devices console when asked to page within the quotes on this option.
```sh
    # Set pager prompt. Must place command in quotations
    pagerPrompt: "--More--"
```

Coupled with the previous option, this option sets the actual text or command to type if the output returned to rConfig matches the prompt previously specified. i.e. If rConfig sees a *--More--" prompt, you will want to send space for Cisco devices, enter a *space* or multiple spaces between the double quotes for this option.
```sh
    # Set pager prompt key-stroke. Must place command in quotations
    pagerPromptCmd: " "
```

Set the command to save the running config. If blank, command will not be sent.
```sh
    # Save configuration command. Leave blank, or set as required. Must be in quotes
    saveConfig: "wr mem"
```

Set the command to exit the interactive etlnet or SSH session fro the device. If not set, you may risk leaving open sessions on your devices thus causing lockout in the future. 
```sh
    # Set exit command. Must place command in quotations
    exitCmd: "quit"
```
