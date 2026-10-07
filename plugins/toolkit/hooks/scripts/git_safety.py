#!/usr/bin/env python3
"""git-safety PreToolUse hook for Claude Code.

Reads the Bash tool call from stdin. If the command contains a git operation
that rewrites history, discards uncommitted work, or publishes to a remote,
returns permissionDecision "ask" so the user confirms it. Everything else
passes through untouched (exit 0, no output).
"""
import json
import re
import shlex
import sys

# git global options that take a separate value argument
OPTS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"}


def split_segments(command):
    """Split a shell command line into simple commands on ; && || | & and newlines."""
    return [s for s in re.split(r"\|\||&&|[;|&\n]|\$\(|`|\(|\)", command) if s.strip()]


def git_args(segment):
    """Return the args after `git` (and its global options) or None if not a git command."""
    try:
        tokens = shlex.split(segment, posix=True)
    except ValueError:
        tokens = segment.split()
    # skip env assignments and common wrappers: FOO=bar git ..., sudo git ..., command git ...
    while tokens and (re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tokens[0])
                      or tokens[0] in {"sudo", "command", "exec", "env", "nohup", "time"}):
        tokens = tokens[1:]
    if not tokens or tokens[0].rsplit("/", 1)[-1] != "git":
        return None
    args = tokens[1:]
    while args and args[0].startswith("-"):
        opt = args.pop(0)
        if opt in OPTS_WITH_VALUE and args:
            args.pop(0)
    return args


def has(args, *flags):
    return any(a in flags or any(a.startswith(f + "=") for f in flags if f.startswith("--")) for a in args)


def has_short(args, letter):
    """True if a combined short-flag cluster like -fd or -D contains letter."""
    return any(re.fullmatch(r"-[A-Za-z]+", a) and letter in a[1:] for a in args)


def check(args):
    """Return a reason string if the git command is risky, else None."""
    if not args:
        return None
    sub, rest = args[0], args[1:]

    if sub == "push":
        if has(rest, "--force", "--force-with-lease", "--force-if-includes", "--mirror") or has_short(rest, "f"):
            return "force-pushes to a remote, which can overwrite others' commits"
        if has(rest, "--delete") or has_short(rest, "d") or any(a.startswith(":") and len(a) > 1 for a in rest):
            return "deletes a branch or tag on a remote"
        return "publishes commits to a remote"
    if sub == "reset" and has(rest, "--hard", "--merge", "--keep"):
        return "discards uncommitted changes and moves the branch"
    if sub == "clean" and not has(rest, "--dry-run", "-n") and not has_short(rest, "n"):
        return "permanently deletes untracked files"
    if sub == "checkout":
        paths_after_dashdash = "--" in rest and rest.index("--") < len(rest) - 1
        if paths_after_dashdash or "." in rest or has(rest, "--force") or has_short(rest, "f"):
            return "overwrites uncommitted changes in the working tree"
    if sub == "restore":
        touches_worktree = has(rest, "--worktree", "-W") or not has(rest, "--staged", "-S")
        if touches_worktree:
            return "overwrites uncommitted changes in the working tree"
    if sub == "switch" and (has(rest, "--discard-changes", "--force") or has_short(rest, "f")):
        return "switches branch and discards uncommitted changes"
    if sub == "branch" and (has_short(rest, "D") or has(rest, "--force") and has(rest, "--delete")):
        return "force-deletes a branch, including unmerged commits"
    if sub == "branch" and (has(rest, "--force") or has_short(rest, "f")) and len(rest) > 1:
        return "force-moves an existing branch"
    if sub == "stash" and rest[:1] in (["drop"], ["clear"]):
        return "permanently deletes stashed changes"
    if sub == "rebase" and not has(rest, "--abort", "--continue", "--skip", "--quit", "--show-current-patch"):
        return "rewrites commit history"
    if sub == "commit" and has(rest, "--amend"):
        return "rewrites the last commit (risky if it was already pushed)"
    if sub in ("filter-branch", "filter-repo"):
        return "rewrites repository history"
    if sub == "reflog" and rest[:1] in (["expire"], ["delete"]):
        return "deletes reflog entries used to recover lost commits"
    if sub == "gc" and has(rest, "--prune"):
        return "permanently prunes unreachable commits"
    if sub == "update-ref" and (has(rest, "-d") or has_short(rest, "d")):
        return "deletes a ref directly"
    if sub == "tag" and (has(rest, "--delete", "--force") or has_short(rest, "d") or has_short(rest, "f")):
        return "deletes or moves a tag"
    if sub == "remote" and rest[:1] in (["remove"], ["rm"], ["set-url"]):
        return "changes or removes a remote"
    if sub == "worktree" and rest[:1] == ["remove"] and (has(rest, "--force") or has_short(rest, "f")):
        return "force-removes a worktree with uncommitted changes"
    return None


def risky_reasons(command):
    reasons = []
    for seg in split_segments(command):
        args = git_args(seg)
        reason = check(args) if args is not None else None
        if reason:
            reasons.append(f"`{seg.strip()}` {reason}")
    if re.search(r"\brm\s+(-[A-Za-z]*\s+)*\S*\.git(/|\s|$)", command):
        reasons.append("deletes a .git directory, destroying repository history")
    return reasons


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    command = (data.get("tool_input") or {}).get("command") or ""
    reasons = risky_reasons(command)
    if not reasons:
        return 0
    json.dump({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": "git-safety: " + "; ".join(reasons),
        }
    }, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
