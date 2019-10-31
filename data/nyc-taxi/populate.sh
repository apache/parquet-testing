#!/usr/bin/env bash

THIS="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

generate_dates() {
  for d in {2009..2018}-{01..12}; do echo $d; done;
  # At the time of writing this script the latest available is 2019-06
  for d in {2019..2019}-{01..06}; do echo $d; done;
}

# Tune this if processes dies due to memory usage
: ${N_PARALLEL:=4}

parallel_download() {
  xargs -L1 -P${N_PARALLEL} ${THIS}/download2parquet.py
}

main() {
  mkdir ${PWD}/data
  pushd ${PWD}/data

  generate_dates | parallel_download

  popd
}

main
