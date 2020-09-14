#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import argparse
import json
import logging
import os
import subprocess
import sys
import urllib
from typing import Dict, List

import requests
from django.db.utils import OperationalError
from packageurl import PackageURL

from . import BaseJob

logger = logging.getLogger(__name__)


class CharacteristicsJob(BaseJob):
    """Identifies characteristics using OSS Gadget."""

    purl = None  # type: PackageURL

    def __init__(self):
        super().__init__()

        parser = argparse.ArgumentParser()
        parser.add_argument(
            "package", help="Package URL to check for typo-squatting.", type=str,
        )
        args = parser.parse_args()

        try:
            self.purl = PackageURL.from_string(args.package)
        except ValueError:
            logger.warning("Invalid PackageURL: %s", args.package)
            raise

    def run(self):
        """Runs the job."""
        if self.purl.type == "github":
            logger.warning("Unable to calculate typo-squatting for GitHub projects.")
            return None

        output = subprocess.check_output(
            ["oss-characteristic", "-f", "sarifv2", str(self.purl)], cwd="/tmp", timeout=30
        )
        output_json = json.loads(output)
        tags = set()
        for run in output_json.get("runs", []):
            for result in run.get("results", []):
                for tag in result.get("properties", {}).keys():
                    tags.add(tag)
        return {"tags": tags}


if __name__ == "__main__":
    job = CharacteristicsJob()
    _result = job.run()
    if _result is not None:
        print(json.dumps(_result, indent=2))
        sys.exit(0)
    else:
        sys.exit(1)
