from src.log.logger import logger
from src.config.app import setup, install
from src.config.backup import create_bash_script
from src.config.schedule import create_systemctl_service, create_systemctl_timer


def main():
    # app_info = setup()

    logger.info("Starting process...")
    app_info = {
        "name": "liferea",
        "bkp_path": "/home/augusto/.config/liferea",
        "dst_path": "/home/augusto/Development/schedule_backup/tmp",
        "max_files": 5,
        "notification": 1,
        "notification_url": "https://api.pushover.net/1/messages.json",
        "username": "USERNAME",
        "secrets_env": "/home/USER/.zshSecrets",
        "frequency": "Mon 13:15"
    }

    create_bash_script(app_info)
    create_systemctl_service(app_info)
    create_systemctl_timer(app_info)

    install()


if __name__ == '__main__':
    main()
