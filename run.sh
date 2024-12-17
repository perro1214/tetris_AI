#!/bin/bash
if [ $# -eq 0 ]; then
    echo "引数が指定されていません。デフォルトの5回繰り返し動作を実行します。"
    start=0
    count=5
    current_datetime=$(date)
    echo "gen_test: $current_datetime test/$count"
    echo "test" | python3 tetris-one.py > gen/gen_test.txt #2> /dev/null
    echo "test" | python3 tetris-test.py #2> /dev/null
    echo "0" | python3 make_model.py
elif [ $# -eq 1 ];then
    start=0
    count=$1
    current_datetime=$(date)
    echo "gen_test: $current_datetime test/$count"
    echo "test" | python3 tetris-one.py > gen/gen_test.txt 2> /dev/null
    echo "test" | python3 tetris-test.py #2> /dev/null
    echo "0" | python3 make_model.py

elif [ $# -eq 2 ];then
  start=$1
  count=$2
else
  echo "エラー: 引数の数は1つまたは2つである必要があります。"
  exit 1
fi


for ((i=start; i<count; i++));
do
    current_datetime=$(date)
    echo "gen_test: $current_datetime $i/$count"
    echo $i | python3 tetris-one.py > gen/gen_$i.txt 2> /dev/null
    echo $i | python3 tetris.py #2> /dev/null
    echo $(($i+1)) | python3 make_model.py
done

current_datetime=$(date)
echo "gen_test: $current_datetime $count/$count"