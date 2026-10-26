#!/usr/bin/env python3
"""Regression tests for scripts/validate_templates.py.

Usage:
    python3 -m unittest discover -s scripts -p "test_*.py"
"""

import copy
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import yaml  # noqa: E402

import validate_templates as vt  # noqa: E402

TEMPLATE = "vendor/vendor-os-ssh-noenable.yml"


def connection_doc(protocol):
    """A minimal template carrying every key mandatory for ssh and telnet."""
    return {
        "main": {"name": "Test", "desc": "Test"},
        "connect": {"protocol": protocol, "port": 22, "timeout": 30},
        "auth": {
            "username": "Username:",
            "password": "Password:",
            "enable": "off",
            "enableCmd": "enable",
            "enablePassPrmpt": "Password:",
            "hpAnyKeyStatus": "off",
        },
        "config": {
            "linebreak": "n",
            "paging": "off",
            "pagingCmd": "terminal length 0",
            "resetPagingCmd": "terminal length 40",
            "saveConfig": "wr mem",
            "exitCmd": "quit",
        },
    }


def without_linebreak(doc):
    doc = copy.deepcopy(doc)
    del doc["config"]["linebreak"]
    return doc


def check(doc):
    protocol = doc["connect"]["protocol"]
    rep = vt.Report()
    vt.check_keys(TEMPLATE, doc, rep)
    vt.check_mandatory(TEMPLATE, doc, protocol, rep)
    vt.check_values(TEMPLATE, doc, rep)
    return rep


class LegacyLinebreakTest(unittest.TestCase):
    """config.linebreak has no runtime effect, but rConfig Pro before V8.3.2 and Core before
    8.2.16 fail every job on a template without it. It must stay mandatory. See RCO-1588."""

    def test_ssh_and_telnet_templates_without_linebreak_are_rejected_with_the_reason(self):
        for protocol in ("ssh", "telnet"):
            with self.subTest(protocol=protocol):
                rep = check(without_linebreak(connection_doc(protocol)))

                self.assertEqual(len(rep.errors), 1, rep.errors)
                self.assertIn("missing mandatory key 'config.linebreak'", rep.errors[0])
                self.assertIn("Pro before V8.3.2 and Core before 8.2.16", rep.errors[0])
                self.assertIn("config.commandLinebreak", rep.errors[0])

    def test_template_with_linebreak_and_command_linebreak_is_clean(self):
        doc = connection_doc("ssh")
        doc["config"]["commandLinebreak"] = "n"

        rep = check(doc)

        self.assertEqual(rep.errors, [])
        self.assertEqual(rep.warnings, [])

    def test_linebreak_is_not_flagged_as_deprecated(self):
        self.assertIn("linebreak", vt.ALLOWED["config"])
        self.assertNotIn("linebreak", vt.DEPRECATED.get("config", set()))

    def test_linebreak_stays_mandatory_for_ssh_and_telnet(self):
        self.assertIn("config.linebreak", vt.MANDATORY["ssh"])
        self.assertIn("config.linebreak", vt.MANDATORY["telnet"])

    def test_protocols_that_never_read_it_do_not_require_it(self):
        for protocol in ("tl1", "script", "xftp", "ftp"):
            with self.subTest(protocol=protocol):
                rep = vt.Report()
                vt.check_mandatory(TEMPLATE, without_linebreak(connection_doc(protocol)), protocol, rep)

                self.assertEqual(rep.errors, [])

    def test_starter_template_keeps_linebreak(self):
        with open(os.path.join(vt.REPO, "_base", "base.yml")) as f:
            doc = yaml.load(f, Loader=vt.RConfigLoader)

        self.assertEqual(doc["config"].get("linebreak"), "n")


if __name__ == "__main__":
    unittest.main()
