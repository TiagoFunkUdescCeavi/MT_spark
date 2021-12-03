#!/bin/bash

execute_all(){
    for dir in ./*
    do
        for file in $dir/*
        do
            if [ -f "$file" ]
            then
                for n in $(seq 1 $1)
                do
                    echo "$n-$file"
                    echo "$file" >> $2
                    python3 ../project/main.py --file $file --alpha 0.9 --iterations 50000 --path y --margin 1.9 --removeOperator RandomRemove --removePercentage 0.15 --shuffleOperator Exchange --addOperator BestAdd >> $2
                done
            fi
        done
    done
}

execute_all 5 log_2021_11_12_mono.txt
