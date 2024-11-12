import yaml
import requests
import os
import time

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

def check_health(endpoint):
    url = endpoint.get("url")
    method = endpoint.get("method", "GET").upper()
    headers = endpoint.get("headers", {})
    body = endpoint.get("body")
    json_body = yaml.safe_load(body) if body else None
    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, json=json_body, timeout=0.5)
        latency = (time.time() - start_time) * 1000
        if 200 <= response.status_code < 300 and latency < 500:
            return "UP", latency
        else:
            return "DOWN", latency
    except (requests.RequestException, requests.Timeout):
        return "DOWN", None

def main():
    try:
        yaml_file = find_yaml_file()
        print(f"YAML file found: {yaml_file}")
        endpoints = load_endpoints_from_yaml(yaml_file)
        print("Starting health checks... Press Ctrl+C to exit.")
        while True:
            for name, endpoint in endpoints.items():
                status, latency = check_health(endpoint)
                if latency is not None:
                    print(f"{name} - {status} (Latency: {latency:.2f} ms)")
                else:
                    print(f"{name} - {status} (No response)")

            time.sleep(15)
    except FileNotFoundError as e:
        print(e)
    except KeyboardInterrupt:
        print("\nHealth check terminated by user.")

if __name__ == "__main__":
    main()