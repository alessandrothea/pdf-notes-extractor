# PDF Annotation Extractor

Extract annotations (highlights, comments, notes, strikethroughs, etc.) from PDF files and export them to **Markdown**, **plain text**, or **Microsoft Word**.

## Setup

```bash
cd pdf-annotation-extractor
uv sync
```

## Usage

```bash
# Default — Markdown output
uv run extract-pdf-annotations report.pdf

# Choose a format
uv run extract-pdf-annotations report.pdf -f txt
uv run extract-pdf-annotations report.pdf -f docx
uv run extract-pdf-annotations report.pdf -f all

# Custom output path
uv run extract-pdf-annotations report.pdf -f docx -o my_notes.docx

# Preview in terminal (rich table, no file written)
uv run extract-pdf-annotations report.pdf --list-only
```

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--format` | `-f` | `markdown` (default), `md`, `txt`, `text`, `docx`, `word`, `all` |
| `--output` | `-o` | Output file path (auto-named next to the PDF if omitted) |
| `--list-only` | `-l` | Print a rich table to the terminal without writing any file |
