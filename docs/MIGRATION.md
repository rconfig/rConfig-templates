# Migration map: 2026 restructure

The 2026 restructure was a clean cut. Directories and template files were renamed to a
single convention, and no redirect stubs were left behind. Any link, bookmark, script, or
device record that referenced an old path will not resolve.

This file is the lookup. Find the old path on the left, read the new path on the right.

The convention itself is recorded in CLAUDE.md under "Template file naming".

## Directory renames

| Old | New | Notes |
| --- | --- | --- |
| `Adtran/` | `adtran/` | |
| `Adva/` | `adva/` | |
| `Allied_Telesis/` | `allied-telesis/` | |
| `Aruba/` | `aruba/` | |
| `Audiocodes/` | `audiocodes/` | |
| `Avaya/` | `avaya/` | |
| `base/` | `_base/` | Underscore prefix sorts the starter template above the vendor listing. |
| `Brocade/` | `brocade/` | |
| `Calix/` | `calix/` | |
| `Checkpoint/` | `checkpoint/` | |
| `Ciena/` | `ciena/` | |
| `Cisco/` | `cisco/` | |
| `Dell/` | `dell/` | |
| `DiGi/` | `digi/` | |
| `Edge-core/` | `edgecore/` | Edgecore Networks is one word. |
| `Extreme/` | `extreme/` | |
| `Fortinet/` | `fortinet/` | |
| `HP/` | `hp/` | |
| `Juniper/` | `juniper/` | |
| `Mellanox/` | `nvidia/` | MERGED. Mellanox is NVIDIA Networking. The directory no longer exists. |
| `Mikrotik/` | `mikrotik/` | |
| `Palo_Alto_Networks/` | `palo-alto/` | |
| `pfSense/` | `pfsense/` | |
| `RAD/` | `rad/` | |
| `Ruckus/` | `ruckus/` | |
| `Sonicwall/` | `sonicwall/` | |
| `Ubiquiti/` | `ubiquiti/` | |

Unchanged: `huawei/`, `linux/`, `nvidia/`, `siemens/`, `vyos/`.

Deferred to a later phase, still uppercase: `SIE-Base/`, `SIE-Radware/`, `SIE-Zyxel/`,
`SSH-Private-Key/`, `XFTP/`.

New: `docs/`.

### Cross directory moves

| Old | New | Notes |
| --- | --- | --- |
| `Mellanox/mellanox-ssh-enable.yml` | `nvidia/nvidia-onyx-ssh-enable.yml` | Whole directory merged into `nvidia/`. |
| `Aruba/HP-A5120-SSH-NoSystem-View.yml` | `hp/hp-comware-ssh-noenable-nosystemview.yml` | Misfiled. The A5120 is HP Comware, not Aruba. |

## Template renames

Every template below moved, was renamed, or both.

