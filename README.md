<a name="readme-top"></a>
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/rconfig/rconfig">
    <img src="https://portal.rconfig.com/images/rconfig-logos/rConfig-logo-and-icon/rconfig_logo_and_icon_with_strapline_gradient.png" alt="rConfig Logo" width="500"/>
  </a>

  <h3 align="center">rConfig - Templates</h3>

  <!-- Shields.io badge -->
  <p align="center">
    <img src="https://img.shields.io/badge/vendors-+25-blueviolet?style=for-the-badge&logo=yaml&logoColor=white" alt="Vendors Badge"/>
  </p>

  <p align="center">
    This repository stores community-submitted connection templates for use with <a href="https://www.rconfig.com">rConfig</a>, including templates for SSH, Telnet, and Script-based device integrations.
  </p>
</div>
<br>

<br>

### 🔗 Docs & Contribution
- 📚 Documentation: [Script Integration Engine (SIE)](https://docs.rconfig.com/integrations/script-integration-engine/sie/)
- 🤝 Submit or browse templates: [rConfig-templates GitHub](https://github.com/rconfig/rConfig-templates)

<br>

## File Structure & Naming Convention

Each template must reside in a directory named after the device vendor:

```
/cisco/cisco-ios-ssh-enable.yml
/hp/hp-procurve-telnet-noenable.yml
```

**File naming format**:
```text
vendorName-modelName-connectionType-enableMode.yml
```
**Example**:
```text
cisco-ios-ssh-enable.yml
hp-1920-telnet-noenable.yml
```

---

## YAML Structure & Descriptors

Each template **must** start with the following docblock:
```yaml
# rConfig connection template – DO NOT EDIT DIRECTLY
## Template Notes:
## - All free text values must be wrapped in double quotes: " "
## - Documentation: https://docs.rconfig.com/integrations/script-integration-engine/sie/
## - Community templates and contributions: https://github.com/rconfig/rConfig-templates
```

---

### `main:`  
Defines the template's label and a brief description.
```yaml
main:
  name: "Cisco IOS - SSH - Enable"
  desc: "Cisco IOS SSH based connection with enable mode"
```

---

### `connect:`  
Defines how rConfig connects to the device.
```yaml
connect:
  timeout: 60          # Seconds until connection timeout
  protocol: ssh        # Protocol (ssh | telnet | script)
  port: 22             # Port number (1-65535)
  isNonInteractiveMode: true  # (Optional) Set true for non-interactive SSH
```

---

### `auth:`  
Defines authentication and optional elevation behavior.
```yaml
auth:
  username: "Username:"             # Username prompt
  password: "Password:"             # Password prompt
  enable: on                        # Enable mode: on | off
  enableCmd: "enable"               # Command to enter enable mode
  enablePassPrmpt: "Password:"      # Enable password prompt
  hpAnyKeyStatus: off               # Required for some HP devices
  hpAnyKeyPrmpt: "Press any key to continue"  # 'Press any key' prompt
```

---

### `config:`  
Commands related to paging, prompt handling, and session control.
```yaml
config:
  linebreak: "n"                      # Command linebreak type: 'n' or 'r'
  paging: on                          # Disable device paging: on | off
  pagingCmd: "terminal length 0"      # Command to disable paging
  resetPagingCmd: "terminal length 40"  # Command to re-enable paging
  pagerPrompt: ""                     # Pager prompt (leave blank if not needed)
  pagerPromptCmd: ""                  # Keystroke to clear pager (leave blank if not needed)
  saveConfig: "wr mem"                # Save config command
  exitCmd: "quit"                     # Exit session command
```

---

### `options:` (Optional)  
Advanced settings, used primarily for legacy or VT100-based terminal environments.
```yaml
options:
  AnsiHost: "yes"                       # Enable ANSI support for VT100 sessions
  setWindowSize: [240, 2048]           # Terminal width and height
  setTerminalDimensions: [260, 1000]   # ANSI screen dimensions
```

---

## ✅ Submission Guidelines

- ✅ Use consistent spacing and quotes for all free text fields.
- ✅ Remove `pagerPrompt` and `pagerPromptCmd` if not required.
- ❌ Do **not** include unused or commented-out keys.
- ✅ Test templates before submitting.


Thanks for helping grow the rConfig community! If you have questions or suggestions, feel free to [open an issue](https://github.com/rconfig/rConfig-templates/issues) or [join the discussion](https://rconfig.com/community/).


Let me know if you'd like this in a `.md` file or if you're ready to update template validation scripts or directory structure too.
