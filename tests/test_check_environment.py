"""Regression coverage for diagnostics emitted by uv on macOS."""
import io
import os
import subprocess
import sys

import pytest

from scripts.check_environment import capture_command_stdout


def test_requirements_stdout_excludes_environment_diagnostic(tmp_path):
    diagnostic = "Using Python 3.12 environment at: /private/var/folders/tool"
    log = io.StringIO()
    command = [sys.executable, "-c",
               "import sys; print('psutil==7.2.2'); "
               f"print({diagnostic!r}, file=sys.stderr)"]
    requirements = capture_command_stdout(
        command, cwd=tmp_path, environment=os.environ.copy(), log=log,
    )
    assert requirements == "psutil==7.2.2\n"
    assert diagnostic not in requirements
    assert diagnostic in log.getvalue()
    assert "psutil==7.2.2" in log.getvalue()


def test_empty_dependencies_stay_empty_with_stderr_diagnostic(tmp_path):
    log = io.StringIO()
    result = capture_command_stdout(
        [sys.executable, "-c", "import sys; print('Using Python', file=sys.stderr)"],
        cwd=tmp_path, environment=os.environ.copy(), log=log,
    )
    assert result == ""
    assert "Using Python" in log.getvalue()


def test_failed_command_is_not_accepted_as_dependency_snapshot(tmp_path):
    log = io.StringIO()
    with pytest.raises(subprocess.CalledProcessError) as failure:
        capture_command_stdout(
            [sys.executable, "-c",
             "import sys; print('collection failed', file=sys.stderr); sys.exit(2)"],
            cwd=tmp_path, environment=os.environ.copy(), log=log,
        )
    assert failure.value.returncode == 2
    assert "collection failed" in log.getvalue()
