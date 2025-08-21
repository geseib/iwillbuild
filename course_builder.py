import argparse
import re
import shutil
import subprocess
import tempfile
from typing import List


def _run(cmd: List[str], cwd: str) -> str:
    """Run a command and return stdout."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True)
    return result.stdout


def generate_course(repo_url: str, output_path: str = "course.md") -> str:
    """Clone a repository and build a step-by-step course file."""
    temp_dir = tempfile.mkdtemp()
    try:
        subprocess.run(["git", "clone", repo_url, temp_dir], check=True, capture_output=True, text=True)
        commits = _run(["git", "rev-list", "--reverse", "HEAD"], cwd=temp_dir).strip().splitlines()
        course_lines = ["# Course Outline", ""]
        for index, commit in enumerate(commits, start=1):
            message = _run(["git", "show", "-s", "--format=%s", commit], cwd=temp_dir).strip()
            if index == 1:
                diff = _run(["git", "show", commit], cwd=temp_dir)
            else:
                diff = _run(["git", "diff", f"{commit}^", commit], cwd=temp_dir)
            snippet = "\n".join(
                line for line in diff.splitlines() if line.startswith("+") or line.startswith("@@")
            )
            new_funcs = re.findall(r"^\+def\s+(\w+)", diff, flags=re.MULTILINE)
            step_lines = [f"## Step {index}: {message}", "```python", snippet, "```"]
            if new_funcs:
                step_lines.append("### Hints")
                step_lines.extend([f"- Examine how `{fn}` is implemented." for fn in new_funcs])
                step_lines.append("### Quiz")
                step_lines.extend([f"- What parameters does `{fn}` accept?" for fn in new_funcs])
            anecdotes: List[str] = []
            lower_msg = message.lower()
            if "refactor" in lower_msg:
                anecdotes.append("Notice the refactoring approach used here.")
            if "test" in lower_msg:
                anecdotes.append("Tests are introduced to ensure correctness.")
            if "fix" in lower_msg:
                anecdotes.append("Bug fixing showcases debugging techniques.")
            if anecdotes:
                step_lines.append("### Anecdotes")
                step_lines.extend([f"- {a}" for a in anecdotes])
            course_lines.extend(step_lines)
            course_lines.append("")
        with open(output_path, "w") as f:
            f.write("\n".join(course_lines))
        return output_path
    finally:
        shutil.rmtree(temp_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a course from a GitHub repo")
    parser.add_argument("repo_url", help="GitHub repository URL")
    parser.add_argument("-o", "--output", default="course.md", help="Output markdown file")
    args = parser.parse_args()
    output = generate_course(args.repo_url, args.output)
    print(f"Course written to {output}")


if __name__ == "__main__":
    main()
