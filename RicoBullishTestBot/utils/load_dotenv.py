import sys
import os

from dotenv import dotenv_values
from dotenv import load_dotenv as l_dotenv


def load_dotenv (dotenv_path: str = ".env", verbose: bool = False, lower: bool = True, encoding: str = "utf-8") -> dict:
    """Load environment variables from .env2 file. by default this will create a dict with the keys being
    changed to lower case

    Args:
        dotenv_path (str, optional): Path to the .env2 file. Defaults to ".env2".
        verbose (bool, optional): Whether to print output. Defaults to False.
        lower (bool, optional): Whether to override existing to lower. Defaults to False.
        encoding (str, optional): The encoding of the .env2 file. Defaults to "utf-8".

    Returns:
        dict: A dictionary of the environment variables.
    """
    
    l_dotenv(dotenv_path=dotenv_path)
    
    env_dict = dotenv_values(dotenv_path=dotenv_path, verbose=verbose, encoding=encoding)
    
    if lower:
        env_dict = dict((k.lower(), v) for k, v in env_dict.items())
    
    if verbose:
        for k, v in env_dict.items():
            print(f"{k}={v}")
    
    return env_dict


def main ():
    # env_file = "/Users/rico.rojas/Development/RicoBullishTestBot/.env2"
    env_file = "BullishTechOps.env"
    blah = load_dotenv(dotenv_path=env_file, verbose=True)
    print(blah)


if __name__ == "__main__":
    sys.exit(main())
