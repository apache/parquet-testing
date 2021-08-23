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

`delta_byte_array.parquet` is generated with parquet-mr version 1.10.0.
The expected file contents are in `delta_byte_array_expect.csv`.

All the column are DELTA_BYTE_ARRAY-encoded. Each column has 100,000 rows.

Here is the file structure:
```file:                  file:/Users/pincheng/table/delta_byte_array/arrow_csv/delta_byte_array.parquet
creator:               parquet-mr version 1.10.0 (build 031a6654009e3b82020012a18434c582bd74c73a)

file schema:           hive_schema
--------------------------------------------------------------------------------
c_customer_id:         OPTIONAL BINARY L:STRING R:0 D:1
c_salutation:          OPTIONAL BINARY L:STRING R:0 D:1
c_first_name:          OPTIONAL BINARY L:STRING R:0 D:1
c_last_name:           OPTIONAL BINARY L:STRING R:0 D:1
c_preferred_cust_flag: OPTIONAL BINARY L:STRING R:0 D:1
c_birth_country:       OPTIONAL BINARY L:STRING R:0 D:1
c_login:               OPTIONAL BINARY L:STRING R:0 D:1
c_email_address:       OPTIONAL BINARY L:STRING R:0 D:1
c_last_review_date:    OPTIONAL BINARY L:STRING R:0 D:1

row group 1:           RC:100000 TS:6636179 OFFSET:4
--------------------------------------------------------------------------------
c_customer_id:          BINARY UNCOMPRESSED DO:0 FPO:4 SZ:807995/807995/1.00 VC:100000 ENC:DELTA_BYTE_ARRAY ST:[min: AAAAAAAAAAAABAAA, max: AAAAAAAAPPPPAAAA, num_nulls: 0]
c_salutation:           BINARY UNCOMPRESSED DO:0 FPO:807999 SZ:331048/331048/1.00 VC:100000 ENC:DELTA_BYTE_ARRAY ST:[min: Dr., max: Sir, num_nulls: 3410]
c_first_name:           BINARY UNCOMPRESSED DO:0 FPO:1139047 SZ:653807/653807/1.00 VC:100000 ENC:DELTA_BYTE_ARRAY ST:[min: Aaron, max: Zulma, num_nulls: 3492]
c_last_name:            BINARY UNCOMPRESSED DO:0 FPO:1792854 SZ:679613/679613/1.00 VC:100000 ENC:DELTA_BYTE_ARRAY ST:[min: Aaron, max: Zuniga, num_nulls: 3497]
c_preferred_cust_flag:  BINARY UNCOMPRESSED DO:0 FPO:2472467 SZ:113792/113792/1.00 VC:100000 ENC:DELTA_BYTE_ARRAY ST:[min: N, max: Y, num_nulls: 3426]
c_birth_country:        BINARY UNCOMPRESSED DO:0 FPO:2586259 SZ:947108/947108/1.00 VC:100000 ENC:DELTA_BYTE_ARRAY ST:[min: AFGHANISTAN, max: ZIMBABWE, num_nulls: 3439]
c_login:                BINARY UNCOMPRESSED DO:0 FPO:3533367 SZ:47/47/1.00 VC:100000 ENC:DELTA_BYTE_ARRAY ST:[num_nulls: 100000, min/max not defined]
c_email_address:        BINARY UNCOMPRESSED DO:0 FPO:3533414 SZ:2760226/2760226/1.00 VC:100000 ENC:DELTA_BYTE_ARRAY ST:[min: Aaron.Anderson@0CQ4QUkBY2Q.edu, max: Zulma.Carter@MfvjVN43Udd95KeZ.com, num_nulls: 3521]
c_last_review_date:     BINARY UNCOMPRESSED DO:0 FPO:6293640 SZ:342543/342543/1.00 VC:100000 ENC:DELTA_BYTE_ARRAY ST:[min: 2452283, max: 2452648, num_nulls: 3484]
```
