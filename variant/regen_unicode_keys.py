# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# Generates the `object_unicode_keys_sorted` and `object_unicode_keys_unsorted`
# example files.
#
# These examples contain object field names on both sides of the UTF-16
# surrogate range, where unsigned lexicographic UTF-8 byte order (required by
# the Variant spec for object field ordering) disagrees with UTF-16 code-unit
# order (e.g. Java's String.compareTo). For example, UTF-16 orders U+10000
# (surrogate pair D800 DC00) before U+E000, U+FFFF, while UTF-8 byte order
# places U+10000 (F0 90 80 80) after both (EE 80 80, EF BF BF). An
# implementation that sorts or binary-searches field names with a UTF-16
# string comparison will silently mishandle these files.
#
# Both examples encode the same logical object. Each field's value is a short
# string spelling the field name's code point, so a lookup that lands on the
# wrong field is self-evident:
#
#   * `object_unicode_keys_sorted` -- metadata dictionary is sorted
#     (`sorted_strings = 1`) and field ids appear in dictionary order
#   * `object_unicode_keys_unsorted` -- metadata dictionary is deliberately
#     scrambled (`sorted_strings = 0`), so object field ids are non-monotonic
#     and a reader must compare the referenced key bytes, not the ids

import json

# Field names in unsigned UTF-8 byte order (equal to code point order)
KEYS = [
    "$",      # $        24
    "0",      # 0        30
    "A",      # A        41
    "a",      # a        61
    "~",      # ~        7E
    "¢",      # U+00A2        C2 A2
    "€",      # U+20AC        E2 82 AC
    "\ue000",  # private  EE 80 80  (first BMP char after the surrogates)
    "\uffff",  # U+FFFF   EF BF BF  (last BMP char)
    "\U00010000",  # U+10000  F0 90 80 80  (first supplementary char)
    "\U0001f600",  # U+1F600  F0 9F 98 80
    "\U0010ffff",  # U+10FFFF F4 8F BF BF  (last valid code point)
]

OBJ = {k: "U+%04X" % ord(k) for k in KEYS}

assert KEYS == sorted(KEYS), "KEYS must be listed in code point order"
assert [k.encode("utf-8") for k in KEYS] == sorted(k.encode("utf-8") for k in KEYS)


def encode_metadata(dictionary, sorted_strings):
    key_bytes = [k.encode("utf-8") for k in dictionary]
    total = sum(len(b) for b in key_bytes)
    assert len(dictionary) <= 0xFF and total <= 0xFF, "offset_size 1 is assumed"
    header = 0x01 | (0x10 if sorted_strings else 0x00)  # version 1, offset_size 1
    out = bytearray([header, len(dictionary)])
    offset = 0
    for b in key_bytes:
        out.append(offset)
        offset += len(b)
    out.append(offset)
    for b in key_bytes:
        out += b
    return bytes(out)


def encode_short_string(s):
    b = s.encode("utf-8")
    assert len(b) < 64
    return bytes([(len(b) << 2) | 0b01]) + b


def encode_object(obj, dictionary):
    # field_offset_size 1, field_id_size 1, is_large 0
    fields = sorted(obj, key=lambda k: k.encode("utf-8"))
    values = [encode_short_string(obj[k]) for k in fields]
    assert len(fields) <= 0xFF and sum(len(v) for v in values) <= 0xFF
    out = bytearray([0b10, len(fields)])
    for k in fields:
        out.append(dictionary.index(k))
    offset = 0
    for v in values:
        out.append(offset)
        offset += len(v)
    out.append(offset)
    for v in values:
        out += v
    return bytes(out)


def write_example(name, dictionary, sorted_strings):
    with open(f"{name}.metadata", "wb") as f:
        f.write(encode_metadata(dictionary, sorted_strings))
    with open(f"{name}.value", "wb") as f:
        f.write(encode_object(OBJ, dictionary))


write_example("object_unicode_keys_sorted", KEYS, sorted_strings=True)

# Scramble the dictionary with a fixed permutation so field ids are
# non-monotonic in the object
scrambled = [KEYS[i] for i in [9, 3, 11, 0, 8, 5, 1, 10, 4, 7, 2, 6]]
assert sorted(scrambled) == KEYS
write_example("object_unicode_keys_unsorted", scrambled, sorted_strings=False)

print(json.dumps(OBJ, sort_keys=True, indent=4))
