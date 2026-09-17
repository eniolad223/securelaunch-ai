"""Official Streamlit entry point for the SecureLaunch AI reviewer experience.

The approved interface remains in ``app_redesign.py`` so its completed visual
implementation stays isolated from the security-gateway package. Streamlit
executes this entry point again after every interaction, so the presentation
script must also be executed again instead of being loaded from Python's module
cache.
"""

from pathlib import Path
import runpy


runpy.run_path(str(Path(__file__).with_name("app_redesign.py")), run_name="__main__")
