# NVIDIA

Covers NVIDIA Networking switches. Mellanox was acquired by NVIDIA and the product line has been
NVIDIA Networking since 2020, which is why these templates live here rather than under a Mellanox
directory.

| Template | Use for |
| --- | --- |
| `nvidia-onyx-ssh-enable.yml` | Ethernet switches running Onyx. This is the former Mellanox template |
| `nvidia-mlnxos-ssh-enable.yml` | Quantum InfiniBand switches running MLNX-OS |

Typical retrieval command to attach in an rConfig Command Group:

```text
show running-config
```

The Onyx template keeps `(Mellanox)` in its display name so the old brand stays searchable for
anyone who knows the hardware by its previous name.

Two device side notes, both already recorded in the templates themselves:

- Onyx: set `no cli default paging enable` in the switch running configuration. rConfig does not
  drive the Onyx paging system.
- MLNX-OS: if captures come back partial or truncated, try configuring an incorrect prompt on the
  device record in rConfig. That sounds wrong but it is the workaround that produces complete
  output on these switches.

See [docs/TEMPLATES.md](../docs/TEMPLATES.md) for what each key means and
[docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) before submitting a change.
