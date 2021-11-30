import string
import matplotlib.pyplot as plt
import scipy.stats as stats

class Instance:
    def __init__(self) -> None:
        self.name = ""
        self.results = []
        self.times = []
    
    def to_string( self ):
        s = "Name: " + self.name + "\n"
        s += "Results: ["
        for r in self.results:
            s += str( r ) + ", "
        s += "]\nTimes: ["
        for t in self.times:
            s += str( t ) + ", "
        s += "]"
        return s

def process_name( name: string ):
    name = name.split( ".txt")
    name = name[ 0 ]
    name = name.split( "/" )
    name = name[ 2 ]
    return name


def find_or_create_instance( name: string, instances ):
    for inst in instances:
        if inst.name == name:
            return inst
    new_inst = Instance()
    new_inst.name = name
    return new_inst

def ler(arquivo):
    arq = open( arquivo )
    texto = arq.readlines()
    inst = Instance()
    instances = []

    i = 0
    while i < len( texto ):
        #print( texto[ i ] )
        if texto[ i ].startswith("."):
            pass
        elif texto[ i ].startswith("file:"):
            s = texto[ i ].split( ":" )
            inst = find_or_create_instance( process_name( s[ 1 ] ), instances )
        elif texto[ i ].startswith("seed:"):
            pass
        else:
            inst.results.append( float( texto[ i ] ) )
            inst.times.append( float( texto[ i+1 ] ) )
            instances.append( inst )
            i += 1
        i += 1
    
    return instances

def get_results( instances ):
    list = []
    for i in instances:
        for r in i.results:
            list.append( r )
    return list

def get_times( instances ):
    list = []
    for i in instances:
        for r in i.times:
            list.append( r )
    return list

def anova_all( data1, data2 ):
    fvalue, pvalue = stats.f_oneway( data1, data2 )
    print( pvalue )

instances_mono = ler( "./instances/log_2021_11_12_mono.txt" )
instances_octa = ler( "./instances/log_2021_11_07_octa.txt" )

plt.xlabel("Algoritmo")
plt.ylabel("Qualidade da solução")
plt.boxplot( get_results( instances_mono ), labels=["mono"], positions=[1], widths=[0.7] )
plt.boxplot( get_results( instances_octa ), labels=["octa"], positions=[2], widths=[0.7] )
plt.savefig( "./instances/result.png")
plt.close()

plt.xlabel("Algoritmo")
plt.ylabel("Tempo (ms)")
plt.boxplot( get_times( instances_mono ), labels=["mono"], positions=[1], widths=[0.7] )
plt.boxplot( get_times( instances_octa ), labels=["octa"], positions=[2], widths=[0.7] )
plt.savefig( "./instances/time.png" )

anova_all( get_results( instances_mono ), get_results( instances_octa ) )
anova_all( get_times( instances_mono ), get_times( instances_octa ) )