from src.log.logger import logger
from src.config.app import setup, install
from src.config.backup import create_bash_script
from src.config.schedule import create_systemctl_service, create_systemctl_timer


def main():
    app_info = setup()

    logger.info("Starting process...")

    create_bash_script(app_info)

    create_systemctl_service()
    create_systemctl_timer()


    install()


if __name__ == '__main__':
    main()




