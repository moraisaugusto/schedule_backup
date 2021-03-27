import os

from src.log.logger import logger


def create_bash_script(app_info):
    script_folder = "./scripts/{}".format(app_info["name"])
    full_script_path = "{}/{}.sh".format(script_folder, app_info["name"])

    os.makedirs(script_folder, mode=0o755, exist_ok=True)
    default_file = open("./templates/default.sh", "r").read()

    app_info["app_title"] = app_info["name"].title()

    for k, v in app_info.items():
        search_for = "%%{}%%".format(str(k))
        replace_with = str(v)
        default_file = default_file.replace(search_for, replace_with)

    try:
        with open(full_script_path, "w") as handle:
            os.chmod(full_script_path, 0o766)
            handle.write(default_file)
    except OSError as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)

    logger.success("Created Bash script for: {}".format(app_info["name"]))
    return True
