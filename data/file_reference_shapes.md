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


# `file_reference_shapes.parquet`

`FILE`-annotated groups in the shapes
[LogicalTypes.md](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#file)
allows besides the full group: groups defining a subset of the children, children in an
order other than the specification's, a `REQUIRED` group, and `FILE` groups as list elements
and map values. See [file_reference.md](file_reference.md) for every form of reference.

## Schema

```
message file_reference_shapes {
  required int32 id;
  optional group inline_file (FILE) {
    optional binary inline;
    optional binary content_type (STRING);
  }
  optional group external_file (FILE) {
    optional binary uri (STRING);
    optional binary content_type (STRING);
    optional binary checksum (STRING);
  }
  optional group reordered_file (FILE) {
    optional int64 size;
    optional binary inline;
    optional binary uri (STRING);
  }
  required group required_file (FILE) {
    optional binary uri (STRING);
    optional int64 offset;
    optional int64 size;
    optional binary content_type (STRING);
    optional binary checksum (STRING);
    optional binary inline;
  }
  optional group attachments (LIST) {
    repeated group list {
      optional group element (FILE) {
        optional binary uri (STRING);
        optional int64 offset;
        optional int64 size;
        optional binary content_type (STRING);
        optional binary checksum (STRING);
        optional binary inline;
      }
    }
  }
  optional group renditions (MAP) {
    repeated group key_value {
      required binary key (STRING);
      optional group value (FILE) {
        optional binary uri (STRING);
        optional int64 offset;
        optional int64 size;
        optional binary content_type (STRING);
        optional binary checksum (STRING);
        optional binary inline;
      }
    }
  }
}
```

`inline_file` and `external_file` are the two subset groups the specification gives as
examples. `reordered_file` lists its children in an order other than the specification's,
which a reader must ignore because children are identified by name. The file is
uncompressed.

## Values

Each `FILE` value is given by the fields it sets; `inline` bytes are hex.

| Column | `id` 0 | `id` 1 | `id` 2 |
|--------|--------|--------|--------|
| `inline_file` | `inline` = `89504e470d0a1a0a`, `content_type` = `image/png` | null | `inline` = empty |
| `external_file` | `uri` = `s3://bucket/images/cat.jpg`, `content_type` = `image/jpeg`, `checksum` = `ETAG:"9b2cf535f27731c974343645a3985328"` | null | `uri` = `images/cat.jpg` |
| `reordered_file` | `uri` = `s3://bucket/archive.tar`, `size` = 1024 | null | `inline` = `89504e470d0a1a0a` |
| `required_file` | `inline` = `68656c6c6f` | `uri` = `s3://bucket/images/cat.jpg` | `uri` = `s3://bucket/archive.tar`, `offset` = 4096, `size` = 51200 |
| `attachments` | [`inline` = `68656c6c6f`, `content_type` = `text/plain`; null; `uri` = `s3://bucket/report.pdf`, `content_type` = `application/pdf`] | [] | null |
| `renditions` | {`thumbnail`: `uri` = `s3://bucket/archive.tar`, `offset` = 0, `size` = 100; `original`: null} | {} | null |

## Generation

Written by [Hardwood](https://github.com/hardwood-hq/hardwood) the same way as
[file_reference.parquet](file_reference.md), with the schema above declared through
`FileSchema.fromSchemaElements` and the rows in the table. parquet-java 1.18.1 reads each group
back as a plain group with the values above.
