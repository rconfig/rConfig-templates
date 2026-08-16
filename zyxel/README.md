# Zyxel

Covers Zyxel switches with the Cisco-like CLI, which means the XGS range, the GS2xxx range and
above.

| Template | Use for |
| --- | --- |
| `zyxel-ssh-enable.yml` | Zyxel devices with a full CLI, where the account needs enable mode |

Typical retrieval command to attach in an rConfig Command Group:

```text
show running-config
```

Restricted-CLI models such as the GS1900 cannot be used with a prompt driven template. Those
devices do not present a shell that rConfig can read to a prompt, so there is nothing a
connection template can do with them.

These templates are untested starters. If you run one against real hardware, please file a
test report via the repository's issue templates so it can be promoted to community-tested.

See [docs/TEMPLATES.md](../docs/TEMPLATES.md) for what each key means and
[docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) before submitting a change.
