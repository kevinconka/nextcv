# NextCV Documentation

This directory contains the documentation for NextCV, built with MkDocs and Material theme.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- uv (recommended) or pip

### Install Dependencies

```bash
# Using uv (recommended)
uv sync --all-extras

# Or with pip
pip install -e ".[docs]"
```

### Build Documentation

```bash
# Build static site
mkdocs build

# Serve locally for development
mkdocs serve
```

### Deploy to GitHub Pages

```bash
# Deploy to GitHub Pages (requires push access)
mkdocs gh-deploy
```

## 📁 Structure

```
docs/
├── ...
├── includes/             # Shared content
│   └── abbreviations.md  # Abbreviations
├── gen_ref_pages.py      # Auto-generate API reference
└── gen_cli_pages.py      # Auto-generate CLI docs
```

## 🛠️ Development

### Adding New Pages

1. Create a new `.md` file in the appropriate directory
2. Add it to the `nav` section in `mkdocs.yml`
3. Use the existing pages as templates

### Auto-Generated Content

- **API Reference**: Generated from Python docstrings using `gen_ref_pages.py`
- **CLI Documentation**: Generated using `gen_cli_pages.py`

## 🔧 Configuration

The documentation is configured in `mkdocs.yml`:

- **Theme**: Material with custom fonts and features
- **Plugins**: Search, auto-refs, minification, git integration
- **Extensions**: Code highlighting, admonitions, tabs, etc.

## 🚀 Deployment

Documentation is automatically deployed to GitHub Pages when:

- Pushing to `main` branch

The deployment is handled by the GitHub Actions workflow in `.github/workflows/docs.yml`.

## 🤝 Contributing

1. Make changes to the documentation
2. Test locally with `mkdocs serve` or `uv run mkdocs serve`
3. Submit a pull request
4. Documentation will be automatically deployed on merge

---

For more information, see the [MkDocs documentation](https://www.mkdocs.org/) and [Material theme documentation](https://squidfunk.github.io/mkdocs-material/).
