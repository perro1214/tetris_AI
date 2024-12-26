#!/bin/bash
size1=5
size2=5
mkdir -p gen
mkdir -p model_gen
mkdir -p data_gen
touch score.csv
if [ $# -eq 0 ]; then
    echo "引数が指定されていません。デフォルトの5回繰り返し動作を実行します。"
    start=0
    count=5
elif [ $# -eq 1 ];then
    start=1
    count=$1
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
    (echo $(expr $size2 / 5)| python3 make_dates.py)& #2> /dev/null
    (echo $(expr $size2 / 5)| python3 make_dates.py)& #2> /dev/null
    (echo $(expr $size2 / 5)| python3 make_dates.py)& #2> /dev/null
    (echo $(expr $size2 / 5)| python3 make_dates.py)& #2> /dev/null
    (echo $(expr $size2 / 5)| python3 make_dates.py)& #2> /dev/null
    wait
    python3 make_model.py
    python3 tetris-one.py > gen/gen_$i.txt #2> /dev/null
done

current_datetime=$(date)
echo "gen_test: $current_datetime $count/$count"