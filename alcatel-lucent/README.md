# Alcatel-Lucent

Covers Alcatel-Lucent Enterprise switches running AOS.

| Template | Use for |
| --- | --- |
| `alcatel-lucent-aos-ssh-noenable.yml` | AOS devices reached over SSH |

Typical retrieval command to attach in an rConfig Command Group:

```text
show configuration snapshot
```

AOS has no CLI pager by default, so the template leaves paging off and the paging commands empty.

These templates are untested starters. If you run one against real hardware, please file a
[template test report](https://github.com/rconfig/rConfig-templates/issues/new?template=template-test-report.yml) so it can be promoted to community-tested.

See [docs/TEMPLATES.md](../docs/TEMPLATES.md) for what each key means and
[docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) before submitting a change.
