"""Generate CLI documentation pages."""

from pathlib import Path

import mkdocs_gen_files

# Since NextCV doesn't have a CLI yet, this is a placeholder
# that can be extended when CLI functionality is added

root = Path(__file__).parent.parent

# Create a placeholder CLI documentation
with mkdocs_gen_files.open("cli/index.md", "w") as fd:
    print("# CLI Reference", file=fd)
    print("", file=fd)
    print("NextCV currently focuses on Python API usage. "
    "CLI tools will be added in future releases.", file=fd)
    print("", file=fd)
    print("For now, check out the [API Reference](../reference/) "
    "for all available functionality.", file=fd)
