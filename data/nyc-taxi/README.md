# NYC taxi dataset

The `populate.sh` will download csv for each month from the NYC taxi dataset
from 2009-01 to 2019-06. Files will be downloaded in parallel and transcoded to
parquet.

## Requirements

`python3` must be an executable found in $PATH. The following python libraries
must be installed:

 * pandas (read_csv)
 * pyarrow with parquet support (write_parquet)
