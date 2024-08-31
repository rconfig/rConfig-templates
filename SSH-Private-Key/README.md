This is an example for connecting to devices with rConfig V7 Professional with SSH private keys

## Key Configuration Options

### `sshPrivKey`

- This parameter specifies the path to the SSH private key used for authentication when connecting to remote devices.
- The SSH key must be configured correctly within the Device Credentials feature of `rConfig V7 Pro+` to ensure seamless and secure connectivity.
- It is crucial that the private key is stored securely and adheres to best practices for key management, including the use of passphrases and proper file permissions.

### `Ansihost`

- This option defines the host or list of hosts that the configuration will target.
- It supports a variety of SSH-compatible devices, enabling flexible and scalable management across different network environments.
- The `Ansihost` parameter is essential for directing the automation tasks to the correct remote systems, ensuring accurate and efficient execution of commands and scripts.
 - The setTerminalDimensions might need adjustment depending on the size of files being backed up. 
---

| Filename        | Usage and testing notes     |
|-------------|----- |
|  ssh_priv_key_template.yml    | Tested with native linux such as Rocky 9 and Ubuntu   |
 

This configuration file plays a crucial role in the secure and efficient operation of `rConfig`'s device management capabilities, leveraging SSH for robust and reliable connectivity. Proper setup and adherence to the guidelines above will ensure that `rConfig V7 Pro+` functions optimally, maintaining the security and integrity of your network management tasks.
