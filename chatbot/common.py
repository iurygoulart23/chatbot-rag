import subprocess

def get_path_projeto():
    path = subprocess.run('pwd', shell=True, capture_output=True, text=True).stdout.strip()
    return path
