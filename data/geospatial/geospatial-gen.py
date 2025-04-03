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

import json

from pathlib import Path

import numpy as np

import pyarrow as pa
from pyarrow import parquet
import shapely
import shapely.testing
import yaml

# M value support was added in Shapely 2.1.0
if tuple(shapely.__version__.split(".")) < ("2", "1", "0"):
    raise ImportError("shapely >= 2.1.0 is required")

HERE = Path(__file__).parent


class WkbType(pa.ExtensionType):
    """Minimal geoarrow.wkb implementation"""

    def __init__(self, crs=None, edges=None, *, storage_type=pa.binary()):
        self.crs = crs
        self.edges = edges
        super().__init__(storage_type, "geoarrow.wkb")

    def __arrow_ext_serialize__(self):
        obj = {"crs": self.crs, "edges": self.edges}
        return json.dumps({k: v for k, v in obj.items() if v}).encode()

    @classmethod
    def __arrow_ext_deserialize__(cls, storage_type, serialized):
        obj: dict = json.loads(serialized)
        return WkbType(**obj, storage_type=storage_type)


pa.register_extension_type(WkbType())


def write_geospatial():
    with open(HERE / "geospatial.yaml") as f:
        examples = yaml.safe_load(f)

    schema = pa.schema({"group": pa.utf8(), "wkt": pa.utf8(), "geometry": WkbType()})

    with parquet.ParquetWriter(
        HERE / "geospatial.parquet",
        schema,
        store_schema=False,
        compression="none",
    ) as writer:
        for group_name, geometries_wkt in examples.items():
            # Unfortunately these are not quite right because of
            # https://github.com/libgeos/geos/issues/888
            geometries = shapely.from_wkt(geometries_wkt)
            wkbs = shapely.to_wkb(geometries, flavor="iso")

            batch = pa.record_batch(
                {
                    "group": [group_name] * len(geometries_wkt),
                    "wkt": pa.array(geometries_wkt, pa.utf8()),
                    "geometry": WkbType().wrap_array(pa.array(wkbs, pa.binary())),
                }
            )
            writer.write_batch(batch)


def check_geospatial_values():
    tab = parquet.read_table(
        HERE / "geospatial.parquet", arrow_extensions_enabled=False
    )
    geometries_from_wkt = shapely.from_wkt(tab["wkt"])
    geometries_from_wkb = shapely.from_wkb(tab["geometry"])
    shapely.testing.assert_geometries_equal(geometries_from_wkt, geometries_from_wkb)


def iso_type_code(shapely_type_id, has_z, has_m):
    # item was null
    if shapely_type_id < 0:
        return None

    # GEOS type ids are not quite WKB type ids
    iso_type_id = shapely_type_id if shapely_type_id >= 3 else shapely_type_id + 1
    iso_dimensions = (
        3000 if has_z and has_m else 2000 if has_m else 1000 if has_z else 0
    )
    return int(iso_dimensions + iso_type_id)


def calc_stats_shapely(wkts):
    geometries = shapely.from_wkt(wkts)

    # Calculate the list of iso type codes
    type_codes = set()
    for type_id, has_z, has_m in zip(
        shapely.get_type_id(geometries),
        shapely.has_z(geometries),
        shapely.has_m(geometries),
    ):
        type_codes.add(iso_type_code(type_id, has_z, has_m))

    # Calculate min/max ignoring nan values
    coords = shapely.get_coordinates(geometries, include_z=True, include_m=True)
    coord_mins = [
        None if np.isposinf(x) else float(x)
        for x in np.nanmin(coords, 0, initial=np.inf)
    ]
    coord_maxes = [
        None if np.isneginf(x) else float(x)
        for x in np.nanmax(coords, 0, initial=-np.inf)
    ]

    # Assemble stats in the same format as returned by geo_statistics.to_dict()
    stats = {}
    stats["geospatial_types"] = list(
        sorted(code for code in type_codes if code is not None)
    )
    stats["xmin"], stats["ymin"], stats["zmin"], stats["mmin"] = coord_mins
    stats["xmax"], stats["ymax"], stats["zmax"], stats["mmax"] = coord_maxes

    return stats


def check_batch_statistics(stats, wkts, group):
    if stats is None:
        raise ValueError(f"geo_statistics is missing for group {group}")

    shapely_stats = calc_stats_shapely(wkts)
    file_stats = stats.to_dict()
    if file_stats != shapely_stats:
        raise ValueError(
            f"stats mismatch calculated:\n{shapely_stats}\nvs file\n{file_stats}"
        )


def check_geospatial_statistics():
    file = parquet.ParquetFile(
        HERE / "geospatial.parquet", arrow_extensions_enabled=False
    )
    for i in range(file.num_row_groups):
        batch = file.read_row_group(i)
        column_metadata = file.metadata.row_group(i).column(2)
        group = batch["group"][0].as_py()

        check_batch_statistics(column_metadata.geo_statistics, batch["wkt"], group)


if __name__ == "__main__":
    write_geospatial()
    check_geospatial_values()
    check_geospatial_statistics()
