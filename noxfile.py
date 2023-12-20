import nox  # pylint: disable=import-error

nox.options.sessions = ["isort", "black", "flake8", "pylint"]
nox.options.force_venv_backend = "none"


@nox.session
def isort(session):
    session.run("python", "-m", "isort", "--profile", "black", "--check-only", ".")


@nox.session
def black(session):
    session.run("python", "-m", "black", "-C", "--line-length=88", "--check", ".")


@nox.session
def flake8(session):
    session.run(
        "python",
        "-m",
        "flake8",
        "apps/",
        "delivery/",
        "--exclude",
        "delivery/settings/",
        "--max-line-length=88",
    )


@nox.session
def pylint(session):
    session.run("python", "-m", "pylint", "--recursive=y", ".")


@nox.session
def format_task(session):
    session.run(
        "python", "-m", "isort", "--overwrite-in-place", "--profile", "black", "."
    )
    session.run("python", "-m", "black", "-C", "--line-length=88", ".")
