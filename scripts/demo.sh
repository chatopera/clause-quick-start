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

if [ ! -z "$3" ]; then
    export CL_PROFILE=$3
fi

if [ -z $CL_HOST ]; then
    if [ -f .env ]; then
        echo "load environ from .env"
        source .env
    fi
fi

export CL_HOST=${CL_HOST:-localhost}
export CL_PORT=${CL_PORT:-8056}
export CL_PROFILE=${CL_PROFILE:-profile.json}

echo "set CL_HOST=$CL_HOST, CL_PORT=$CL_PORT and CL_PROFILE=$CL_PROFILE, you can pass them with arguments."
sleep 3 # Give human hints

set -x
cd $baseDir/..
python bot.py
