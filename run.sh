#!/bin/bash
size1=5000
size2=100

if [ $# -eq 0 ]; then
    echo "引数が指定されていません。デフォルトの5回繰り返し動作を実行します。"
    start=1
    count=5
    current_datetime=$(date)
    echo "gen_test: $current_datetime test/$count"
    echo "test" $size1| python3 tetris-test.py #2> /dev/null #data_0
    echo 0 | python3 make_model.py #gen_0.k
    echo 0 | python3 tetris-one.py > gen/gen_0.txt #2> /dev/null #gen_0.txt
elif [ $# -eq 1 ];then
    start=1
    count=$1
    current_datetime=$(date)
    echo "gen_test: $current_datetime test/$count"
    echo "test" $size1| python3 tetris-test.py #2> /dev/null
    echo 0 | python3 make_model.py
    echo 0 | python3 tetris-one.py > gen/gen_test.txt #2> /dev/null

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
    (echo $i $(expr $size2 / 5)| python3 make_dates_of_AI.py)& #2> /dev/null
    (echo $i $(expr $size2 / 5)| python3 make_dates_of_AI.py)& #2> /dev/null
    (echo $i $(expr $size2 / 5)| python3 make_dates_of_AI.py)& #2> /dev/null
    (echo $i $(expr $size2 / 5)| python3 make_dates_of_AI.py)& #2> /dev/null
    (echo $i $(expr $size2 / 5)| python3 make_dates_of_AI.py)& #2> /dev/null
    wait
    echo $i | python3 remake_model.py
    echo $i | python3 tetris-one.py > gen/gen_$i.txt #2> /dev/null
done

current_datetime=$(date)
echo "gen_test: $current_datetime $count/$count"