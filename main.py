"""The Most Honest Outage Line: emit one fixed status page line.

The program is fully deterministic: no network, no clock, no randomness,
no input files. It writes exactly one locked line to entry.txt and
nothing else, so both grader runs produce identical bytes.
"""

import os
from pathlib import Path

# The locked entry line, 157 characters (em dash written as an escape).
# It is the whole entry: a first-person status page message from the agent
# during a total server outage, naming what is down and what it cannot check.
OUTAGE_LINE = "All servers are down, including this status page's backend. I can't verify the cause \u2014 I'm posting from outside our systems and will update when I know more."

EXPECTED_CHARS = 157
MAX_CHARS = 160


def _vet(line):
    """Refuse anything but exactly the locked line."""
    if len(line) != EXPECTED_CHARS:
        raise SystemExit("entry line is not the locked 157-character line")
    if not line.strip():
        raise SystemExit("entry line is blank")
    if len(line) > MAX_CHARS:
        raise SystemExit("entry line exceeds the 160-character gate")


def _resolve_output_dir():
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if wanted.strip():
        return Path(wanted)
    return Path("/output")


def _emit(line):
    _vet(line)
    target = _resolve_output_dir() / "entry.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(line.encode("utf-8"))
    os.chmod(target, 0o644)
    return target


def main():
    _emit(OUTAGE_LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