| Old path | New path | Notes |
| --- | --- | --- |
| `Adtran/Adtran900_telnet.yml` | `adtran/adtran-aos-telnet-enable.yml` |  |
| `Adva/adva-ssh-no_enable.yml` | `adva/adva-ssh-noenable.yml` |  |
| `Allied_Telesis/AlliedTelesis-SSH-Enable.yml` | `allied-telesis/allied-telesis-awplus-ssh-enable.yml` |  |
| `Aruba/Aruba-S3500-SSH-enable.yml` | `aruba/aruba-aos-ssh-enable.yml` |  |
| `Aruba/Aruba2930F-SSH-NoEnable.yml` | `aruba/aruba-aos-s-ssh-noenable.yml` |  |
| `Aruba/HP-A5120-SSH-NoSystem-View.yml` | `hp/hp-comware-ssh-noenable-nosystemview.yml` | Misfiled. The A5120 is HP Comware, not Aruba. Moved directory and renamed. |
| `Audiocodes/audiocodes.yml` | `audiocodes/audiocodes-mediant-ssh-noenable.yml` |  |
| `Avaya/avaya-4526gtx-telnet-noenable.yml` | `avaya/avaya-ers-telnet-noenable.yml` |  |
| `Avaya/avaya-swtich-vector-ssh.yml` | `avaya/avaya-ers-ssh-noenable-vector.yml` |  |
| `Brocade/brocade.yml` | `brocade/brocade-fastiron-ssh-noenable.yml` |  |
| `Calix/calix-axos-ssh-no_enable.yml` | `calix/calix-axos-ssh-noenable.yml` |  |
| `Checkpoint/CheckpointGaiaOS_NoEnable.yml` | `checkpoint/checkpoint-gaia-ssh-noenable.yml` |  |
| `Ciena/6500-TL1-telnet.yml` | `ciena/ciena-6500-tl1-telnet.yml` | TL1 has no enable concept, so authmode is omitted. Model retained. |
| `Ciena/6500-TL1.yml` | `ciena/ciena-6500-tl1-ssh.yml` | TL1 has no enable concept, so authmode is omitted. Model retained. |
| `Cisco/asa-ssh-enable.yml` | `cisco/cisco-asa-ssh-enable.yml` |  |
| `Cisco/cisco-smb-telnet-noenable.yml` | `cisco/cisco-smb-telnet-noenable.yml` |  |
| `Cisco/ciscowlc-ssh-noenable.yml` | `cisco/cisco-wlc-ssh-noenable.yml` |  |
| `Cisco/ios-ssh-enable.yml` | `cisco/cisco-ios-ssh-enable.yml` |  |
| `Cisco/ios-ssh-noenable.yml` | `cisco/cisco-ios-ssh-noenable.yml` |  |
| `Cisco/ios-telnet-enable-no-username.yml` | `cisco/cisco-ios-telnet-enable-nousername.yml` |  |
| `Cisco/ios-telnet-enable.yml` | `cisco/cisco-ios-telnet-enable.yml` |  |
| `Cisco/ios-telnet-noenable.yml` | `cisco/cisco-ios-telnet-noenable.yml` |  |
| `Dell/dell-5524-telnet-noenable.yml` | `dell/dell-powerconnect-telnet-noenable.yml` | Model collapse. 5524 folded into the PowerConnect family. |
| `Dell/dell-6248-telnet-enable.yml` | `dell/dell-powerconnect-telnet-enable.yml` | Model collapse. 6248P folded into the PowerConnect family. |
| `Dell/dell-s4048-ssh-noenable.yml` | `dell/dell-networking-ssh-noenable.yml` | Model collapse. S4048 is one of the Dell Networking family. Model recorded in the template description. |
| `DiGi/digi-ix20-ssh-noenable.yml` | `digi/digi-dal-ssh-noenable.yml` | Model collapse. IX20 folded into the Digi Accelerated Linux (DAL) family. |
| `Edge-core/edgecore-ssh-noenable.yml` | `edgecore/edgecore-ssh-noenable.yml` |  |
| `Extreme/extreme-summit-ssh-noenable.yml` | `extreme/extreme-exos-ssh-noenable.yml` | Summit is hardware. EXOS is the OS family the convention asks for. |
| `Fortinet/fortigate-ssh-noenable-banner_prompt.yml` | `fortinet/fortinet-fortios-ssh-noenable-banner.yml` |  |
| `Fortinet/fortigate-ssh-noenable-noninteractive.yml` | `fortinet/fortinet-fortios-ssh-noenable-noninteractive.yml` |  |
| `Fortinet/fortigate-ssh-non-vdom.yml` | `fortinet/fortinet-fortios-ssh-noenable.yml` |  |
| `Fortinet/fortigate-ssh-vdom.yml` | `fortinet/fortinet-fortios-ssh-noenable-vdom.yml` |  |
| `HP/H3C-ssh-noenable.yml` | `hp/hp-comware-ssh-noenable.yml` | H3C branded Comware hardware. Vendor prefix follows the directory. H3C is recorded in the description and in hp/README.md. |
| `HP/HP-1920-SSH-noenable-v2.yml` | `hp/hp-1920-ssh-enable.yml` | Name vs content. File said noenable, content is `enable: on`. Content wins. Model retained: the 1920 needs a special elevation command. |
| `HP/hp-5400-xl-ssh-enable.yml` | `hp/hp-comware-5400xl-ssh-noenable.yml` | Name vs content. File said enable, content is `enable: off`. Content wins. Content is Comware, not ProCurve. |
| `HP/hp-flexfabric-ssh-noenable.yml` | `hp/hp-comware-ssh-noenable-flexfabric.yml` | FlexFabric is Comware. Product name kept as the variant token. |
| `HP/hp-procurve-ssh-noenable-v2.yml` | `hp/hp-procurve-ssh-noenable.yml` | ProCurve swap. The former v2 is now the canonical ProCurve template. Its `nno page` doubled letter is deliberate. |
| `HP/hp-procurve-ssh-noenable.yml` | `hp/hp-procurve-ssh-noenable-nopage.yml` | ProCurve swap. The old canonical template lives on under the -nopage name. It sends the plain `no page` command. |
| `HP/hp-procurve-telnet-noenable.yml` | `hp/hp-procurve-telnet-noenable.yml` |  |
| `Juniper/JUNOS_SWITCHES.yml` | `juniper/juniper-junos-ssh-noenable.yml` | Renamed from an all-caps underscore name. |
| `Mellanox/mellanox-ssh-enable.yml` | `nvidia/nvidia-onyx-ssh-enable.yml` | Directory merge. Mellanox is NVIDIA Networking. The display name keeps `(Mellanox)` so the old brand stays searchable. |
| `Mikrotik/mikrotik-ssh-banner_prompt.yml` | `mikrotik/mikrotik-routeros-ssh-noenable-banner.yml` |  |
| `Mikrotik/mikrotik-ssh-noenable_isNonInteractiveMode-Vector.yml` | `mikrotik/mikrotik-routeros-ssh-noenable-noninteractive-vector.yml` | Carries two variants, so the tokens chain. |
| `Mikrotik/mikrotik-ssh-noenable_v2.yml` | `mikrotik/mikrotik-routeros-ssh-noenable.yml` | The v2 template becomes the canonical MikroTik template. |
| `Palo_Alto_Networks/panos-ssh-9x.yml` | `palo-alto/palo-alto-panos-9x-ssh-noenable.yml` | PAN-OS keeps its version split. 9.x behaves differently on connect. |
| `Palo_Alto_Networks/panos-ssh-v2.yml` | `palo-alto/palo-alto-panos-ssh-enable.yml` | The v2 template becomes the canonical PAN-OS template. `enable: on`, so authmode is enable. |
| `Palo_Alto_Networks/panos-ssh-vector.yml` | `palo-alto/palo-alto-panos-ssh-enable-vector.yml` |  |
| `RAD/rad-ssh-noenable.yml` | `rad/rad-ssh-noenable.yml` |  |
| `Ruckus/Ruckus_Devices_Enable.yml` | `ruckus/ruckus-fastiron-ssh-noenable.yml` | Name vs content. Both Ruckus files are `enable: off`. Enable/NO_Enable never described enable mode, it described paging. This is the paging on variant. |
| `Ruckus/Ruckus_Devices_NO_Enable.yml` | `ruckus/ruckus-fastiron-ssh-noenable-nopaging.yml` | Paging clarification. This is the paging off variant, hence -nopaging. |
| `Sonicwall/Sonicwall-ssh-confirm-banner.yml` | `sonicwall/sonicwall-sonicos-ssh-enable-banner.yml` |  |
| `Sonicwall/Sonicwall-ssh-no-enable.yml` | `sonicwall/sonicwall-sonicos-ssh-noenable.yml` |  |
| `Ubiquiti/unifios-ssh-no-enable.yml` | `ubiquiti/ubiquiti-unifios-ssh-enable.yml` | Name vs content. File said no-enable, content is `enable: on`. Content wins. |
| `base/base.yml` | `_base/base.yml` |  |
| `huawei/hua-ssh-noenable.yml` | `huawei/huawei-vrp-ssh-noenable.yml` |  |
| `linux/centos-7-ssh.yml` | `linux/linux-el-ssh-noenable.yml` | Generalised from CentOS 7 to the Enterprise Linux family (RHEL, CentOS, Rocky, Alma). |
| `nvidia/InfiniBand-ssh-noenable.yml` | `nvidia/nvidia-mlnxos-ssh-enable.yml` | Name vs content. File said noenable, content is `enable: on`. Content wins. |
| `pfSense/pfSense-ssh.yml` | `pfsense/pfsense-ssh-noenable.yml` |  |
| `siemens/ruggedcom-ros-ssh-noenable.yml` | `siemens/siemens-ruggedcom-ros-ssh-noenable.yml` |  |

