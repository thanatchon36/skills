import re
import unicodedata


def slugify(title: str, max_len: int = 60) -> str:
    """Turn a title into a URL slug: lowercase ASCII words joined by hyphens."""
    text = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    words = re.findall(r"[a-z0-9]+", text.lower())
    slug = "-".join(words)
    return slug[:max_len].rstrip("-")
