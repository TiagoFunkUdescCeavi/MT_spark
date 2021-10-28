#!/bin/bash

python3 project/main.py --file "/home/tiago/Documentos/Repositorios/TOP_GRASP_TS_PR/instances/set_1_2/p1.2.b.txt" --seed "1234" --alpha 0.9 --iterations 50000 --path y --margin 1.9 --removeOperator RandomRemove --removePercentage 0.15 --shuffleOperator Exchange --addOperator BestAdd
