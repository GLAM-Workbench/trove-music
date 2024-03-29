import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import nbformat
import re

AuthorInfo = Dict[str, str]


LISTIFY = ["author", "object", "result"]

def listify(value):
    if not isinstance(value, list):
        return [value]
    return value

def extract_notebook_title(nb):
    md_cells = [c for c in nb.cells if c["cell_type"] == "markdown"]
    for cell in md_cells:
        if title := re.search(r"^# (.+)(\n|$)", cell["source"]):
            return title.group(1)

def extract_notebook_metadata(notebook: Path, keys: Dict[str, Any]) -> Dict[str, Any]:
    """Attempts to extract metadata from the notebook.

    Parameters:
        notebook: The path to the jupyter notebook
        keys: A dictionary of keys to look for in the notebook, and their
            corresponding defaults if the key is not found.

    Returns:
        A dictionary containing the retrieved metadata for each key.
    """
    result = {}
    nb = nbformat.read(notebook, nbformat.NO_CONVERT)
    metadata = nb.metadata.rocrate
    for key, default in keys.items():
        if key in LISTIFY:
            result[key] = listify(metadata.get(key, default))
        else:
            result[key] = metadata.get(key, default)
    return result

