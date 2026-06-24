import sys
import importlib
import subprocess
from pathlib import Path


DEFAULT_EXTERNAL_MODULES = ['f90nml', 'cdsapi']

def import_extrernal_modules (extra_module_names = DEFAULT_EXTERNAL_MODULES):
    for module_name in extra_module_names:
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            print(f"'{module_name}' exists.")
        else:
            print(f"'{module_name}' does not exist.")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
            print(f"'{module_name}' installed ")
        importlib.import_module (module_name)


def init_CDS (url = None, key = None):
    if url is None:
        url = input("Enter the URL of the CDS API: ")
    if key is None:
        key = input("Enter your API key: ")
    # Locate the user's home directory across Linux, macOS, or Windows
    home_dir = Path.home()
    config_file = home_dir / ".cdsapirc"
    
    # Format the content precisely as required by the CDS API
    config_content = f"url: {url}\nkey: {key}\n"
    
    # Write the configuration file
    with open(config_file, "w", encoding="utf-8") as f:
        f.write(config_content)