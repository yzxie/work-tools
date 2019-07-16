msg_id=("1"  "2")
results=()
index=0
for str in ${msg_id[@]}; do
	params="{\"msg_id\": ${str}, \"registration_ids\":[\"xxxx\"]}"
	res=`curl -s --insecure -X POST -v https://report.jpush.cn/v3/status/message -H "Content-Type: application/json" -u "username:password" -d "${params}"`
	results[index]=$str+$res

	echo ${results[index]}
	index=$(($index+1))
done

for res in ${results[@]}; do
	echo $res
done

