# SSH private key authentication

| File | What it is |
| --- | --- |
| `ssh-private-key-template.yml` | An ordinary SSH connection template with private key authentication switched on |

## sshPrivKey is a flag, not the key

`auth.sshPrivKey` is a switch. It carries no key material and no path to a key file.

When it is set to a truthy value, rConfig authenticates with a private key instead of a password.
The actual key and its passphrase are read from the **Device Credentials record attached to the
device** in rConfig, not from the template. A template never contains key bytes, and should never
be edited to try to hold them.

Set up the credential record first, attach it to the device, then assign this template.

## Support position

Private key authentication is **supported on rConfig Pro**. The code that reads `auth.sshPrivKey`
is also present in Core, but the capability is not supported there. That is a support position
rather than a code gate: it may appear to work on Core and is still not supported. See
[docs/EDITIONS.md](../../docs/EDITIONS.md).

## Otherwise a normal SSH template

Apart from the one flag, this is a standard `protocol: ssh` template and every usual key applies:
prompts, enable mode, paging commands, and the `options` block for ANSI terminal handling.

Two notes on the values shipped here:

- `options.AnsiHost` is set to `yes`, which selects the ANSI read path. It has nothing to do with
  choosing which hosts to target; it controls how output is decoded.
- `options.setTerminalDimensions` may need raising for devices with large configurations. It
  affects ANSI post-processing only.

Private key sessions take the ANSI read path, so those two options matter more here than on a
plain password template.

See [docs/TEMPLATES.md](../../docs/TEMPLATES.md) for the full key reference.
