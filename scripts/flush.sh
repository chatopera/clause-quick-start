#! /bin/bash 
###########################################
#
###########################################

# constants
baseDir=$(cd `dirname "$0"`;pwd)
# functions

# main 
[ -z "${BASH_SOURCE[0]}" -o "${BASH_SOURCE[0]}" = "$0" ] || return
cd $baseDir/..
docker-compose down
docker-compose rm

sudo rm -rf var/mysql/data/*
sudo rm -rf var/activemq/data/*
sudo rm -rf var/redis/data/*
sudo rm -rf var/local/workarea/*
