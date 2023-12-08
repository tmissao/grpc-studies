# Proto File Organization

When defining a proto file is possible to adopt several organizations

- `Multiple Messages in the same proto file`

```proto
syntax = "proto3"

message Address {
  uint32 number = 1;
  string street = 2;
  string city = 3;
  string state = 4;
  string country = 5;
}

enum Gender {
  UNSPECIFIED = 0;
  MALE = 1;
  FEMALE = 2;
}

message Person {
  string name = 1;
  Gender gender = 2;
  Address address = 3;
}
```

- `Nested Type`

```proto
syntax = "proto3"

enum Gender {
  UNSPECIFIED = 0;
  MALE = 1;
  FEMALE = 2;
}

message Person {
  
  message Address {
    uint32 number = 1;
    string street = 2;
    string city = 3;
    string state = 4;
    string country = 5;
  }

  enum Gender {
    UNSPECIFIED = 0;
    MALE = 1;
    FEMALE = 2;
  }

  string name = 1;
  Gender gender = 2;
  Address address = 3;
}
```

- `Imports`

Imports works for file in the same directory (same level)

```proto

syntax = "proto3"

import "person.proto"

message Employee {
  // Person should be imported from external proto file
  Person person = 1;
}

```

- `Packages`

Suppose your person.proto in under a package called `models`

```proto
// models/person.proto

systax = "proto3"

package models;

message Person {
  
  message Address {
    uint32 number = 1;
    string street = 2;
    string city = 3;
    string state = 4;
    string country = 5;
  }

  enum Gender {
    UNSPECIFIED = 0;
    MALE = 1;
    FEMALE = 2;
  }

  string name = 1;
  Gender gender = 2;
  Address address = 3;
}
```

And you now you desire to use the person proto in other proto that is not under the same directory or package

```proto
syntax = "proto3"

import "models/person.proto"

message Employee {
  // To use the reference you should include the suffix of the package in the type
  models.Person person = 1;
}
```