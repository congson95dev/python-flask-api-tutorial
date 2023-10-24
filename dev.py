import logging
import math
import os
import sys
import re

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


# logger masking
class MaskingFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        masking_rules = [
            (r"\b(\d{4}-\d{4}-\d{4}-\d{4})\b", "****-****-****-****"),  # Credit card
            (r"\b(\d{3}-\d{2}-\d{4})\b", "***-**-****"),  # Social Security Numbers
            (r"\b[\w\.-]+@[\w\.-]+\b", "user@example.com"),  # Email addresses
            (r"\b(\d{3}-\d{3}-\d{4})\b", "***-***-****"),  # Phone numbers
            (r'\bpassword[\'": ]*[^\'": ]+\b', "password: ********"),  # Passwords
            (r"\bapi_key=[\w-]+\b", "api_key=***"),  # API keys and tokens
        ]

        for pattern, replacement in masking_rules:
            message = re.sub(pattern, replacement, message)

        return message


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
            "masked": {
                "()": MaskingFormatter,
                "format": "[%(asctime)s] [%(levelname)s "
                "| %(module)s:%(lineno)d] %(message)s",
                "datefmt": "%B %d, %Y %H:%M:%S %Z",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "masked",
            },
            "time-rotate": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": "logs/flask.log",
                "when": "D",
                "interval": 7,
                "backupCount": 5,
                "formatter": "masked",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console", "time-rotate"]},
    }
)

# Example log usage
logger = logging.getLogger(__name__)
credit_card_number = "1234-5678-9012-3456"
ssn = "123-45-6789"
email = "user@example.com"
phone = "555-555-5555"
password = "user_password"
api_key = "api_key=abcdef123456"

logger.info(f"User provided credit card number: {credit_card_number}")
logger.info(f"User provided SSN: {ssn}")
logger.info(f"User provided email: {email}")
logger.info(f"User provided phone number: {phone}")
logger.info(f"User provided password: {password}")
logger.info(f"User provided API key: {api_key}")

if __name__ == "__main__":
    app.run()
