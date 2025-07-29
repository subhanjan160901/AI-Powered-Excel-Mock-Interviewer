# src/local_llm_handler.py

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import streamlit as st

# Use Streamlit's cache to load the model and pipeline only once.
@st.cache_resource
def load_llm_pipeline():
    """
    Loads and caches the local LLM pipeline. This will run only once per session.
    We use Phi-2 because it's powerful but small enough for free cloud hardware.
    """
    print("--- Loading main LLM (microsoft/phi-2) for the first time. This may take several minutes... ---")
    model_name = "microsoft/phi-2"
    
    # Load the model with specific settings for better performance on a CPU
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        torch_dtype="auto", # Use a mix of precisions for performance
        device_map="auto",  # Automatically use CPU or GPU
        trust_remote_code=True
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    
    # Create a text-generation pipeline
    llm_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=300,  # Limit response length
        return_full_text=False
    )
    print("--- Main LLM loaded and cached successfully. ---")
    return llm_pipeline

def get_llm_response(prompt: str) -> str:
    """
    Gets a response from the cached local LLM pipeline.
    """
    llm_pipeline = load_llm_pipeline()
    
    # Format the prompt for the model
    # Note: Different models may need different prompt formats. This works for Phi-2.
    formatted_prompt = f"Instruct: {prompt}\nOutput:"

    print("AI: (Generating response with local LLM...)")
    try:
        outputs = llm_pipeline(formatted_prompt)
        response = outputs[0]["generated_text"]
        return response
    except Exception as e:
        print(f"Error during local LLM generation: {e}")
        return "Sorry, I encountered an error while generating a response."