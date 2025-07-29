# src/perplexity_detector.py

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import streamlit as st

# Load a pre-trained model and tokenizer. 
# This will be downloaded and cached the first time it's run.
# We use 'gpt2', a relatively small and effective model for this task.
# model_name = "gpt2"
# model = AutoModelForCausalLM.from_pretrained(model_name)
# tokenizer = AutoTokenizer.from_pretrained(model_name)

# --- NEW CACHED FUNCTION TO LOAD THE MODEL ---
@st.cache_resource
def load_model_and_tokenizer():
    """
    Loads the model and tokenizer and caches them in memory.
    This function will only run ONCE.
    """
    print("--- Loading model and tokenizer for the first time ---")
    model_name = "gpt2"
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print("--- Model and tokenizer loaded and cached ---")
    return model, tokenizer

# --- MODIFIED FUNCTION ---
def calculate_perplexity(text: str) -> float:
    """
    Calculates the perplexity of a given text using the cached model.
    """
    # Load the model and tokenizer from the cache
    model, tokenizer = load_model_and_tokenizer()

    encodings = tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**encodings, labels=encodings["input_ids"])
        neg_log_likelihood = outputs.loss

    ppl = torch.exp(neg_log_likelihood)
    return ppl.item()

def is_ai_generated(text: str, threshold: float = 40.0) -> bool:
    """
    Checks if a text is likely AI-generated based on a perplexity threshold.
    
    Args:
        text (str): The text to analyze.
        threshold (float): The perplexity value below which text is considered AI-generated.
                           This value may require tuning.
                           
    Returns:
        bool: True if the perplexity is below the threshold, False otherwise.
    """
    if not text:
        return False
        
    print("AI: (Calculating perplexity...)")
    perplexity = calculate_perplexity(text)
    print(f"AI: (Perplexity score: {perplexity:.2f}, Threshold: {threshold})")
    
    # If perplexity is lower than our threshold, it's likely AI-generated
    return perplexity < threshold