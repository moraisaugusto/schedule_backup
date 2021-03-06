import os
import subprocess

from cerberus import Validator

from src.log.logger import logger

def setup():
    v = Validator()

    schema = {
        "name": {"type": "string", "required": True},
        "name_title": {"type": "string", "required": True},
        "bkp_path": {"type": "string", "required": True},
        "dst_path": {"type": "string", "required": True},
        "max_files": {"type": "integer", "coerce": int, "required": True},
        "notification": {"type": "boolean", "coerce": bool, "required": True},
        "username": {"type": "string", "required": True},
        "secrets_env": {"type": "string", "required": True}
    }

    document = {
        "name": None,
        "bkp_path": None,
        "dst_path": None,
        "max_files": None,
        "notification": None,
        "username": None,
        "secrets_env": None,
        "notification_url": None
    }

    questions = {
        "name": "App name: ",
        "bkp_path": "Backup path: ",
        "dst_path": "Destination path: ",
        "max_files": "Max backup files (5 default): ",
        "notification": "Send notification? (y/N): ",
        "username": "System user that will run this service: ",
        "secrets_env": "Secrets env file used for notification API: ",
        "notification_url": "Notification API url: "
    }

    confirmed = False
    while not confirmed :
        document = fill_info(document, questions)

        print("\n")
        for k, _ in questions.items():
            print(f"{questions[k]} {document[k]}")

        confirmed = False if input("\nIs this correct? (Y/n): ").lower() == "n" else True
        if not v.validate(document, schema):
            confirmed = False
            logger.error("There are errors in the following field(s): ", v.errors())

    document["name_title"] = document["name"].title()

    return document

def fill_info(document, questions):

    document["name"] = input(questions["name"]) or None
    document["bkp_path"] = input(questions["bkp_path"]) or None
    document["dst_path"] = input(questions["dst_path"]) or None
    document["max_files"] = int(input(questions["max_files"]) or 5)
    document["username"] = input(questions["username"]) or None
    document["secrets_env"] = input(questions["secrets_env"]) or None
    document["notification_url"] = input(questions["notification_url"]) or None

    answer = None
    while answer not in [True, False]:
        answer = True if input(questions["notification"]).lower() == "y" else False

        if isinstance(answer, bool):
            document["notification"] = int(answer)
            break

    return document


# REFACT: please refact me
def install(app_info):
    question = "Do you want to install the backup service? (Y/n): "

    answer = None
    while answer not in [True, False]:
        answer = True if input(question).lower() == "y" else False

        if isinstance(answer, bool):
            break

    if answer:
        files = {
            "service_script": "{}/scripts/{}/schedule_{}_backup.service".format(
                os.getcwd(),
                app_info["name"],
                app_info["name"]
            ),
            "timer_script": "{}/scripts/{}/schedule_{}_backup.timer".format(
                os.getcwd(),
                app_info["name"],
                app_info["name"]
            )
        }

        systemctl_path = "/usr/lib/systemd/system/"
        for k, script_file in files.items():
            systemctl_script_path = "{}{}".format(systemctl_path, os.path.basename(script_file))
            sudo_cmd = "sudo cp -p {} {} && sudo chown root:root {}".format(
                script_file,
                systemctl_path,
                systemctl_script_path
            )
            sudo_cmd_enable = "sudo systemctl enable {}".format(os.path.basename(script_file))
            sudo_cmd_start = "sudo systemctl start {}".format(os.path.basename(script_file))

            subprocess_cmd(sudo_cmd)
            if k == "timer_script":
                subprocess_cmd(sudo_cmd_enable)
                subprocess_cmd(sudo_cmd_start)

    logger.success("Installed with success")


def subprocess_cmd(cmd):
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
