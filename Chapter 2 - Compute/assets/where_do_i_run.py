import pydantic
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, udf

# --- PHASE A ---
spark = SparkSession.builder.appName("ComplexLogic").getOrCreate() // יוצר סשן בדרייבר
lookup_table = {"A": 1.1, "B": 1.2, "C": 1.3} // יוצר אובייקט פייתון בזיכרון של הדרייבר

# --- PHASE B ---
raw_df = spark.read.parquet("s3://data/events/") //  יצירת דאטה פריים, גם בדרייבר אחריי קריאה מהdata source
meta_df = spark.createDataFrame([("A", "Premium"), ("B", "Standard")], ["code", "type"]) 


# --- PHASE C ---
udf("double")
def calculate_markup(price, code):
    multiplier = lookup_table.get(code, 1.0)    // שורות של פונקציות משתמש ירוצו בפועל באקסקיוטרים
    return price * multiplier


# --- PHASE D ---
joined_df = raw_df.join(meta_df, raw_df.event_code == meta_df.code) // יעשה באקסקיוטרים

# --- PHASE E ---
final_df = joined_df.withColumn(
    "final_price", calculate_markup("price", "code")
).filter(col("type") == "Premium")   // יעשה באקסקיוטרים, רק בקריאת אקשן (גם הפקודה הקודמת)

# --- PHASE F ---
report = final_df.groupBy("type").agg(avg("final_price")).collect() // יעשה באקסקיוטרים ויחזיר תשובה לדרייבר

# --- PHASE G ---
for row in report:
    print(f"Type: {row['type']}, Avg: {row['avg(final_price)']}")