Five templates kept their path unchanged: `SIE-Base/script_template.yml`,
`SIE-Radware/alteon_expect_script_template.yml`, `SSH-Private-Key/ssh_priv_key_template.yml`,
`XFTP/xftp-inbound-only.yml`, `vyos/vyos-ssh-noenable.yml`.

## Removed

### Templates

| Removed | Use instead | Reason |
| --- | --- | --- |
| `Mikrotik/mikrotik-ssh-noenable.yml` | `mikrotik/mikrotik-routeros-ssh-noenable.yml` | Superseded by the v2 template, which adds `isMikrotik: yes`. The `AnsiHost` and window size options the v1 carried are documented in `mikrotik/README.md`. |
| `Palo_Alto_Networks/panos-ssh.yml` | `palo-alto/palo-alto-panos-ssh-enable.yml` | Superseded by the v2 template, which adds scripting mode, richer paging commands and an options block. |

### Other files

| Removed | Reason |
| --- | --- |
| `.vscode/settings.json` | Editor configuration does not belong in the repository. The file remains on disk for anyone who had it, and `.vscode/` is now in `.gitignore`. |

### Stripped content

Trailing AI chat residue was removed from two documents. No document content was lost.

| File | Removed |
| --- | --- |
| `README.md` | Closing line "Let me know if you'd like this in a `.md` file..." plus two orphaned blank lines. |
| `docs/noninteractive-ssh.md` | Opening line "Sure thing! Here's the content converted to GitHub-styled markdown:" with its rule, and the closing rule plus "Let me know if you need any tweaks..." sign off. Eight lines in total, four of them blank. |

