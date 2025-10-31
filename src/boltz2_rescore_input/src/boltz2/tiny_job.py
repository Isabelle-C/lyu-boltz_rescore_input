from pyspark.sql import SparkSession
spark = (
    SparkSession.builder
    .master("local[2]")
    .appName("CheckPython")
    .getOrCreate()
)

def get_worker_version(_):
    import platform
    return platform.python_version()

print("[Driver]", __import__('platform').python_version())
print("[Worker]", spark.sparkContext.parallelize(range(2), 2).map(get_worker_version).collect())

spark.stop()
