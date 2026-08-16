# Arista

Covers Arista EOS switches.

| Template | Use for |
| --- | --- |
| `arista-eos-ssh-enable.yml` | EOS devices where the account needs enable mode |
| `arista-eos-ssh-noenable.yml` | EOS devices where the account is already privileged |

Typical retrieval command to attach in an rConfig Command Group:

```text
show running-config
```

These templates are untested starters. If you run one against real hardware, please file a
test report via the repository's issue templates so it can be promoted to community-tested.

See [docs/TEMPLATES.md](../docs/TEMPLATES.md) for what each key means and
[docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) before submitting a change.
