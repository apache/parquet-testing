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

# Variant Shredding

This directory contains binary files used to verify shredded variant readers.

## Contents

`cases.json` - a JSON list of test cases. Each case is an error case, a single record variant case, or a multi-record variant case.

Each JSON object in the list represents a single case and includes:
* `case_number` - a number to identify the case and its data files
* `test` - name of the test from which the case was generated. Multiple cases can be generated from a single test. For instance, `testShreddedVariantPrimitives` is used to generate a case for each variant primitive.

Binary files for each case are named using the case number. Variant binary files are also named using the row number.

Error cases have the following fields:
* `error_message` - a message describing why the case is an error

Single record cases have the following fields:
* `parquet_file` - path of the Parquet file to be read for the case
* `variant_file` - path of the binary variant file to be read for the case
* `variant` - string representation of the variant for the case

Multi-record cases have the following fields:
* `parquet_file` - path of the Parquet file to be read for the case, containing multiple records
* `variant_files` - path of each binary variant file, one for each record in the Parquet file (may be null for a null variant)
* `variants` - string representation of the variants for the case

## Variant file encoding

Each `*.variant.bin` file contains a single variant serialized by concatenating the serialized bytes of the variant metadata followed by the serialized bytes of the variant value.

## Parquet file encoding

Each Parquet file contains one or more rows. Each row corresponds to a variant file (by ID) for the test case and consists of an `id` field and a `var` field.

## Source

For more information, see the [original test cases](https://github.com/apache/iceberg/blob/main/parquet/src/test/java/org/apache/iceberg/parquet/TestVariantReaders.java).
