# iwillbuild

Education site builder.

## Course Builder Script

The `course_builder.py` script turns a GitHub repository into a step-by-step course.
It walks through the commit history, generating code snippets, hints, quizzes, and
a small anecdote for each change.

### Usage

```bash
python course_builder.py https://github.com/octocat/Hello-World -o hello-course.md
```

The command above clones the target repository and produces a `hello-course.md`
file that outlines the app's evolution, challenges learners, and provides hints
along the way.
