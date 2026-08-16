# A10

Covers A10 Thunder appliances running ACOS.

| Template | Use for |
| --- | --- |
| `a10-acos-ssh-enable.yml` | ACOS devices where the account needs enable mode |

Typical retrieval command to attach in an rConfig Command Group:

```text
show running-config
```

These templates are untested starters. If you run one against real hardware, please file a
[template test report](https://github.com/rconfig/rConfig-templates/issues/new?template=template-test-report.yml) so it can be promoted to community-tested.

See [docs/TEMPLATES.md](../docs/TEMPLATES.md) for what each key means and
[docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) before submitting a change.
