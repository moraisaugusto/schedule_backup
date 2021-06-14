#!/usr/bin/env sh

# Backup script for %%name%%
tmp_dir=$HOME/.tmp

app="%%name%%"
date=`date +"%Y%m%d_%H%M%S"`
num_backups=%%max_files%%
backup_path="%%bkp_path%%"
dest_path="%%dst_path%%"
notification=%%notification%%

basename=`basename $backup_path`
success=false

msg_success="%%app_title%% backup done in ${app}_${date}.tgz"
msg_failed="%%app_title%% backup FAILED"

backup_file="${tmp_dir}/${app}_${date}.tgz"
echo "Backing %%app_title%% data... $backup_path"
cd $backup_path/.. && tar -zcf $backup_file $basename && mv $backup_file $dest_path && msg=$msg_success || msg=$msg_failed
echo $msg

# TODO: create feature
if [ $upload_nextcloud == 1 ] ; then
    curl -T  ${output_dir}/${app}_${date}.tgz -u '$NEXTCLOUD_USER:NEXTCLOUD_PASS' $NEXTCLOUD_URL
fi

# Backup rotate
files=($(ls -t ${dest_path}/%%name%%_*))
num_files=${#files[@]}

if [ $num_files -gt $num_backups ] ; then
    for (( i=0; i<$num_backups; i++ )); do unset files[$i] ; done
    rm ${files[@]}
fi

# Pushover notification
if [ $notification == 1 ] ; then
    source %%secrets_env%%
    curl -s \
    --form-string "token=$PUSHOVER_TOKEN" \
    --form-string "user=$PUSHOVER_USER" \
    --form-string "message=$msg" \
    %%notification_url%%
fi
