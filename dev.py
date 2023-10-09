import math
import os
import sys

import click

from logging.config import dictConfig

from src import app, COV


@app.cli.command("test")
@click.option("--with_coverage")
@click.option("--with_dir")
def test(with_coverage=False, with_dir=""):
    if with_coverage and not os.environ.get("FLASK_COVERAGE"):
        os.environ["FLASK_COVERAGE"] = "1"
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    import unittest

    if with_dir:
        tests = unittest.TestLoader().discover(with_dir)
    else:
        tests = unittest.TestLoader().discover("src/tests")
    test_results = unittest.TextTestRunner(verbosity=2).run(tests)

    if COV:
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        cov_percentage = COV.report()
        COV.html_report()
        print(cov_percentage)

        if (
            len(test_results.failures) == len(test_results.errors) == 0
            and math.floor(cov_percentage) >= 80
        ):
            return sys.exit(0)
        else:
            return sys.exit(1)


# create folder "logs"
if not os.path.exists("logs"):
    os.makedirs("logs")

# logger configuration
# follow this instruction to understand and customize
# it's very clear and detailed
# https://betterstack.com/community/guides/logging/how-to-start-logging-with-flask/
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s "
                "| %(module)s:%(lineno)d] %(message)s",
                "datefmt": "%B %d, %Y %H:%M:%S %Z",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "time-rotate": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": "logs/flask.log",
                "when": "D",
                "interval": 7,
                "backupCount": 5,
                "formatter": "default",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console", "time-rotate"]},
    }
)

if __name__ == "__main__":
    app.run()
