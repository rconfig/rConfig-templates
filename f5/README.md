# F5

Covers F5 BIG-IP running TMOS.

| Template | Use for |
| --- | --- |
| `f5-tmos-ssh-noenable.yml` | BIG-IP devices reached over SSH into tmsh |

Typical retrieval command to attach in an rConfig Command Group:

```text
show running-config
```

That command runs inside tmsh and captures the running configuration as text. A full UCS archive
is a file transfer job, not a CLI capture, so it is out of scope for a connection template.

The login account must land in tmsh, not bash. Set the user shell to tmsh on the BIG-IP,
otherwise the paging and save commands in the template are sent to a bash prompt.

These templates are untested starters. If you run one against real hardware, please file a
[template test report](https://github.com/rconfig/rConfig-templates/issues/new?template=template-test-report.yml) so it can be promoted to community-tested.

See [docs/TEMPLATES.md](../docs/TEMPLATES.md) for what each key means and
[docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) before submitting a change.
