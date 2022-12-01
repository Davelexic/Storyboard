import pandas as pd
import numpy as np
import streamlit as st
import pickle
import base64
import tensorflow
import random
import torch
from diffusers import StableDiffusionPipeline
from transformers import AutoTokenizer, AutoModelForCausalLM



# Title Screen


# Page selection
#@st.cache

tokenizer = AutoTokenizer.from_pretrained("cpierse/gpt2_film_scripts")
model = AutoModelForCausalLM.from_pretrained("cpierse/gpt2_film_scripts")
model_id = "CompVis/stable-diffusion-v1-4"
device = "cuda" if torch.cuda.is_available() else "cpu"
app_mode = st.sidebar.selectbox('Select Page',['Home','Generate'])
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, revision="fp16")
pipe = pipe.to(device)


# Home Page

if app_mode == "Home":
    st.title('Capstone Three')
    st.title('Storyboard generation')
    st.write('Hello this is a test')
    email = st.sidebar.text_input('Email address')


    

#Script Generation Page
if app_mode== 'Generate':
    st.sidebar.multiselect('Pick your Genre:',['Action', 'Adventure', 'Comedy', 'Drama', 'Romance', 'Biography'])
    max_length= st.sidebar.slider('pick length:',500,2000)
    if st.sidebar.button("Generate Script"):
        st.echo()
        with st.echo():
            model.eval()
            num_samples = 3

            output = model.generate(
                        bos_token_id=random.randint(1,50000),
                        do_sample=True,   
                        top_k=50, 
                        max_length = max_length,
                        top_p=0.95, 
                        num_return_sequences=num_samples)

            decoded_output = []
            for sample in output:
                decoded_output.append(tokenizer.decode(
                sample, skip_special_tokens=True))
            st.write(decoded_output[0])
            #prompt = 'horse on a boat'
            #image1 = pipe(prompt).images[0]
            #st.image(image1)
            st.write(decoded_output[1])
            #st.image(decoded_output[1])
            st.write(decoded_output[2])
            #st.image(decoded_output[2])
            st.button('Download Script')




