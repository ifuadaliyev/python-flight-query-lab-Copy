# AI Usage Disclosure

## Tools used

- ChatGPT (OpenAI, GPT-6): explaining Python concepts, implementation guidance, code review, debugging, and testing assistance.

## Conversation links

- Link 1: https://chatgpt.com/share/6b0572d9-613c-83ed-9b5a-f9d2b7690f5d

## What I used them for

- Understanding the assignment requirements and project structure.
- Explaining Python concepts such as sets, regular expressions, datetime, CSV parsing, argparse, JSON, and logging.
- Implementing and reviewing the required functions.
- Debugging indentation and code placement issues.
- Preparing test commands and interpreting test results.

## Which parts of the code were AI-generated or substantially AI-assisted

| File | Function or part | How |
| --- | --- | --- |
| validator.py | load_airports() | AI-assisted implementation |
| validator.py | validate_row() | AI-assisted implementation |
| validator.py | to_record() | AI-assisted implementation |
| csv_loader.py | parse_files() | AI-assisted implementation |
| query.py | run_query() | AI-assisted implementation |
| query.py | run_queries() | AI-assisted implementation |
| flight_parser.py | main() | AI-assisted implementation and debugging |

## Key prompts

1. Help me implement the Python Flight Query graded lab step by step, following the exact assignment requirements.
2. Explain and help implement the validation, CSV parsing, and query functions while keeping the code simple.
3. Help me implement the command-line interface, JSON handling, logging, and debug the program using the public tests.

## What I changed or verified myself

I entered and reviewed the suggested code in GitHub Codespaces, corrected code placement and indentation issues, and tested the individual functions. I used Python 3.13.5, ran the sample datasets, and executed the teacher's public test suite. All 29 public tests passed.
