import streamlit_mermaid as stmd
import streamlit as st

code = """
    flowchart TD
        A[Christmas] -->|Get money| B(Go shopping)
        B --> C{Let me think}
        C -->|One| D[Laptop]
        C -->|Two| E[iPhone]
        C -->|Three| F[fa:fa-car Car]
"""

mermaid = stmd.st_mermaid(code)
