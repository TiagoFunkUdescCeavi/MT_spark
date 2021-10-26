from pyspark import SparkContext, SparkConf
import subprocess
import sys

spark_conf = SparkConf().setAppName("YourTest").setMaster("local[*]")

sc = SparkContext.getOrCreate(spark_conf)

SIZE = 800

print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

def run_external_program( n ):
	result = subprocess.run(['./app', str( n )], check=True, stdout=subprocess.PIPE, universal_newlines=True)
	#result = subprocess.run(['../TOP_GRASP_TS_PR/Project/TOP_GRASP_TS_PR', "1", "1", "1011742676", "../TOP_GRASP_TS_PR/instances/set_4_4/p4.4.l.txt", "--alpha", "0.98", "--iterations", "1000", "--path", "y", "--margin", "1.42", "--removeOperator", "w", "--removePercentage", "0.56", "--shuffleOperator", "e", "--addOperator", "b" ], check=True, stdout=subprocess.PIPE, universal_newlines=True)
	value = float( result.stdout )
	return value

nums = list( range( 0, SIZE ) )

nums_rdd = sc.parallelize(nums,8)

print("Number of Partitions: "+str(nums_rdd.getNumPartitions()))

pairs = nums_rdd.map(lambda x: (x, run_external_program( x ) ) )
a = pairs.take( SIZE )
print( a )
