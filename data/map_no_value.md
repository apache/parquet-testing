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

`map_no_value.parquet` is generated with parquet-rs version 53.2.0.
It contains a MAP without a `values` field, and an equivalent LIST
repeating the MAP keys. Both columns comprise 3 rows:
```
[1, 2, 3]
[4, 5, 6]
[7, 8, 9]
```

Here is the file metadata printed by parquet-cli:
```
File path:  map_no_value.parquet
Created by: parquet-rs version 53.2.0
Properties: (none)
Schema:
message spark_schema {
  required group my_map (MAP) {
    repeated group key_value {
      required int32 key;
    }
  }
  required group my_list (LIST) {
    repeated group list {
      required int32 element;
    }
  }
}


Row group 0:  count: 3  72.00 B records  start: 4  total(compressed): 216 B total(uncompressed):216 B 
--------------------------------------------------------------------------------
                      type      encodings count     avg size   nulls   min / max
my_map.key_value.key  INT32     _ RR_     9         12.00 B    0       "1" / "9"
my_list.list.element  INT32     _ RR_     9         12.00 B    0       "1" / "9"
```
