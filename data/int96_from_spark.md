<!--
  ~ Licensed to the Apache Software Foundation (ASF) under one
  ~ or more contributor license agreements.  See the NOTICE file
  ~ distributed with this work for additional information
  ~ regarding copyright ownership.  The ASF licenses this file
  ~ to you under the Apache License, Version 2.0 (the
  ~ "License"); you may not use this file except in compliance
  ~ with the License.  You may obtain a copy of the License at
  ~
  ~   http://www.apache.org/licenses/LICENSE-2.0
  ~
  ~ Unless required by applicable law or agreed to in writing,
  ~ software distributed under the License is distributed on an
  ~ "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
  ~ KIND, either express or implied.  See the License for the
  ~ specific language governing permissions and limitations
  ~ under the License.
  -->

`int96_from_spark.parquet` is generated by Apache Spark 3.4.3 with parquet-mr version 1.13.1.

It has a single column of int96 type with 6 values. int96 typically represents a timestamp with
int32 representing the number of days since the epoch, and an int64 representing
nanoseconds. Due to its nanosecond resolution, many systems handle int96 timestamps by
converting the int32 days to nanoseconds and adding the two values to form a single
64-bit nanosecond timestamp. However, Spark's default timestamp resolution is microseconds, which
results in being able to read and write timestamps with a larger range of dates.

Note that this type is now deprecated in the Parquet spec. It exists only for systems that wish
to maintain compatibility with Apache Spark and other systems that still write this type.

This file contains timestamps that are not all representable with 64-bit nanosecond timestamps.
It originates from [a test for DataFusion Comet](https://github.com/apache/datafusion-comet/blob/fa5910efd927e115d1717b5f0c78fad0ece75c6c/spark/src/test/scala/org/apache/comet/CometCastSuite.scala#L902),
and can be reproduced in a Spark shell with the code below:

```scala
val values = Seq(Some("2024-01-01T12:34:56.123456"), Some("2024-01-01T01:00:00Z"), Some("9999-12-31T01:00:00-02:00"), Some("2024-12-31T01:00:00+02:00"), None, Some("290000-12-31T01:00:00+02:00"))
import org.apache.spark.sql.types.DataTypes
val df = values.toDF("str").select(col("str").cast(DataTypes.TimestampType).as("a")).coalesce(1)
df.write.parquet("int96_from_spark.parquet")
```

As microseconds since the epoch, they correspond to:
```
1704141296123456, 1704070800000000, 253402225200000000, 1735599600000000, null, 9089380393200000000
```

# File Metadata (from parquet-cli meta command)
```
File path:  int96_from_spark.parquet
Created by: parquet-mr version 1.13.1 (build db4183109d5b734ec5930d870cdae161e408ddba)
Properties:
                   org.apache.spark.version: 3.4.3
  org.apache.spark.sql.parquet.row.metadata: {"type":"struct","fields":[{"name":"a","type":"timestamp","nullable":true,"metadata":{}}]}
Schema:
message spark_schema {
  optional int96 a;
}


Row group 0:  count: 6  18.83 B records  start: 4  total(compressed): 113 B total(uncompressed):113 B 
--------------------------------------------------------------------------------
   type      encodings count     avg size   nulls   min / max
a  INT96     S _ R     6         18.83 B    1       
```

# Column Index (from parquet-cli column-index command)
```
row-group 0:
column index for column a:
NONE
offset index for column a:
                          offset   compressed size       first row index
page-0                        81                36                     0
```
