def validate_github_url(url: str) -> bool:
    """
    Simple utility to check if the provided string looks like a GitHub link.
    """
    return url.strip().startswith("https://github.com/")