import numpy as np
from scipy.io.wavfile import write
import gradio as gr
from math import sqrt
import tempfile
import os

phi = (1 + sqrt(5)) / 2

def generate_song(user_input):
    binary = ''.join(format(ord(c), '08b') for c in str(user_input))
    
    duration = 60
    sample_rate = 44100
    total_samples = int(duration * sample_rate)
    signal = np.zeros(total_samples)

    t = np.arange(total_samples)
    freq = 120.0

    for i in range(total_samples):
        bit_index = i % len(binary)
        bit = binary[bit_index]
        freq += (phi if bit == '1' else -1/phi) * 0.06
        signal[i] = np.sin(2 * np.pi * freq * i / sample_rate)

    signal = signal / np.max(np.abs(signal)) * 0.85

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        write(tmp.name, sample_rate, signal.astype(np.float32))
        return tmp.name

with gr.Blocks() as demo:
    gr.Markdown("# Heart Song Generator")
    gr.Markdown("Enter any text or number to hear its unique continuous frequency evolution.")
    
    input_text = gr.Textbox(label="Input", placeholder="Jesus is the Christ or 888")
    output_audio = gr.Audio(label="Your Heart Song")
    
    btn = gr.Button("Generate Song")
    btn.click(generate_song, inputs=input_text, outputs=output_audio)

demo.launch()
