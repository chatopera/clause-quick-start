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

if [ ! -z "$1" ]; then
    export CL_HOST=$1
fi

if [ ! -z "$2" ]; then
    export CL_PORT=$2
fi

if [ -z $CL_HOST ]; then
    source .env
    export CL_HOST=$CL_HOST
    export CL_PORT=$CL_PORT
fi

echo "set CL_HOST=$CL_HOST and CL_PORT=$CL_PORT, you can pass them with arguments."
echo "Usage: $0 YOUR_HOST YOUR_PORT"

sleep 3 # Give human hints

set -x
cd $baseDir/..
python bot.py
