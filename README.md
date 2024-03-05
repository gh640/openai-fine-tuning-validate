# `openai-fine-tuning-validate`

A simple script to validate datasets for OpenAI fine tuning. 

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

