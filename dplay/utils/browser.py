"""
Browser utility.

Responsibility: open a URL in the system default browser.
"""

import webbrowser


# ------------------------------------------------------------------
# EXTENSIBLE METADATA
# ------------------------------------------------------------------
def open_browser(url: str):
    """
    Open the given URL in the system default browser.
    """

    print(f"Opening: {url}")
    webbrowser.open(url)
