import os
import re

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
    except SubprocessError as e:
        logger.error(e)
    except OSError as e:
        logger.error(e)
    except ValueError(e):
        logger.error(e)
    except Exception as e:
        logger.error(e)

    return proc_stdout
