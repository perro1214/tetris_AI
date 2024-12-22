#!/bin/bash
size1=10
size2=5


mkdir -p gen
mkdir -p model_gen
mkdir -p data_gen
touch score.csv

if [ $# -eq 1 ];then
  count=$1
else
  echo "エラー: 引数の数は1つである必要があります。"
  echo "デフォルトの5回繰り返し動作を実行します。"
  count=5
fi

if [ $(cat score.csv | wc -l) -eq 0 ]; then
  echo "The file is empty"
  current_datetime=$(date)
  echo "gen_test: $current_datetime test/$count"
  echo "test" $size1| python3 tetris-test.py #2> /dev/null #data_0
  echo 0 | python3 make_model.py #gen_0.k
  echo 0 | python3 tetris-one.py > gen/gen_0.txt #2> /dev/null #gen_0.txt
fi

for ((i=0; i<count; i++));
do
    current_datetime=$(date)
    echo "gen_test: $current_datetime $i/$count"
    (echo $(expr $size2 / 5) | python3 max_score_gen.py | python3 make_dates_of_max_AI.py)& #2> /dev/null
    #(echo $(expr $size2 / 5)| python3 max_score_gen.py | python3 make_dates_of_max_AI.py)& #2> /dev/null
    #(echo $(expr $size2 / 5)| python3 max_score_gen.py | python3 make_dates_of_max_AI.py)& #2> /dev/null
    #(echo $(expr $size2 / 5)| python3 max_score_gen.py | python3 make_dates_of_max_AI.py)& #2> /dev/null
    #(echo $(expr $size2 / 5)| python3 max_score_gen.py | python3 make_dates_of_max_AI.py)& #2> /dev/null
    wait
    echo $i | python3 max_remake_model.py
    echo $i | python3 tetris-one.py > gen/gen_$i.txt #2> /dev/null
done

current_datetime=$(date)
echo "gen_test: $current_datetime $count/$count"