import os

from src.log.logger import logger


def create_systemctl_service(app_info):
    script_folder = "scripts/{}".format(app_info["name"])
    full_script_path = "{}/{}/schedule_{}_backup.service".format(
        os.getcwd(), script_folder, app_info["name"])
    app_bash_script = "{}/scripts/{}/{}.sh".format(os.getcwd(),
                                                   app_info["name"],
                                                   app_info["name"])

    default_file = open("./templates/default_systemctl.service", "r").read()

    app_info["app_bash_script"] = app_bash_script

    for k, v in app_info.items():
        search_for = "%%{}%%".format(str(k))
        replace_with = str(v)
        default_file = default_file.replace(search_for, replace_with)

    try:
        with open(full_script_path, "w") as handle:
            os.chmod(full_script_path, 0o644)
            handle.write(default_file)
    except OSError as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)

    logger.success(f"Created systemctl service script for: {app_info['name']}")


def create_systemctl_timer(app_info):
    script_folder = "scripts/{}".format(app_info["name"])
    full_script_path = "{}/{}/schedule_{}_backup.timer".format(
        os.getcwd(), script_folder, app_info["name"])
    app_bash_script = "{}/scripts/{}/{}.sh".format(os.getcwd(),
                                                   app_info["name"],
                                                   app_info["name"])

    default_file = open("./templates/default_systemctl.timer", "r").read()

    app_info["app_bash_script"] = app_bash_script

    for k, v in app_info.items():
        search_for = "%%{}%%".format(str(k))
        replace_with = str(v)
        default_file = default_file.replace(search_for, replace_with)

    try:
        with open(full_script_path, "w") as handle:
            os.chmod(full_script_path, 0o644)
            handle.write(default_file)
    except OSError as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)

    logger.success("Created systemctl Service script")
    logger.success("Created systemctl Timer script")
