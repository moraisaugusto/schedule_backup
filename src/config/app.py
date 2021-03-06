from cerberus import Validator

from src.log.logger import logger

def setup():
    v = Validator()

    schema = {
        "name": {"type": "string", "required": True},
        "bkp_path": {"type": "string", "required": True},
        "dst_path": {"type": "string", "required": True},
        "max_files": {"type": "integer", "coerce": int, "required": True},
        "notification": {"type": "boolean", "coerce": bool, "required": True},
    }

    document = {
        "name": None,
        "bkp_path": None,
        "dst_path": None,
        "max_files": None,
        "notification": None,
    }

    questions = {
        "name": "App name: ",
        "bkp_path": "Backup path: ",
        "dst_path": "Destination path: ",
        "max_files": "Max backup files (5 default): ",
        "notification": "Send notification? (y/N): ",
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

    return document

def fill_info(document, questions):

    document["name"] = input(questions["name"]) or None
    document["bkp_path"] = input(questions["bkp_path"]) or None
    document["dst_path"] = input(questions["dst_path"]) or None
    document["max_files"] = int(input(questions["max_files"]) or 5)

    answer = None
    while answer not in [True, False]:
        answer = True if input(questions["notification"]).lower() == "y" else False

        if isinstance(answer, bool):
            document["notification"] = int(answer)
            break

    return document


def install():
    logger.info("Do you want to install the backup service? (Y/n): ")
    logger.success("Installed with success")

