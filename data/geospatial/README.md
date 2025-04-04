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

# Geospatial Test Files


These test files cover the main and corner case functionality of the
[Parquet Geospatial Types](https://github.com/apache/parquet-format/blob/master/Geospatial.md)
GEOMETRY and GEOGRAPHY.

- `geospatial.parquet`: Contains row groups with specific combinations of
  geometry types to test statistics generation and geometry type coverage.
  The file contains columns `group` (string identifier of the group name),
  `wkt` (the human-readable well-known text representation of the geometry)
  and `geometry` (a Parquet GEOMETRY column). A human-readable version of
  the file is available in `geospatial.yaml`.
