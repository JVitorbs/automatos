import os
import sys

from django.core.management import execute_from_command_line


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webui.settings")
    command = ["run_web.py", "runserver", "127.0.0.1:8000"]
    execute_from_command_line(command + sys.argv[1:])


if __name__ == "__main__":
    main()
