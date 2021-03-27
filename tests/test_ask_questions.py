import os
from src.config.helper import replace_env_var


def test_replace_env_var():
    os.environ["HOME"] = "/home/FAKEUSER"
    output = replace_env_var("$HOME/temp_dir")

    assert output == "/home/FAKEUSER/temp_dir"
    assert output != "$HOME/temp_dir"
