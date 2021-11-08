#!/bin/bash

execute_all(){
	count=0
    for dir in ./*
    do
        for file in $dir/*
        do
            if [ -f "$file" ]
            then
                for n in $(seq 1 $1)
                do
                    echo "$n-$file"
                    count=$(($count+1))
                    echo "$file" >> $2
                    python3 ../project/main.py --seed 1234 --file $file --alpha 0.9 --iterations 50000 --path y --margin 1.9 --removeOperator r --removePercentage 0.15 --shuffleOperator e --addOperator b >> $2
                done
            fi
        done
    done
    echo $count
}

execute_all 30 log_2021_11_07_mono.txt
