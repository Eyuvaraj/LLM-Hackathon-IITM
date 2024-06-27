import os

def read_env_file(file_path):
    env_vars = {}
    try:
        with open(file_path) as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
        return env_vars
    except:
        print('Error! No .env found\n\nPlease copy the .env-sample file and rename it to .env. And set the necessary environment variables✌️\n')

env_vars = read_env_file('.env')

# Fetch the environment variables, prefers the one set in the environment over the one set in the .env file
dev = os.environ.get("dev", "False").lower() in ("true", "1", "t") or env_vars.get("dev", "False").lower() in ("true", "1", "t")
hf_token = os.environ.get("HF_TOKEN") or env_vars.get("HF_TOKEN")
groq_api_key = os.environ.get("GROQ_API_KEY") or env_vars.get("GROQ_API_KEY")
nomic_api_key = os.environ.get("NOMIC_API_KEY") or env_vars.get("NOMIC_API_KEY")
api_key = os.environ.get("api_key") or env_vars.get("api_key")
base_url = os.environ.get("base_url") or env_vars.get("base_url")
llm_model = os.environ.get("llm_model") or env_vars.get("llm_model")


# print(f"dev: {dev}")
# print(f"hf_token: {hf_token}")
# print(f"groq_api_key: {groq_api_key}")
# print(f"nomic_api_key: {nomic_api_key}")
# print(f"api_key: {api_key}")
# print(f"base_url: {base_url}")
# print(f"llm_model: {llm_model}")