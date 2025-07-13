import os
import subprocess

def run_streamlit():
    # Lanza la app de Streamlit ubicada en src/gui/app.py
    subprocess.run(["streamlit", "run", "src/gui/app.py"])

if __name__ == "__main__":
    run_streamlit()
