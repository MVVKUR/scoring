from pyngrok import ngrok
import subprocess
import os

# Specify the port you want to run Streamlit on
PORT = 8501

# 1. Start ngrok tunnel on the same port as Streamlit
public_url = ngrok.connect(PORT).public_url
print("ngrok tunnel URL:", public_url)

# 2. Run Streamlit with subprocess
streamlit_command = f"streamlit run app.py --server.port {PORT}"
process = subprocess.Popen(streamlit_command, shell=True)

# Keep the process running
process.wait()
