# Protoc - Protobuffer Compiler

In order to compile and generate the target source code using proto buffer protocols, it is necessary to install the [protoc](https://github.com/google/protobuf/releases).

## Setup
---

```bash
curl -OL https://github.com/protocolbuffers/protobuf/releases/download/v25.0/protoc-25.0-linux-x86_64.zip
unzip protoc-25.0-linux-x86_64.zip -d protoc3
sudo mv protoc3/bin/* /usr/local/bin/
sudo mv protoc3/include/* /usr/local/include/
```

## Usage
---

It is possible to generate files for the following languages:

- C - using the option --cpp_out
- C# - using the option --csharp_out
- Java - using the option --java_out
- Kotlin - using the option --kotlin_out
- Object-C - using the option --objc_out
- PHP - using the option --php_out
- Python - using the option --python_out
- Ruby - using the option --ruby_out
- Rust - using the option --rust_out

```bash
# protoc <target_out> <proto files>

protoc --java_out=./java --python_out=./python ./person.proto
```

## Protoc Advanced Usage
---

- `decode_raw` - This option allows to print the tag / value field from a binary proto file. (No proto file is required)

```bash
# Suppose you save your proto data at simple.bin file


cd artifacts/resources/protoc/advanced
cat simple.bin | protoc --decode_raw

# 1: 42
# 2: 1
# 3: "My name"
# 4: "\001\002\003\004\005\006"

```

- `decode` - Similar to `decode_raw`, however it prints name / value from a binary proto file. In this case, it is required the "Message" name and the proto file.

```bash
# Suppose you save your proto data at simple.bin file

cd artifacts/resources/protoc/advanced
cat simple.bin | protoc --decode=Simple simple.proto

# id: 42
# is_simple: true
# name: "My name"
# sample_lists: 1
# sample_lists: 2
# sample_lists: 3
# sample_lists: 4
# sample_lists: 5
# sample_lists: 6
```

- `encode` - Does the oposite of `decode` it takes the name / value file and converts to binary proto file

```bash
# Suppose you save your proto data at simple.bin file

cd artifacts/resources/protoc/advanced
# Generates Data to TXT format
cat simple.bin | protoc --decode=Simple simple.proto > simple.txt

cat simple.txt | protoc --encode=Simple simple.proto

```