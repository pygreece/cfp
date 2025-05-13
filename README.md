# 📋 cfp – PyCon GR Program Team Utilities

**cfp** is a Python CLI tool that helps the PyCon Greece Program Team
assign reviewers to talk proposals efficiently. It reads proposals and
reviewer lists exported from [Pretalx](https://pretalx.org/), generates
fair assignments, and can export filtered views for use with Pretalx again.

## 🚀 Features

* 📤 Assigns multiple reviewers per proposal
* 🔎 Filter assignments by reviewer or proposal ID
* 🔄 Re-generate assignments when needed
* 📦 Export to Pretalx-compatible format
* ✨ Colorful CLI output using [Rich](https://github.com/Textualize/rich)

## 🏗️ Project Structure

```
cfp/
├── app.py           # Click commands for assignments & filtering
├── assign.py        # Core logic for assigning reviewers
├── utils.py         # Data classes + file I/O
└── __main__.py      # CLI entry point
```

## 📂 Inputs

Make sure you have the following files (usually exported from Pretalx):

* `sessions.csv`: Contains the proposals (must include `ID`, `Proposal title`)
* `reviewers.csv`: Contains the reviewers (must include `Name`, `Email`)

## 🧪 Usage

### Create assignments

```bash
uv run python -m cfp assignments create
```

Options:

* `--sessions FILE`: Alternative path to a file containing all the session as
                     exported from Pretalx  [default: sessions.csv]
* `--reviewers FILE`: Alternative path to a file containing all the reviewers as
                      exported from Pretalx  [default: reviewers.csv]
* `--regen`: Regenerate the assignments even if they already exist
* `--verbose`: Print additional information about the assignments

### Filter assignments

```bash
uv run python -m cfp assignments filter --reviewer alice@example.com
uv run python -m cfp assignments filter --proposal proposal-123
uv run python -m cfp assignments filter --reviewer alice@example.com --pretalx
uv run python -m cfp assignments filter --reviewer alice@example.com --reviewer john@example.com
```

Options:

* `--proposal TEXT`: List of proposal IDs to filter assignments for
* `--reviewer TEXT`: List of rewviewer emails to filter assignments for
* `--pretalx`: Print objects that can be uploaded to Pretalx to add assignments

## 🧰 Development

Run linters, formatters and type checkers:

```bash
uv run ruff check
uv run ruff format
uv run mypy
```

## 📜 License

MIT License. See [`LICENSE`](./LICENSE) for more.

## 🙌 Acknowledgements

Built with ❤️ for the PyCon Greece Program Committee.
