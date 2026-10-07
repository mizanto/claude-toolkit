"""Tests for the git-safety hook. Run: python3 -m unittest discover tests"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "plugins/toolkit/hooks/scripts/git_safety.py"

RISKY = [
    "git push", "git push --force origin main", "git push -f", "git push --force-with-lease",
    "git push origin :old", "git push --delete origin x", "git -c core.x=y push -u origin feat",
    "git reset --hard HEAD~1", "git reset --keep HEAD~1", "FOO=1 git -C ../repo reset --hard",
    "git clean -fd", "cd x; git clean -xfd",
    "git checkout -- src/a.ts", "git checkout .", "git checkout -f main",
    "git restore src/a.ts", "git restore --staged --worktree a", "git switch -f main",
    "git branch -D feat", "git branch -fd x", "git branch -f main HEAD~2",
    "git stash drop", "git stash clear",
    "git rebase main", "git rebase -i HEAD~3", "git commit --amend --no-edit",
    "git filter-branch --tree-filter x", "git filter-repo --path x",
    "git reflog expire --all", "git gc --prune=now", "git update-ref -d refs/heads/x",
    "git tag -d v1", "git tag -f v1", "git remote remove origin", "git remote set-url origin x",
    "git worktree remove --force ../wt", "rm -rf .git",
    "npm test && git push", "echo $(git push)", "/usr/bin/git push",
]

SAFE = [
    "git status", "git add -A", "git commit -m 'feat: x'", "git log --oneline", "git diff --cached",
    "git checkout main", "git checkout -b feat", "git switch feat", "git switch -c feat",
    "git restore --staged a.ts", "git clean -n", "git clean --dry-run",
    "git rebase --continue", "git rebase --abort", "git branch -d merged", "git branch new",
    "git stash", "git stash pop", "git fetch", "git pull", "git tag v1.0", "git remote add origin x",
    "git gc", "git worktree add ../wt", "ls .git", "echo 'git push'",
    "git commit -m 'reset --hard docs'", "grep -r 'git push' .", "npm test",
]


def run_hook(command, tool="Bash"):
    payload = json.dumps({"tool_name": tool, "tool_input": {"command": command}})
    return subprocess.run([sys.executable, str(SCRIPT)], input=payload,
                          capture_output=True, text=True, timeout=10)


class GitSafetyTest(unittest.TestCase):
    def test_risky_commands_ask(self):
        for cmd in RISKY:
            with self.subTest(cmd=cmd):
                out = run_hook(cmd).stdout
                self.assertTrue(out, f"not flagged: {cmd}")
                decision = json.loads(out)["hookSpecificOutput"]
                self.assertEqual(decision["permissionDecision"], "ask")
                self.assertTrue(decision["permissionDecisionReason"].startswith("git-safety:"))

    def test_safe_commands_pass(self):
        for cmd in SAFE:
            with self.subTest(cmd=cmd):
                self.assertEqual(run_hook(cmd).stdout, "", f"false positive: {cmd}")

    def test_bad_input_passes_through(self):
        result = subprocess.run([sys.executable, str(SCRIPT)], input="{bad json",
                                capture_output=True, text=True, timeout=10)
        self.assertEqual((result.returncode, result.stdout), (0, ""))

    def test_other_tools_ignored(self):
        self.assertEqual(run_hook("git push", tool="Write").stdout, "")


if __name__ == "__main__":
    unittest.main()
