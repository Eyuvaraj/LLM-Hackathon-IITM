def read_env_file(file_path):
    env_vars = {}
    with open(file_path) as file:
        for line in file:
            # Strip whitespace and ignore lines that are comments or empty
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

# Read the .env file
env_vars = read_env_file('.env')
dev = env_vars.get("dev", "False").lower() in ("true", "1", "t")
hf_token = env_vars.get("HF_TOKEN")
groq_api_key = env_vars.get("GROQ_API_KEY")
nomic_api_key = env_vars.get("NOMIC_API_KEY")
api_key = env_vars.get("api_key")
base_url = env_vars.get("base_url")


print(f"dev: {dev}")
print(f"hf_token: {hf_token}")
print(f"groq_api_key: {groq_api_key}")
print(f"nomic_api_key: {nomic_api_key}")
print(f"api_key: {api_key}")
print(f"base_url: {base_url}")
