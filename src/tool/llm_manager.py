from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain.schema.output_parser import StrOutputParser
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables with priority
def load_env_files():
    """Load environment files with priority: .env.local first, then .env"""
    if os.path.exists('.env.local'):
        load_dotenv('.env.local')
        print("Loaded .env.local file")
    elif os.path.exists('.env'):
        load_dotenv('.env')
        print("Loaded .env file")
    else:
        print("No environment file found")

# Load environment variables
load_env_files()

class LLMManager:
    """Manager multiple LLM providers"""

    def __init__(self) -> None:
        self.providers = {
            "OpenAI": {
                "models": ["gpt-4o-mini"],
                "requires_api_key": True
            },
            "Google": {
                "models": ["gemini-2.5-flash"],
                "requires_api_key": True
            },
            "Ollama": {
                "models": ["gemma3n:latest", "gemma3n:e4b"],
                "requires_api_key": False
            }
        }

    def get_llm(self, provider: str, model: str, api_key: Optional[str] = None) -> BaseLanguageModel:
        """
        Get LLM instance based on provider and model.
        Parameters
        ----------
        provider : str
            Name of the prover in form of string. Ex: OpenAI, Google and Ollama. 
        model : str
            Provide the name of the model that user want to use inside the the project. Ex: gemini-2.5-flash, gpt-4o-mini and so on.
        api_key : Optional[str] = None
            Values require for API_Key value or not.
        Returns
        -------
        resume_model : Personal
                This will return the value of personal in formatted way of pydantic.
        """

        if provider == "OpenAI":
            if not api_key:
                raise ValueError("OpenAI API key is required")
            return ChatOpenAI(
                model=model,
                api_key=api_key,
                temperature=0.5
            )
        elif provider == "Google":
            if not api_key:
                raise ValueError("Google API key is required")
            return ChatGoogleGenerativeAI(
                model=model,
                api_key=api_key
            )
        elif provider == "Ollama":
            return ChatOllama(
                model=model,
                temperature=0
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def init_llm_chain(self, prompt: PromptTemplate) -> Runnable:
        """
        Initialize LLM chain with selected provider and model.
        Parameters
        ----------
        prompt : PromptTemplate
            Provide the prompt to give inside the chat model.
        Returns
        -------
        chain : Runnable
                This will return the value of chains in form of Runnable.
        """
        # Get API keys from environment
        openai_api_key = os.getenv('OPENAI_API_KEY')
        google_api_key = os.getenv('GOOGLE_API_KEY')
        
        # Get LLM config from session state or use defaults
        llm_config = st.session_state.get("llm_config", {
            'provider': os.getenv('DEFAULT_LLM_PROVIDER', 'Ollama'),
            'model': os.getenv('DEFAULT_LLM_MODEL', 'gemma3n:e4b'),
            'api_key': None
        })
        
        # Set API key based on provider
        if llm_config['provider'] == 'OpenAI':
            llm_config['api_key'] = openai_api_key
        elif llm_config['provider'] == 'Google':
            llm_config['api_key'] = google_api_key
        
        if not llm_config:
            raise ValueError("LLM configuration not found")
        
        try:
            llm = self.get_llm(
                provider=llm_config['provider'],
                model=llm_config['model'],
                api_key=llm_config.get('api_key')
            )
            chain: Runnable = prompt | llm | StrOutputParser()
            return chain
        except Exception as e:
            if 'st' in globals():
                st.error(f"Failed to initialize LLM: {str(e)}")
            raise e

    def cleanup_llm_output(self, raw_output: str) -> str:
        """Clean up LLM output to extract pure JSON"""
        if raw_output.startswith("```json"):
            raw_output = raw_output[len("```json"):].lstrip()
        if raw_output.endswith("```"):
            raw_output = raw_output[:-3].rstrip()
        return raw_output.strip()

    def get_available_models(self, provider: str) -> list:
        """Get available models for a provider"""
        return self.providers.get(provider, {}).get("models", [])

    def requires_api_key(self, provider: str) -> bool:
        """Check if provider requires API key"""
        return self.providers.get(provider, {}).get("requires_api_key", False)

llm_manager = LLMManager()