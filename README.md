# Schedule Backup
Schedule Backup is a backup helper application that creates a simple bash backup script and the systemctl service/timer files. You can use it to backup your data application from time to time.

Example: Let's suppose that you are using the [Zotero](https://www.zotero.org/) app to organize your Scientific and Books. You can use the Schedule Backup to backup your data folder and save it into a [NextCloud](https://nextcloud.com/) or [Google Drive](https://drive.google.com/) account.


![Schedule Backup](https://raw.githubusercontent.com/moraisaugusto/schedule_backup/main/media/schedule_backup.gif)

## How to Install


Clone the repository

```bash
git clone https://github.com/moraisaugusto/schedule_backup.git
```

Install python dependences

```bash
pip install -r requirements.txt
```

### How to use

Edit the `default.yml` file and configure your backup application
```bash
default:
  name: my_app
  bkp_path: $HOME/my_app_data
  dst_path: $HOME/my_app_data_dst_folder
  max_files: 5
  notification: 1
  notification_url: https://api.pushover.net/1/messages.json
  username: $USER
  secrets_env: $HOME/.secrets
  frequency: Mon 13:15
```

NOTE: Schedule Backup can understand environment variables. So you can use `$HOME` variable

