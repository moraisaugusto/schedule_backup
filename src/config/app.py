import os

import yaml
from cerberus import Validator

from src.log.logger import logger
from src.config.helper import replace_env_var, subprocess_cmd, ask_question


def setup():
    v = Validator()

    schema = {
        "name": {"type": "string", "required": True},
        "bkp_path": {"type": "string", "required": True},
        "dst_path": {"type": "string", "required": True},
        "max_files": {"type": "integer", "coerce": int, "required": True},
        "notification": {"type": "boolean", "coerce": bool, "required": True},
        "notification_url": {
            "type": "boolean", "coerce": bool, "required": False},
        "frequency": {"type": "string", "required": True},
        "username": {"type": "string", "required": True},
        "secrets_env": {"type": "string", "required": True}
    }

    questions = {
        "name": "App name: ",
        "bkp_path": "Backup path: ",
        "dst_path": "Destination path: ",
        "max_files": "Max backup files (5 default): ",
        "notification": (
            "Do you want to use the pushover service notification? (y/N): "),
        "frequency": "Frequency that backup will run: ",
        "username": "System user that will run this service: ",
        "secrets_env": "Secrets env file used for notification API: ",
        "notification_url": "Notification API url: "
    }

    while True:
        document = fill_info(questions)

        print("\n")
        for k, _ in questions.items():
            print(f"{questions[k]} \033[1m{document[k]}\033[0m")

        ask_question("\nIs this correct? (Y/n): ", True)

        if not v.validate(document, schema):
            logger.error(f"We found some error: {v.errors}")
        else:
            break

    document["name_title"] = document["name"].title()

    return document


def fill_info(questions, use_default_file=False):
    """Fill document with data of the app that will be backed up

    @param questions:  document to be configured
    @type  questions:  dict

    @return:  document validated
    @rtype :  dict

    @raise e:  None
    """
    yaml_filename = "default.yaml"
    exist_yaml_file = os.path.isfile(yaml_filename)

    use_yaml_file = False
    if exist_yaml_file:
        use_yaml_file = ask_question(
            "We found a YAML default, want to use it? (Y/n): ", True
        )

    document = dict()
    if use_yaml_file:
        with open(yaml_filename) as f:
            logger.info(
                "Found default yaml file. Automatically configuring params..."
            )
            yaml_data = yaml.safe_load(f)["default"]

        document["name"] = yaml_data["name"] or None
        document["bkp_path"] = replace_env_var(yaml_data["bkp_path"]) or None
        document["dst_path"] = replace_env_var(yaml_data["dst_path"]) or None
        document["max_files"] = yaml_data["max_files"] or 5
        document["frequency"] = replace_env_var(yaml_data["frequency"]) or "Mon 12:15"
        document["username"] = replace_env_var(yaml_data["username"]) or None
        document["secrets_env"] = replace_env_var(
            yaml_data["secrets_env"]) or None
        document["notification_url"] = yaml_data["notification_url"] or None
    else:
        document["name"] = input(questions["name"]) or None
        document["bkp_path"] = input(questions["bkp_path"]) or None
        document["dst_path"] = input(questions["dst_path"]) or None
        document["max_files"] = int(input(questions["max_files"]) or 5)
        document["frequency"] = replace_env_var(yaml_data["frequency"]) or "Mon 12:15"
        document["username"] = input(questions["username"]) or None
        document["secrets_env"] = input(questions["secrets_env"]) or None
        document["notification_url"] = input(
            questions["notification_url"]) or None

    confirmed = ask_question(questions["notification"], False)
    document["notification"] = confirmed

    return document


# REFACT: please refact me
def install(app_info):

    confirmed = ask_question(
        "Do you want to install the backup service? (y/N): ", False
    )

    if confirmed:
        base_systemctl_path = "{}/scripts/{}/schedule_{}_backup".format(
            os.getcwd(),
            app_info["name"],
            app_info["name"]
        )

        files = dict()
        for i in ["service", "timer"]:
            k = f"{i}_script"
            v = f"{base_systemctl_path}.{i}"
            files[k] = v

        systemctl_path = "/usr/lib/systemd/system/"
        for k, script_file in files.items():
            systemctl_script_path = "{}{}".format(
                systemctl_path, os.path.basename(script_file)
            )
            sudo_cmd = "sudo cp -p {} {} && sudo chown root:root {}".format(
                script_file,
                systemctl_path,
                systemctl_script_path
            )
            sudo_cmd_enable = "sudo systemctl enable {}".format(
                os.path.basename(script_file))
            sudo_cmd_start = "sudo systemctl start {}".format(
                os.path.basename(script_file))

            subprocess_cmd(sudo_cmd)
            subprocess_cmd(sudo_cmd_enable)
            subprocess_cmd(sudo_cmd_start)

        logger.success("Installed with success")
    else:
        logger.success("Scripts created but NOT installed")
