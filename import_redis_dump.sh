#! bin/sh

DUMP_FILE=~/work/data/dump.rdb
REDIS_PORT=6379

function refresh_dump() {
  count=`ps -ef | grep redis | wc -l`
  if [ $count -gt 1 ]
  then
    echo "start stop redis..."
    redis-cli -p $REDIS_PORT shutdown
  fi
  
  cp $DUMP_FILE .
  if [ $? = 0 ]
  then
    redis-server ./redis.conf
  else
    echo "dump.rdb not found"
    exit 1
  fi
}

refresh_dump
