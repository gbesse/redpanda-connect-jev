"""Optional end-to-end check against a real Redpanda Connect binary."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PipelineTests(unittest.TestCase):
    @unittest.skipUnless(os.environ.get("CONNECT_BIN"), "CONNECT_BIN is not configured")
    def test_failed_input_is_reviewed_without_reaching_stdout(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            manifest = (ROOT / "plugin.yaml").read_text()
            command = [sys.executable, str(ROOT / "processor.py")]
            manifest = re.sub(r"^command:.*$", "command: " + json.dumps(command), manifest, flags=re.MULTILINE)
            (work / "plugin.yaml").write_text(manifest)
            (work / "connect.yaml").write_bytes((ROOT / "connect.yaml").read_bytes())
            env = os.environ.copy()
            env["TYPESAFE_API_KEY"] = "test-only"
            result = subprocess.run(
                [
                    os.environ["CONNECT_BIN"],
                    "run",
                    "--log.level=off",
                    "--disable-telemetry",
                    "--rpc-plugins=plugin.yaml",
                    "connect.yaml",
                ],
                cwd=work,
                env=env,
                input=b'{"id":1}\n',
                capture_output=True,
                timeout=30,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
            self.assertEqual(result.stdout, b"")
            self.assertEqual((work / "failed-inputs.txt").read_bytes(), b'{"id":1}\n')
