"""
Den - Braindumping for projects made easy.
"""

from . import cmd


def main() -> None:
    try:
        cmd.execute()
    except Exception as e:
        print(
            f"""
            Terminated due to an exception: {e}
            If this is a significant issue, please consider reporting this by filing an issue on GitHub.
            """
        )


if __name__ == "__main__":
    main()
