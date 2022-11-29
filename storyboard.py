import pandas as pd
import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import random

tokenizer = AutoTokenizer.from_pretrained("cpierse/gpt2_film_scripts")
model = AutoModelForCausalLM.from_pretrained("cpierse/gpt2_film_scripts")

@st.cache
