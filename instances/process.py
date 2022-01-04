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

def read(arquivo):
    arq = open( arquivo )
    texto = arq.readlines()
    inst = Instance()
    instances = []

    i = 0
    while i < len( texto ):
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

def get_results( instances, filter: string ):
    list = []
    for i in instances:
        if i.name == filter:    
            for r in i.results:
                list.append( r )
    return list

def get_times( instances, filter: string ):
    list = []
    for i in instances:
        if i.name == filter:    
            for r in i.times:
                list.append( r )
    return list

def anova_all( data1, data2 ):
    fvalue, pvalue = stats.f_oneway( data1, data2 )
    print( pvalue )

instances_mono = read( "./instances/log_2021_11_12_mono.txt" )
instances_octa = read( "./instances/log_2021_11_07_octa.txt" )

def plot( filter: string ):
    plt.xlabel("Algoritmo")
    plt.ylabel("Qualidade da solução")
    plt.boxplot( get_results( instances_mono, filter ), labels=["mono " + filter], positions=[1], widths=[0.7] )
    plt.boxplot( get_results( instances_octa, filter ), labels=["octa " + filter], positions=[2], widths=[0.7] )
    plt.savefig( "./instances/result_" + filter + ".png")
    plt.close()

    plt.xlabel("Algoritmo")
    plt.ylabel("Tempo (ms)")
    plt.boxplot( get_times( instances_mono, filter ), labels=["mono " + filter], positions=[1], widths=[0.7] )
    plt.boxplot( get_times( instances_octa, filter ), labels=["octa " + filter], positions=[2], widths=[0.7] )
    plt.savefig( "./instances/time_" + filter + ".png" )

    anova_all( get_results( instances_mono, filter ), get_results( instances_octa, filter ) )
    anova_all( get_times( instances_mono, filter ), get_times( instances_octa, filter ) )

plot( "p1.2.m" )