from pyspark import SparkContext, SparkConf

spark_conf = SparkConf()\
  .setAppName("YourTest")\
  .setMaster("local[*]")

sc = SparkContext.getOrCreate(spark_conf)

def sei_la():
	nums = list(range(0, 1000001))

	nums_rdd = sc.parallelize(nums)

	squared_nums_rdd = nums_rdd.map(lambda x: x ** 2)

	pairs = squared_nums_rdd.map(lambda x: (x, len(str(x))))

	even_digit_pairs = pairs.filter(lambda x: (x[1] % 2) == 0)

	flipped_pairs = even_digit_pairs.map(lambda x: (x[1], x[0]))

	grouped = flipped_pairs.groupByKey()

	grouped = grouped.map(lambda x: (x[0], list(x[1])))

	averaged = grouped.map(lambda x: (x[0], sum(x[1]) / len(x[1]) ))

for i  in range( 10 ):
	print( i )
	sei_la()
