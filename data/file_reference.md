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


# `file_reference.parquet`

One `FILE`-annotated group holding every form of reference that
[LogicalTypes.md](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#file)
defines, one form per row. The group defines all six children.

## Schema

```
message file_reference {
  required int32 id;
  optional group file (FILE) {
    optional binary uri (STRING);
    optional int64 offset;
    optional int64 size;
    optional binary content_type (STRING);
    optional binary checksum (STRING);
    optional binary inline;
  }
}
```

The file is uncompressed. A blank cell is a null child.

## Values

| `id` | `uri` | `offset` | `size` | `content_type` | `checksum` | `inline` | Resolves to |
|------|-------|----------|--------|----------------|------------|----------|-------------|
| 0  |  |  |  | `image/png` |  | `89504e470d0a1a0a` | the 8 inline bytes (a PNG signature) |
| 1  |  |  |  | `text/plain` |  | (empty) | zero inline bytes; an empty `BYTE_ARRAY` is set |
| 2  | `s3://bucket/images/cat.jpg` |  |  | `image/jpeg` |  |  | the whole object |
| 3  | `https://example.com/archive.tar` |  | 1024 |  |  |  | bytes `[0, 1024)`; no `content_type`, so `application/octet-stream` |
| 4  | `s3://bucket/archive.tar` | 4096 | 51200 | `image/png` |  |  | bytes `[4096, 55296)` |
| 5  | `s3://bucket/archive.tar` | 0 | 0 |  |  |  | zero bytes |
| 6  | `s3://bucket/greeting.txt` | 0 | 5 | `text/plain` | `SHA-256:2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824` | `68656c6c6f` | the inline bytes `hello`, or the locator; both denote the same bytes |
| 7  | `images/cat.jpg` |  |  | `image/jpeg` |  |  | the whole object at a relative URI |
| 8  |  |  |  |  | `MD5:5d41402abc4b2a76b9719d911017c592` | `68656c6c6f` | `hello` |
| 9  |  |  |  |  | `CRC32:3610a686` | `68656c6c6f` | `hello` |
| 10 |  |  |  |  | `CRC32C:9a71bb4c` | `68656c6c6f` | `hello` |
| 11 |  |  |  |  | `SHA-256:2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824` | `68656c6c6f` | `hello` |
| 12 | `s3://bucket/images/cat.jpg` |  |  |  | `ETAG:"9b2cf535f27731c974343645a3985328"` |  | the whole object |
| 13 | (the group is null) | | | | | | nothing |

Rows 8 to 11 carry one checksum per recomputable algorithm over the inline bytes `hello`,
so a reader can verify each digest. Row 12's `ETAG` is opaque and refers to an object that
does not exist.

## Generation

Written by [Hardwood](https://github.com/hardwood-hq/hardwood)
([hardwood-hq/hardwood#1494](https://github.com/hardwood-hq/hardwood/pull/1494)) with:

```java
FileSchema schema = FileSchema.builder("file_reference")
        .addColumn("id", PhysicalType.INT32, RepetitionType.REQUIRED)
        .file("file", RepetitionType.OPTIONAL)
        .build();
byte[] png = {(byte) 0x89, 'P', 'N', 'G', '\r', '\n', 0x1A, '\n'};
byte[] hello = "hello".getBytes(StandardCharsets.UTF_8);
String sha256 = "SHA-256:2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824";
List<PqFile> rows = Arrays.asList(
        PqFile.inline(png).withContentType("image/png"),
        PqFile.inline(new byte[0]).withContentType("text/plain"),
        PqFile.external("s3://bucket/images/cat.jpg").withContentType("image/jpeg"),
        PqFile.external("https://example.com/archive.tar", 1024),
        PqFile.external("s3://bucket/archive.tar", 4096, 51200).withContentType("image/png"),
        PqFile.external("s3://bucket/archive.tar", 0, 0),
        PqFile.external("s3://bucket/greeting.txt", 0, 5).withInline(hello)
                .withContentType("text/plain").withChecksum(sha256),
        PqFile.external("images/cat.jpg").withContentType("image/jpeg"),
        PqFile.inline(hello).withChecksum("MD5:5d41402abc4b2a76b9719d911017c592"),
        PqFile.inline(hello).withChecksum("CRC32:3610a686"),
        PqFile.inline(hello).withChecksum("CRC32C:9a71bb4c"),
        PqFile.inline(hello).withChecksum(sha256),
        PqFile.external("s3://bucket/images/cat.jpg").withChecksum("ETAG:\"9b2cf535f27731c974343645a3985328\""),
        null);
WriterConfig config = WriterConfig.builder().codec(CompressionCodec.UNCOMPRESSED).build();
try (ParquetFileWriter writer = ParquetFileWriter.create(OutputFile.of(path), schema, config)) {
    for (int i = 0; i < rows.size(); i++) {
        int id = i;
        writer.rowWriter().writeRow(row -> row.setInt("id", id).setFile("file", rows.get(id)));
    }
}
```

parquet-java 1.18.1, which predates `FILE`, reads the group back as a plain group with the values
above.
