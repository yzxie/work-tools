#! /bin/sh

#REDIS_SLOW_LOG=./24_redis_slow_log.txt
#REDIS_SLOW_LOG=./17_csp_redis_slow_log.txt
#REDIS_SLOW_LOG=./17_csp_slow_log_201810111530.txt
#REDIS_SLOW_LOG=./24_csp_slow_log_201810111603.txt
#REDIS_SLOW_LOG=./20_csp_slow_log_201810111637.txt
#REDIS_SLOW_LOG=./24_redis_slow_log_201810112148.txt
#REDIS_SLOW_LOG=./20_redis_slow_log_201810112156.txt
#REDIS_SLOW_LOG=./now_redis_slow.log
#REDIS_SLOW_LOG=./24_redis_slow_log_201810121003.txt
#REDIS_SLOW_LOG=./24_redis_slow_log_201810112343.txt
#REDIS_SLOW_LOG=./24_redis_slow_log_201810121647.txt
#REDIS_SLOW_LOG=./20_redis_slow_log_201810160027.txt
#REDIS_SLOW_LOG=./20_redis_slow_log_201810230018.txt
#REDIS_SLOW_LOG=./20_redis_slow_log_201810230036.txt
#REDIS_SLOW_LOG=./20_redis_slow_log_201810231350.txt
#REDIS_SLOW_LOG=./20_redis_slow_log_201810231634.txt
#REDIS_SLOW_LOG=./20_redis_slow_log_201810232355.txt
REDIS_SLOW_LOG=./20_redis_slow_log_201810252235.txt
function show_slow_log_human() {
  # timestamp
  i=1
  ts_array=()
  for ts in `cat $REDIS_SLOW_LOG | grep '2) (integer) ' | awk '{print $3}'`
  do
  	timestamp=`date -r $ts`
    #echo "$i: $timestamp"
    ts_array[i]=`date -r $ts | awk '{print $1, $3}'`
    i=$[i+1]
  done

  # cost time
  i=1
  ct_array=()
  for ct in `cat $REDIS_SLOW_LOG | grep '3) (integer) ' | awk '{print $3}'`
  do
  	cost_time=$[$ct/1000]
  	#echo "$i: ${cost_time}ms"
  	ct_array[i]=$cost_time
  	i=$[i+1]
  done

  # command
  i=1
  cd_array=()
  for cd in `cat $REDIS_SLOW_LOG | grep '4) 1) "' | awk '{print $3}'`
  do
  	cd_array[i]=$cd
  	i=$[i+1]
  done

  # redis key
  i=1
  rk_array=()
  for rk in `cat $REDIS_SLOW_LOG | grep '2) "' | awk '{print $2}'`
  do
  	rk_array[i]=$rk
  	i=$[i+1]
  done

  for ((j=0; j<"${#ct_array[*]}";j=j+1))
  do
  	echo "${ts_array[$j]}, ${cd_array[$j]}:${rk_array[$j]}, ${ct_array[$j]}ms"
  done
}

show_slow_log_human
