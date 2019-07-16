# 
msg_id=("1" "2")
reg_id=("1" "2")
results=()
index=0
for str in ${msg_id[@]}; do

  for str2 in ${reg_id[@]}; do
    a="{\"msg_id\": ${str}, \"registration_ids\":[\"${str2}\"]}"
    res=`curl -s --insecure -X POST -v https://report.jpush.cn/v3/status/message -H "Content-Type: application/json" -u "username:password" -d "${a}"`
    results[index]=$str+$res

    echo ${results[index]}
    index=$(($index+1))
  done
  
done

echo "======="
for res in ${results[@]}; do
  echo $res
done

