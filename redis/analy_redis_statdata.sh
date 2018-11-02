#! /bin/sh

function list_calls() {
  for str in `cat redis_slow_statistic.txt | awk -F'=' '{print substr($2, 0, index($2, ",")-1), $0}' | sort -frh`
  do
    echo $str
  done
}

function list_total_cost_time() {
  for str in `cat redis_slow_statistic.txt | awk -F'=' '{print substr($3, 0, index($3, ",")-1), $0}' | sort -frh`
  do
    echo $str
  done
}

function list_each_cost_time() {
  for str in `cat redis_slow_statistic.txt | awk -F'=' '{print $4, $0}' | sort -frh`
  do
    echo $str
  done
}

if [ $# = 0 ]
then
  echo "usage: sh analy_redis_statdata.sh [calls | tct | ect] \n tct: total_cost_time, ect: each_cost_time"
else
  case $1 in
  calls)
    list_calls
    ;;
  tct)
    list_total_cost_time
    ;;
  ect)
    list_each_cost_time
    ;;
  *)
    list_each_cost_time
    ;;
  esac
fi
