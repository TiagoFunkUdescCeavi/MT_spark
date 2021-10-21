from pyspark import SparkContext, SparkConf
import subprocess

spark_conf = SparkConf().setAppName("YourTest").setMaster("local[*]")

sc = SparkContext.getOrCreate(spark_conf)

SIZE = 100

def run_external_program( n ):
	result = subprocess.run(['./app', str( n )],  capture_output=True, text=True)
	value = int( result.stdout )
	return value

nums = list( range( 0, SIZE ) )

nums_rdd = sc.parallelize(nums)
a = nums_rdd.take( SIZE )

pairs = nums_rdd.map(lambda x: (x, run_external_program( x ) ) )
a = pairs.take( SIZE )
print( a )
