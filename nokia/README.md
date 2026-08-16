# Nokia

Covers Nokia SR OS routers. SR OS ships two command line interfaces and they are not
interchangeable, so pick the template that matches the node.

| Template | Use for |
| --- | --- |
| `nokia-sros-classic-ssh-noenable.yml` | Nodes running the Classic CLI |
| `nokia-sros-md-ssh-noenable.yml` | Nodes running MD-CLI |

Typical retrieval command to attach in an rConfig Command Group:

```text
Classic CLI:  admin display-config
MD-CLI:       admin show configuration
```

The paging syntax differs between the two as well, which is why there are two templates rather
than one. Each template names the other in its header comments.

These templates are untested starters. If you run one against real hardware, please file a
[template test report](https://github.com/rconfig/rConfig-templates/issues/new?template=template-test-report.yml) so it can be promoted to community-tested.

See [docs/TEMPLATES.md](../docs/TEMPLATES.md) for what each key means and
[docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) before submitting a change.
