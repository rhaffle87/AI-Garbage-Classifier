import subprocess
import sys
import os


def test_train_dry_run():
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    script = os.path.join(ROOT, 'scripts', 'train.py')
    # Run dry-run to validate dataset parsing
    proc = subprocess.run([sys.executable, script, '--dry-run'], capture_output=True, text=True)
    # On missing dataset this script may exit non-zero; ensure it didn't crash (we accept 0 or nonzero with a message)
    assert proc.returncode == 0
    assert 'Dry run' in proc.stdout
