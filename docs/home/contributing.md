# Contributing to NextCV

First off, thank you for considering contributing to NextCV! We welcome all contributions, from bug fixes to new features and documentation improvements.

## 🚀 How to Contribute

!!! tip "Quick Setup"
    We use [uv](https://github.com/astral-sh/uv) as our package manager - it's like pip, but much faster! Learn more in the [uv documentation](https://github.com/astral-sh/uv#readme).

We recommend following this workflow to contribute:

1.  **Fork the repository:** Create your own copy of the project.
2.  **Create a feature branch:** `git checkout -b my-new-feature`
3.  **Set up the development environment:**
    ```bash
    # Install dependencies with uv (blazing fast Python package manager)
    uv sync

    # Install pre-commit hooks
    uvx pre-commit install
    ```
4.  **Make your changes:** Write your code and add tests for it.
5.  **Run tests and code quality checks:**
    ```bash
    # Run tests
    uv run pytest

    # Run pre-commit checks
    uvx pre-commit run --all-files
    ```
6.  **Commit your changes:** `git commit -m 'Add some feature'`
7.  **Push to your branch:** `git push origin my-new-feature`
8.  **Submit a pull request:** Open a pull request from your fork to the main NextCV repository.

## 💡 What to Contribute

!!! example "Contribution Ideas"
    Not sure where to start? Here are a few ideas:

    - **🐛 Bug fixes:** Look for open issues with the `bug` label.
    - **✨ New features:** Propose a new feature by opening an issue to discuss it first.
    - **📚 Documentation:** Improve the documentation, add examples, or write tutorials.
    - **⚡️ Performance improvements:** Find bottlenecks and optimize them.
