# Protobuffers Basics

Below is an example of a Proto definition

```proto
syntax = "proto3"// Defines Protocol Version

message Account { // Message is similar to a class in High Level Languages or Struct in low Level Languages
  
  // The attribute definition follow this pattern

  // [type] [attribute name] = [field tag]
  uint32 id = 1;
  string name = 2;
  bool is_verified = 3;
}
```

## Tags Fields
---

The tags field is what make serialization and deserialization possible

### `Tags Fields Rules`

- The smallest tag is `1` and the largest `536870911`
- Google Reserved Tags `19000 - 19999`

## These are the scalar types allowed in Protocol Buffer:
---
### `Number`

- int32, int64 - (Not efficient serializing negative values) 
- sint32, sint64 - (Not efficient serializing positive values)
- uint32, uint64
- fixed32, fixed64, sfixed32, sfixed64 - takes a fixed amount of bytes when serializing (The fixed family is used when you data have big numbers all the time)
- float, double

> On all the fields above the default value is 0

### `Boolean`

- bool - Allows value true or false

> the default value is false

### `String`

- string - Allows any arbitrary length of text (UTF-8 encoded or 7-bit ASCII)

> the default value is a empty string

### `Bytes`

- bytes - Allows any arbitrary length byte sequence

> the default value is an empty array of bytes

```proto
syntax = proto3

message Account {
  uint32 id = 1;
  string name = 2;
  bytes thumbnail = 3;
  bool is_verified = 4;
  float height = 5;

  repeated string phones = 6;
}
```


## Repeated Fields
---

This is a more complex field type meaning that you can have zero or more elements of that type. Following this pattern

> `repeated <type> <name> = <tag>`;

```proto
message Example {
  repeated string names = 1; // Zero or More values
}
```

> The default value is an empty list

## Optional Fields
---

Allows a field to optionally set, so the field could be in one of two possible states
- the field is set, and contains a value that was explicitly set or parsed from the wire. It will be serialized to the wire.
- the field is unset, and will return the default value. It will not be serialized to the wire.

```proto
message Example {
  optional uint32 age = 1; // Zero or More values
}
```

So in this case it is necessary to call the method `HasField("Age")` or `has_age()` in order to check if the field is set

## Enum
---

Enum is a special structure that represents a group of constants. In an enum the `first tag should start at ZERO`

```proto
  enum DRINK {
    UNSPECIFIED = 0;
    WATER = 1;
    JUICE = 2;
    SODA = 3;
    BEER = 4;
  }

  message Example {
    DRINK drink = 1;
  }
```

> The default value of an enum is the first value

## Maps
---

Map is a special structure that allow to create associative map

> `map<key_type, value_type> map_field = N;`

```proto
  message Project {
    uint32 id = 1;
    string name = 2
  }

  message Wrapper {
    map<string, Project> projects = 1; 
  }
```

Map Fields Rules:
- Map fields cannot be repeated
- When parsing from the wire or when merging, if there are duplicate map keys the last key seen is used. When parsing a map from text format, parsing may fail if there are duplicate keys.
- Cannot use fload,double and enums/message as keys
- The key is not ordering

## OneOf
---

Oneof fields are like regular fields except all the fields in a oneof share memory, so just one field could be set at the same time.

```proto
  message SampleMessage {
    oneof identifier {
      uint32 id = 1;
      string uuid = 2;
    }
  }
```

> Note that if multiple values are set, the last set value as determined by the order in the proto will overwrite all previous ones.

`Cannot use repeated property`



## Example
---

Look below an example with a proto using all field types discussed until now

Look an example below

```proto
syntax = proto3

enum AccountType {
  UNSPECIFIED = 0;
  SAVINGS = 1;
  CHECKING = 2;
  PORTABLE = 3;
}

message Account {
  uint32 id = 1;
  string name = 2;
  bytes thumbnail = 3;
  bool is_verified = 4;
  float height = 5;

  repeated string phones = 6;
  AccountType type = 7;
}
```