## Documentation moves

| Old | New | Notes |
| --- | --- | --- |
| `README-NONINTERACTIVEMODE-SSH.md` | `docs/noninteractive-ssh.md` | Moved out of the repository root. One `blob/master/Fortinet/` link inside it was corrected to `blob/main/fortinet/`. |
| `huawei/hua-ssh-noenable.md` | `huawei/README.md` | Vendor notes now follow the README convention used by other vendor directories. |

## Reconciliation

| | Count |
| --- | --- |
| Templates before | 66 |
| Templates renamed or moved | 59 |
| Templates deleted | 2 |
| Templates with unchanged paths | 5 |
| Templates after | 64 |
| Top level directories before | 38 |
| Top level directories after | 37 |
| Directory renames | 25 |
| Directory merges | 1 |
| Directories removed from tracking | 1 |
| Directories added | 1 |

## A note on git history

Git rename detection pairs the two ProCurve templates the wrong way round, because the
former v1 and v2 were about 90 percent identical and one took the other's filename. The
table above follows the file contents, which is the reliable lineage:

- `pagingCmd: "no page"` was in the old `hp-procurve-ssh-noenable.yml` and is now in
  `hp-procurve-ssh-noenable-nopage.yml`.
- `pagingCmd: "nno page"` was in the old `hp-procurve-ssh-noenable-v2.yml` and is now in
  `hp-procurve-ssh-noenable.yml`.
