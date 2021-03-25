import os
import re
import subprocess

from loguru import logger


def ask_question(question, default_answer=None):
    """Ask a question to the user

    @param question:  question to be displayed
    @type  question:  string

    @param default_answer:  default answer for the question
    @type  default_answer:  bool

    @return:  answer
    @rtype :  bool

    @raise e:  None
    """
    answers = {"y": True, "n": False}

    confirmed = None
    while not confirmed:
        confirmed = input(f"\033[1m{question}\033[0m").lower() or default_answer

        if isinstance(confirmed, bool):
            return confirmed
        if confirmed in ["y", "n"]:
            return answers[confirmed]
        confirmed = None

def replace_env_var(param):
    """Replace a string that contains a env variable

    @param param:  raw string that may have the env variable
    @type  param:  string

    @return:  string replaced
    @rtype :  string

    @raise e:  None
    """
    search_env_var = re.match("\$[A-Z0-1]+", param)
    param_replaced = param

    if search_env_var:
        env_var = search_env_var.group()
        env_var_value = os.getenv(env_var[1:])
        param_replaced = param.replace(env_var, env_var_value)

    return param_replaced

def subprocess_cmd(cmd):
    """execute a subprocess

    @param param:  command to be executed
    @type  param:  string

    @return:  result of the command
    @rtype :  string

    @raise e:  None
    """
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        proc_stdout = process.communicate()[0].strip()
    except subprocess.SubprocessError as e:
        logger.error(e)
    except OSError as e:
        logger.error(e)
    except ValueError(e):
        logger.error(e)
    except Exception as e:
        logger.error(e)

    return proc_stdout
