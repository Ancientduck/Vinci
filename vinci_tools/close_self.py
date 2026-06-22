import subprocess
import sys

def main():
    # Close VS Code
    # Close Vinci (python process)
    subprocess.run(['taskkill', '/f', '/im', 'ollama.exe'], capture_output=True)
    
    subprocess.run(['taskkill', '/f', '/im', 'cmd.exe'], capture_output=True)
    subprocess.run(['taskkill', '/f', '/im', 'Code.exe'], capture_output=True)
    subprocess.run(['taskkill', '/f', '/im', 'python.exe'], capture_output=True)
    
    
    print("Summary: VS Code and Vinci shut down.")

if __name__ == "__main__":
    main()