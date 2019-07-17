# Test data files for Parquet compatibility and regression testing

TODO: Document what each file is

## Encrypted Files

Tests files with .parquet.encrypted suffix are encrypted using Parquet Modular Encryption.

A detailed description of the Parquet Modular Encryption specification can be found here:
```
 https://github.com/apache/parquet-format/blob/encryption/Encryption.md
```

Following are the keys and key ids (when using key\_retriever) used to encrypt the encrypted columns and footer in the files:
* Encrypted/Signed Footer:
  * key:   "0123456789012345";
  * key\_id: "kf"
* Encrypted column double\_field:
  * key:  "1234567890123450"
  * key\_id: "kc1"
* Encrypted column float\_field:
  * key: "1234567890123451"
  * key\_id: "kc2"

AAD prefix is "tester". It is used in the following files:
1. encrypt\_columns\_and\_footer\_disable\_aad\_storage.parquet.encrypted
2. encrypt\_columns\_and\_footer\_aad.parquet.encrypted


A sample that reads and checks these files can be found at the following tests:
```
cpp/src/parquet/encryption-read-configurations-test.cc
cpp/src/parquet/test-encryption-util.h
```
