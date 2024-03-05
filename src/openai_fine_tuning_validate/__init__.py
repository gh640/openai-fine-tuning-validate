"""Validate a dataset for OpenAI fine tuning."""

import json
import sys

from collections import defaultdict
from pathlib import Path
from pprint import pprint

import click


@click.command()
@click.argument("dataset_file", type=click.Path(exists=True), required=True)
def main(dataset_file: str):
    """Main function"""
    dataset = load_dataset(dataset_file)

    if not dataset:
        click.echo("Dataset is empty", err=True)
        sys.exit(1)

    if not isinstance(dataset, list):
        click.echo(f"Dataset is not a list: {type(dataset)=}", err=True)
        sys.exit(1)

    result = validate_dataset(dataset)

    if result:
        pprint(result)
        sys.exit(1)

    click.echo("Dataset is valid")


def load_dataset(dataset_file: str) -> list[dict]:
    """Load a dataset from a file."""
    dataset_lines = Path(dataset_file).read_text(encoding="utf-8").splitlines()
    dataset = [json.loads(line) for line in dataset_lines]
    return dataset


def validate_dataset(dataset: list[dict]) -> dict[str, int]:
    """Validate a dataset for OpenAI fine tuning.

    See: https://cookbook.openai.com/examples/chat_finetuning_data_prep
    """
    # Format error checks
    format_errors = defaultdict(int)

    for ex in dataset:
        if not isinstance(ex, dict):
            format_errors["data_type"] += 1
            continue

        messages = ex.get("messages", None)
        if not messages:
            format_errors["missing_messages_list"] += 1
            continue

        for message in messages:
            if "role" not in message or "content" not in message:
                format_errors["message_missing_key"] += 1

            if any(
                k not in ("role", "content", "name", "function_call", "weight")
                for k in message
            ):
                format_errors["message_unrecognized_key"] += 1

            if message.get("role", None) not in (
                "system",
                "user",
                "assistant",
                "function",
            ):
                format_errors["unrecognized_role"] += 1

            content = message.get("content", None)
            function_call = message.get("function_call", None)

            if (not content and not function_call) or not isinstance(content, str):
                format_errors["missing_content"] += 1

        if not any(message.get("role", None) == "assistant" for message in messages):
            format_errors["example_missing_assistant_message"] += 1

    return dict(format_errors)
