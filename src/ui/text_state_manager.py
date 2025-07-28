import streamlit as st
from typing import Dict

class TextStateManager:
    """A utility class to manage multiple text states in Streamlit session state."""
    
    def __init__(self):
        self._initialize_states()
    
    def _initialize_states(self):
        """Initialize the text states dictionary if it doesn't exist."""
        if 'text_states' not in st.session_state:
            st.session_state.text_states = {
                'resume_text': "",
                'job_description': ""
            }
    
    def set_text(self, key: str, value: str) -> None:
        """Set text for a specific key."""
        if 'text_states' not in st.session_state:
            self._initialize_states()
        st.session_state.text_states[key] = value
    
    def get_text(self, key: str) -> str:
        """Get text for a specific key."""
        if 'text_states' not in st.session_state:
            self._initialize_states()
        return st.session_state.text_states.get(key, "")
    
    def get_all_texts(self) -> Dict[str, str]:
        """Get all text states."""
        if 'text_states' not in st.session_state:
            self._initialize_states()
        return st.session_state.text_states
    
    def clear_text(self, key: str) -> None:
        """Clear text for a specific key."""
        if 'text_states' in st.session_state and key in st.session_state.text_states:
            st.session_state.text_states[key] = ""
    
    def clear_all_texts(self) -> None:
        """Clear all text states."""
        if 'text_states' in st.session_state:
            for key in st.session_state.text_states:
                st.session_state.text_states[key] = ""
    
    def has_text(self, key: str) -> bool:
        """Check if a specific key has non-empty text."""
        return bool(self.get_text(key).strip())
    
    def get_non_empty_texts(self) -> Dict[str, str]:
        """Get only the text states that have content."""
        all_texts = self.get_all_texts()
        return {key: value for key, value in all_texts.items() if value.strip()}
    
    def add_new_text_type(self, key: str, initial_value: str = "") -> None:
        """Add a new text type to the states."""
        if 'text_states' not in st.session_state:
            self._initialize_states()
        if key not in st.session_state.text_states:
            st.session_state.text_states[key] = initial_value

# Create a global instance
text_manager = TextStateManager()
