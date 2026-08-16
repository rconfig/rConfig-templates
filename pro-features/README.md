# Pro features

Everything in this directory requires rConfig Pro. Templates in the vendor directories at the
repository root run on both Core and Pro.

| Directory | Feature | What it does |
| --- | --- | --- |
| [sie/](sie/) | Script Integration Engine | Runs an external script instead of opening a CLI session, for devices with no usable CLI or where retrieval needs logic a connection template cannot express. See [sie/workflows/](sie/workflows/) for worked examples |
| [ssh-private-key/](ssh-private-key/) | SSH private key authentication | Authenticates with a key from the device credential record rather than a password |
| [xftp/](xftp/) | Inbound-only devices | Marks a device that pushes its configuration into rConfig. rConfig never connects out to it |

One Pro capability does not live here. **TL1 templates are Pro only but sit in
[ciena/](../ciena/)**, because they are Ciena device templates and belong with their vendor. The
protocol is Pro; the directory placement follows the hardware.

For the full Core and Pro breakdown, including which individual template keys each edition reads,
see [docs/EDITIONS.md](../docs/EDITIONS.md).
