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
    question = f"\033[1m{question}\033[0m"
    answer = input(question).lower() or default_answer

    while True:
        if answer in ["y", "n"]:
            return answers[answer]
        elif answer == default_answer:
            return default_answer
        else:
            answer = input(question).lower() or default_answer

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

    @param cmd:  command to be executed
    @type  cmd:  string

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
    except ValueError as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)
    finally:
        SystemExit("Aborting...")

    return proc_stdout
