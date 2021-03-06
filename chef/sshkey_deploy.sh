#!/bin/bash

# Usage: ./deploy.sh [host]

host="${1}"
key="${2:-dev}"

# The host key might change when we instantiate a new VM, so
# we remove (-R) the old host key from known_hosts
ssh-keygen -R "${host#*@}" 2> /dev/null

echo Dropping "$key" to /root/.ssh/key on "$host"

dir=`mktemp -d`
cp ~/.ssh/key/${key} $dir

rsync -avz -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" --progress $dir/* $host:/root/.ssh/key/

rm -r $dir

echo
echo Done
