import os
from dotenv import load_dotenv


def load_sqrt_env(env_file_name: str = ".env"):
    try:
        # {HOME}/.env_sqrt/.env
        env_file_path = os.path.join(os.environ.get("HOME"), ".env_sqrt", env_file_name)
        res = load_dotenv(dotenv_path = env_file_path, verbose=True, override=True)

        if not res:
            raise FileNotFoundError(f"Warning: {env_file_path} does not exist")
        
    except FileNotFoundError as fnfe:
        # let user know that .env file does not exist
        raise fnfe


if __name__ == "__main__":
    load_sqrt_env(".env")
    print(os.environ.get("SLACK_API_TOKEN"))
