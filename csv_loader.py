"""Reading CSV files into flight records and error messages."""


import csv
import os
from validator import validate_row, to_record


def parse_files(paths: list[str], airports: set[str]) -> tuple[list[dict], list[str]]:
    """Process the CSV files in the order given.

    Return (records, errors):
      records - valid flight records, in input order
      errors  - one message per invalid row, in input order, formatted as
                "<file name>:<line number>: <ERROR_CODE> | <free text>"
                (base file name only, no timestamp or level, no newline)

    Also performs the DUPLICATE_FLIGHT check across all the files.
    Does not write any files and does not log anything itself.
    """
    records = []
    errors = []
    seen = set()

    for path in paths:
        with open(path, "r", encoding="utf-8", newline="") as file:
            for line_number, line in enumerate(file, start=1):

                if line_number == 1:
                    continue

                if not line.strip() or line.lstrip().startswith("#"):
                    continue

                fields = next(csv.reader([line]))
                fields = [field.strip() for field in fields]

                error = validate_row(fields, airports)

                if error is None:
                    key = (fields[0], fields[3])

                    if key in seen:
                        error = "DUPLICATE_FLIGHT"
                    else:
                        seen.add(key)

                if error:
                    message = (
                        f"{os.path.basename(path)}:{line_number}: "
                        f"{error} | {line.rstrip(chr(13) + chr(10))}"
                    )
                    errors.append(message)
                else:
                    records.append(to_record(fields))

    return records, errors
