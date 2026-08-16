# Opengear

Covers Opengear console servers.

| Template | Use for |
| --- | --- |
| `opengear-ssh-noenable.yml` | Opengear devices reached over SSH |

Typical retrieval command to attach in an rConfig Command Group, depending on the platform:

```text
Classic firmware:  config -g config
NGCS firmware:     ogcli export
```

Opengear presents a Linux shell rather than a network CLI. There is no enable mode, no pager to
disable, and no configuration save step, so the template leaves all three empty.

These templates are untested starters. If you run one against real hardware, please file a
[template test report](https://github.com/rconfig/rConfig-templates/issues/new?template=template-test-report.yml) so it can be promoted to community-tested.

See [docs/TEMPLATES.md](../docs/TEMPLATES.md) for what each key means and
[docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) before submitting a change.
