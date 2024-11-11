import yaml
import os

def find_yaml_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for file in os.listdir(script_dir):
        if file.endswith(".yaml"):
            return os.path.join(script_dir, file)
    raise FileNotFoundError("No YAML file found in the script's directory.")

def load_endpoints_from_yaml(file_path):
    with open(file_path, 'r') as file:
        endpoints = yaml.safe_load(file)
    return {endpoint["name"]: endpoint for endpoint in endpoints}

def main():
    try:
        yaml_file = find_yaml_file()
        print(f"YAML file found: {yaml_file}")
        endpoints = load_endpoints_from_yaml(yaml_file)

        for name, endpoint in endpoints.items():
            print(name, endpoint)

    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    main()