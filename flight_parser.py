"""Flight Schedule Parser and Query Tool - command-line entry point.

Run from the project folder, for example:
    python flight_parser.py -i data/db.csv -a data/airports.txt

"""

import sys
import csv
import argparse
import json
import logging
import os
from datetime import datetime
from validator import load_airports
from csv_loader import parse_files
from query import run_queries

# TODO: fill in your details: plain ASCII, no spaces or underscores.
STUDENT_ID = "251ADB065"
FIRST_NAME = "Fuad"
LAST_NAME = "Aliyev"


def main(argv: list[str] | None = None) -> int:
    """Run the whole program and return the exit code (0, 1 or 2).

    argv is the argument list without the program name.
    None means use sys.argv[1:] (argparse does this for you).
    Do not call sys.exit() inside main(); return the code instead.
    """
    parser = argparse.ArgumentParser(
        description="Flight Schedule Parser and Query Tool"
    )

    source = parser.add_mutually_exclusive_group(required=True)

    source.add_argument("-i", metavar="FILE")
    source.add_argument("-d", metavar="FOLDER")
    source.add_argument("-j", metavar="FILE")

    parser.add_argument("-a", metavar="FILE")
    parser.add_argument("-o", default=None, metavar="FILE")
    parser.add_argument("-q", metavar="FILE")
    parser.add_argument("-r", default=".", metavar="FOLDER")

    args = parser.parse_args(argv)

    if (args.i or args.d) and not args.a:
        parser.error("-a is required with -i or -d")

    if args.j and args.o:
        parser.error("-o cannot be used with -j")
    handler = None
    logger = logging.getLogger("flight_parser")

    try:
        if args.i or args.d:
            airports = load_airports(args.a)

            if args.i:
                paths = [args.i]
            else:
                if not os.path.isdir(args.d):
                    raise FileNotFoundError(f"Folder does not exist: {args.d}")

                paths = sorted(
                    os.path.join(args.d, name)
                    for name in os.listdir(args.d)
                    if name.endswith(".csv")
                    and os.path.isfile(os.path.join(args.d, name))
                )

                if not paths:
                    raise ValueError(f"No CSV files found in folder: {args.d}")

            db, errors = parse_files(paths, airports)

            db_path = args.o if args.o is not None else "db.json"

            with open(db_path, "w", encoding="utf-8") as file:
                json.dump(db, file, indent=2)
                file.write("\n")

            log_path = os.path.join(
                os.path.dirname(os.path.abspath(db_path)),
                "errors.log"
            )

            logger.setLevel(logging.INFO)

            handler = logging.FileHandler(
                log_path, mode="w", encoding="utf-8"
            )

            handler.setFormatter(logging.Formatter(
                "%(asctime)s %(levelname)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            ))

            logger.addHandler(handler)

            for error in errors:
                logger.warning(error)

        else:
            with open(args.j, "r", encoding="utf-8") as file:
                db = json.load(file)

            if not isinstance(db, list) or not all(
                isinstance(record, dict) for record in db
            ):
                raise ValueError("JSON database must be an array of objects")

        if args.q:
            with open(args.q, "r", encoding="utf-8") as file:
                queries = json.load(file)

            if not (
                isinstance(queries, dict)
                or (
                    isinstance(queries, list)
                    and all(isinstance(query, dict) for query in queries)
                )
            ):
                raise ValueError(
                    "Query file must contain an object or an array of objects"
                )

            results = run_queries(db, queries)

            response_name = (
                f"response_{STUDENT_ID}_{FIRST_NAME}_{LAST_NAME}_"
                f"{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            )

            response_path = os.path.join(args.r, response_name)

            with open(response_path, "w", encoding="utf-8") as file:
                json.dump(results, file, indent=2)
                file.write("\n")

        return 0

    except (OSError, UnicodeError, ValueError, csv.Error) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    finally:
        if handler is not None:
            logger.removeHandler(handler)
            handler.close()
      
if __name__ == "__main__":
    sys.exit(main())
