"""Install the documented uv tool environment, then audit or test that environment."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def capture_command_stdout(command, *, cwd, environment, log):
    """Return only command data while preserving diagnostics in the log."""
    result = subprocess.run(
        command, cwd=cwd, env=environment,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace",
    )
    for output in (result.stdout, result.stderr):
        print(output, end="", flush=True)
        log.write(output)
    log.flush()
    result.check_returncode()
    return result.stdout


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--report-dir", type=Path, default=ROOT / "security-reports")
    args = parser.parse_args()
    if not (args.audit or args.test):
        parser.error("Specify --audit or --test")
    reports = args.report_dir.resolve()
    reports.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="pokemon-tool-check-") as temp_dir:
        temporary = Path(temp_dir)
        environment = os.environ.copy()
        environment["PYTHONUTF8"] = "1"
        # Protect the developer's installed tools; use the normal installer unchanged.
        environment["UV_TOOL_DIR"] = str(temporary / "tools")
        environment["UV_TOOL_BIN_DIR"] = str(temporary / "bin")
        with (reports / "python.txt").open("w", encoding="utf-8") as log:
            def run(*command, cwd=ROOT, stdout_only=False):
                line = "+ " + " ".join(map(str, command)) + "\n"
                print(line, end="", flush=True)
                log.write(line)
                if stdout_only:
                    return capture_command_stdout(
                        list(map(str, command)), cwd=cwd,
                        environment=environment, log=log,
                    )
                process = subprocess.Popen(
                    list(map(str, command)), cwd=cwd, env=environment,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding="utf-8", errors="replace",
                )
                output = []
                for line in process.stdout:
                    print(line, end="", flush=True)
                    log.write(line)
                    output.append(line)
                log.flush()
                if process.wait():
                    raise subprocess.CalledProcessError(process.returncode, command)
                return "".join(output)

            if not run("uv", "--version", stdout_only=True).startswith("uv 0.13.8 "):
                raise RuntimeError("Use uv 0.13.8 as documented in the README")

            # Only the source is local for PR verification; installation is the
            # same non-editable uv tool install used in the README.
            source = temporary / "source"
            source.mkdir()
            for name in ("setup.py", "pyproject.toml", "README.md", "LICENSE", "package.json"):
                shutil.copy2(ROOT / name, source / name)
            shutil.copytree(ROOT / "pokemonterminal", source / "pokemonterminal",
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            run("uv", "tool", "install", "--python", "3.12", source)
            tool = temporary / "tools" / "pokemon-terminal"
            python = tool / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
            # Run away from the checkout, so imports and package data come from
            # the installed wheel rather than from the source directory.
            run(python, "-m", "pokemonterminal.main", "-dr", cwd=temporary)
            requirements = reports / "python-requirements.txt"
            snapshot = run("uv", "pip", "freeze", "--python", python,
                           "--exclude", "pokemon-terminal", stdout_only=True)
            requirements.write_text(snapshot, encoding="utf-8")
            if args.audit:
                if snapshot.strip():
                    run("uv", "tool", "run", "--python", "3.12",
                        "--from", "pip-audit==2.10.1", "pip-audit",
                        "-r", requirements, "--no-deps", "--disable-pip",
                        "--strict", "--progress-spinner", "off")
                else:
                    message = "No third-party runtime dependencies on this platform.\n"
                    print(message, end="")
                    log.write(message)
            if args.test:
                # Constrain the additions to the exact installed runtime versions.
                run("uv", "pip", "install", "--python", python,
                    "--constraint", requirements, "-r", ROOT / "requirements-test.txt")
                installed = set(run("uv", "pip", "freeze", "--python", python,
                                    "--exclude", "pokemon-terminal", stdout_only=True).splitlines())
                if not set(snapshot.splitlines()).issubset(installed):
                    raise RuntimeError("Test tools changed runtime dependency versions")
                run(python, "-m", "flake8", ROOT, "--count",
                    "--select=E9,F63,F72,F82", "--show-source", "--statistics")
                # Copy tests and their CI helper; load the app from its installed wheel.
                shutil.copytree(ROOT / "tests", temporary / "tests")
                shutil.copytree(ROOT / "scripts", temporary / "scripts",
                                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                run(python, "-m", "pytest", "tests", "-q", cwd=temporary)


if __name__ == "__main__":
    main()
