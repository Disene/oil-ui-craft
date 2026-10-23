"""Fork-only update safety regression. No network or npm required."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_update.py"


class ForkUpdateProtection(unittest.TestCase):
    def test_explicit_upstream_update_is_blocked(self):
        with tempfile.TemporaryDirectory(prefix="oil-fork-guard-") as tmp:
            skill = Path(tmp) / "fork"
            (skill / "scripts").mkdir(parents=True)
            shutil.copy(SCRIPT, skill / "scripts" / "check_update.py")
            original = '---\nname: oil-ui\nmetadata:\n  version: "0.24.2"\n  fork_release: "craft-ux.1"\n---\n'
            (skill / "SKILL.md").write_text(original, encoding="utf-8")
            env = dict(os.environ)
            env.pop("OIL_NO_UPDATE_CHECK", None)
            env["HOME"] = str(Path(tmp) / "home")
            env["XDG_STATE_HOME"] = str(Path(tmp) / "state")
            env["OIL_API"] = "http://127.0.0.1:9/should-not-call"
            proc = subprocess.run([sys.executable, str(skill / "scripts" / "check_update.py"), "--update"],
                                  env=env, text=True, capture_output=True, timeout=8, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("OIL_FORK_UPDATE_DISABLED", proc.stdout)
            self.assertEqual((skill / "SKILL.md").read_text(encoding="utf-8"), original)
            self.assertFalse((Path(tmp) / "state").exists())


if __name__ == "__main__":
    unittest.main()
