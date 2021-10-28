from InstanceReader import *
from RandomGreedyGen_MinMax import RandomGreedyGen_MinMax
from LocalSearch import LocalSearch
from RandomRemoveOperator import RandomRemoveOperator
from ExchangeOperator import ExchangeOperator
from BestAddOperator import BestAddOperator
from GRASP import GRASP

FILE = "/home/tiago/Documentos/Repositorios/TOP_GRASP_TS_PR/instances/set_1_2/p1.2.b.txt"

inst = read( FILE )

gen = RandomGreedyGen_MinMax( 0.9, 2.0, inst.get_number_paths(), inst.get_time_per_path(), inst )
operators = [ RandomRemoveOperator( 0.15 ), ExchangeOperator(), BestAddOperator() ]
ls = LocalSearch( operators )
grasp = GRASP( 50, 1234, gen, ls, inst )
sol = grasp.execute()
print( sol.to_string() )

