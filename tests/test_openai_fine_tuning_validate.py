import random
import string
from pathlib import Path

import pytest

from openai_fine_tuning_validate import load_dataset, validate_dataset

DATA_DIR = Path(__file__).resolve().parent / "data"


class Test_validate_dataset:
    def test_simple_dataset_valid(self):
        dataset = load_dataset(DATA_DIR / "dataset-1-simple.jsonl")
        assert validate_dataset(dataset) == {}

    def test_multi_turn_dataset_valid(self):
        dataset = load_dataset(DATA_DIR / "dataset-2-multi-turn.jsonl")
        assert validate_dataset(dataset) == {}

    @pytest.mark.skip()
    def test_empty_invalid(self): ...

    @pytest.mark.skip()
    def test_non_list_invalid(self): ...

    @pytest.mark.parametrize("dataset_line", ["", [], 3])
    def test_non_dict_line_invalid(self, dataset_line):
        result = validate_dataset([dataset_line])
        assert result == {"data_type": 1}

    @pytest.mark.parametrize(
        "dataset_line", [{}, {"prompt": "xyz"}, {"completion": "xyz"}]
    )
    def test_missing_messages_invalid(self, dataset_line):
        result = validate_dataset([dataset_line])
        assert result == {"missing_messages_list": 1}

    @pytest.mark.parametrize(
        ["dataset_line", "count"],
        [
            [{"messages": [{"content": "Hello"}]}, 1],
            [{"messages": [{"content": "Hello"}, {"content": "Hi!"}]}, 2],
        ],
    )
    def test_missing_role_invalid(self, dataset_line, count):
        result = validate_dataset([dataset_line])
        assert result["message_missing_key"] == count

    @pytest.mark.parametrize(
        ["dataset_line", "count"],
        [
            [{"messages": [{"role": "system"}, {"role": "user"}]}, 2],
            [
                {
                    "messages": [
                        {"role": "system"},
                        {"role": "user"},
                        {"role": "assistant"},
                    ]
                },
                3,
            ],
        ],
    )
    def test_missing_content_invalid(self, dataset_line, count):
        result = validate_dataset([dataset_line])
        assert result["message_missing_key"] == count

    @pytest.mark.parametrize("message_count", range(1, 10))
    def test_unrecognized_key_invalid(self, message_count):
        valid_keys = ("role", "content", "name", "function_call", "weight")

        messages = []
        for _ in range(1, message_count + 1):
            random_key = random_string()
            while random_key in valid_keys:
                random_key = random_string()
            messages.append({random_key: random_string()})

        result = validate_dataset([{"messages": messages}])
        assert result["message_unrecognized_key"] == message_count

    @pytest.mark.parametrize("role_value", ["asystem", "admin", "staff", "func"])
    def test_unrecognized_role_value_invalid(self, role_value):
        result = validate_dataset([{"messages": [{"role": role_value}]}])
        assert result["unrecognized_role"] == 1

    @pytest.mark.parametrize(
        ["dataset_line", "count"],
        [
            [{"messages": [{}]}, 1],
            [{"messages": [{"content": None}]}, 1],
            [
                {"messages": [{"content": "", "function_call": "xyz"}, {"con": "xyz"}]},
                1,
            ],
            [{"messages": [{"function_call": "xyz"}, {"con": "xyz"}]}, 2],
        ],
    )
    def test_missing_content_value_invalid(self, dataset_line, count):
        result = validate_dataset([dataset_line])
        assert result["missing_content"] == count

    @pytest.mark.parametrize(
        "dataset_line",
        [
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "Please write a blog post about ChatGPT.",
                    },
                ],
            },
            {
                "messages": [
                    {"role": "system", "content": "You are a good writer."},
                    {
                        "role": "user",
                        "content": "Please write a blog post about ChatGPT.",
                    },
                ],
            },
        ],
    )
    def test_missing_assistant_message_invalid(self, dataset_line):
        result = validate_dataset([dataset_line])
        assert result["example_missing_assistant_message"] == 1


def random_string(max_length=15) -> str:
    letters = string.ascii_lowercase
    length = random.choice(range(1, max_length + 1))
    return "".join(random.choices(letters, k=length))
