def test_ruff_format_check():
    import subprocess

    result = subprocess.run(
        ["ruff", "check", "--fix", "."],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, "Ruff check found issues. Run `ruff check --fix .` to fix them."

    result = subprocess.run(
        ["ruff", "format", "."],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, "Ruff format found issues. Run `ruff format .` to fix them."
