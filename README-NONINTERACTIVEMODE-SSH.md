Sure thing! Here’s the content converted to GitHub-styled markdown:

---

# rConfig: SSH Non-Interactive Shell for Configuration Retrieval

## Overview

As of the update (Date: 21/11/2024), a new SSH non-interactive mode has been introduced in rConfig, designed to streamline the process of retrieving configurations from devices. This feature is now available in the following versions:

- **rConfig V6 Core** (installed or updated after 21/11/2024)
- **rConfig V7 (7.2.9) and beyond**

The new template flag, called **NonInteractive**, is available to be used across supported versions of rConfig. This feature enables the use of a non-interactive type SSH shell, which enhances efficiency when retrieving configurations, particularly in scenarios where manual input prompts are undesirable or unfeasible.

## How to Use the Non-Interactive Shell

The new non-interactive shell mode can be configured in the rConfig configuration file by setting the `isNonInteractiveMode` flag. By default, this flag is set to `false` or is not required at all, but users can enable or disable the feature as required.

### Configuration Example

```yaml
# Set SSH non-interactive mode on or off
isNonInteractiveMode: true
```

- `true` (without quotes): Enables non-interactive mode for SSH connections.
- `false` (without quotes): Disables non-interactive mode, defaulting back to interactive connections.

To enable or disable the non-interactive mode, simply modify the value of `isNonInteractiveMode` to `true` or `false`, and save the configuration file. Ensure the values are specified **without quotes** to avoid parsing errors.

See example here [https://github.com/rconfig/rConfig-templates/blob/master/Fortinet/fortigate-ssh-noenable-noninteractive.yml](https://github.com/rconfig/rConfig-templates/blob/master/Fortinet/fortigate-ssh-noenable-noninteractive.yml)

Mikrotiks, Fortinets and some Ciscos have been tested. Please feedback on your tests. 

## Benefits of Using SSH Non-Interactive Mode

- **Improved Automation**: Non-interactive mode allows the SSH client to automatically manage connections without expecting user intervention. This is particularly beneficial when running scheduled or automated configuration retrievals, minimizing manual overhead.

- **Reduced Complexity**: For routine configuration retrieval, non-interactive mode simplifies the process, making it more predictable and easier to script. This makes rConfig an even more powerful tool for handling large-scale networks with frequent config changes.

- **Faster Config Retrieval**: By removing the need for prompts during SSH sessions, non-interactive mode can speed up the process of retrieving configurations from multiple devices, which is ideal for larger networks.

## Compatibility and Future-Proofing

While non-interactive mode is preferred for retrieving device configurations efficiently, users may still need to configure the device in both versions of rConfig (Core and Pro). This ensures compatibility for future use cases, such as sending configuration snippets or managing more interactive workflows that require user confirmation.

In these cases, configuring devices with both interactive and non-interactive capabilities guarantees greater flexibility, particularly when network environments or requirements evolve over time.

## Setting Up Non-Interactive Mode

1. **Edit Configuration**: Locate the configuration file for your version of rConfig, and find the entry for `isNonInteractiveMode`.
2. **Set the Flag**: Update the value to `true` or `false` depending on your requirements. Remember, there should be no quotes around `true` or `false`.
3. **Save Changes**: Save the configuration file and restart rConfig if necessary for the changes to take effect.

### Example

```yaml
isNonInteractiveMode: false
```

This line in the configuration will disable non-interactive mode, keeping the default interactive SSH shell behavior.

## Conclusion

The introduction of SSH non-interactive mode in rConfig adds significant flexibility and efficiency for configuration retrieval. By enabling automated, streamlined SSH sessions, this feature empowers network administrators to manage configurations more effectively across a large array of devices. For those looking to send configuration snippets in the future, maintaining the ability to configure devices in both interactive and non-interactive modes ensures adaptability as network management needs evolve.

--- 

Let me know if you need any tweaks or if there's anything else I can help with! 😊