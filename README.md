# `openai-fine-tuning-validate`

A simple script to validate datasets for OpenAI fine tuning. 

The validator function was blatantly copied from the OpenAI Cookbook.

- [Data preparation and analysis for chat model fine-tuning | OpenAI Cookbook](https://cookbook.openai.com/examples/chat_finetuning_data_prep)
- [openai-cookbook/examples/Chat_finetuning_data_prep.ipynb at b6aeae9bbabe624cd5d766cc96c9a187235dbbda · openai/openai-cookbook](https://github.com/openai/openai-cookbook/blob/b6aeae9bbabe624cd5d766cc96c9a187235dbbda/examples/Chat_finetuning_data_prep.ipynb)

## Target models

- `gpt-3.5-turbo-0125`
- `gpt-3.5-turbo-1106`
- `gpt-3.5-turbo-0613`

> [!CAUTION]
> `babbage-002` and `davinci-002` use a different format and we cannot validate datasets for them with this script.

## Prerequiresites

- Python `>=3.12`
- Poetry `>=1.8.1`

## Usage

Checkout the repository.

```bash
git clone https://github.com/gh640/openai-fine-tuning-validate
```

Install dependencies with Poetry.

```bash
poetry install
```

Run `openai-fine-tuning-validate` command in a venv Poetry manages.

```bash
poetry run openai-fine-tuning-validate [dataset-file]
```

## Reference

- [Fine-tuning - OpenAI API](https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset)
- [Data preparation and analysis for chat model fine-tuning | OpenAI Cookbook](https://cookbook.openai.com/examples/chat_finetuning_data_prep)

