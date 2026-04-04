"""
Den - Braindumping for projects made easy.
"""

from . import cmd


def main() -> None:
    try:
        cmd.execute()
    except Exception as e:
        print("The program was terminated due to the exception: ", e)


if __name__ == "__main__":
    main()
