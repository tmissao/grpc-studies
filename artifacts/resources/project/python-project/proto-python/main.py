import google.protobuf.json_format as json_format
import generated.simple_pb2 as simple_pb2
import generated.complex_pb2 as complex_pb2
import generated.enumerations_pb2 as enumerations_pb2
import generated.oneofs_pb2 as oneofs_pb2
import generated.maps_pb2 as maps_pb2

def simple():
    return simple_pb2.Simple(
        id=42,
        is_simple=True,
        name="Tiago Missão",
        sample_lists=[1, 2, 3],
    )


def dummy(id, name):
    return complex_pb2.Dummy(
        id=id,
        name=name)


def complex():
    message = complex_pb2.Complex(
        one_dummy=dummy(1, "Tiago"),
        multiple_dummies=[dummy(2, "João"), dummy(3, "Kleber")]
    )

    message.multiple_dummies.add(id=4, name="Jonas")
    message.multiple_dummies.append(dummy(id=5, name="Matheus"))
    return message


def enums():
    return enumerations_pb2.Enumeration(
        #eye_color=1
        eye_color=enumerations_pb2.BROWN
    )


def oneofs(is_uuid, id):
    if is_uuid:
        return oneofs_pb2.Identifier(uuid=id)
    else:
        return oneofs_pb2.Identifier(id=id)


def id_wrapper(id):
    return maps_pb2.IdWrapper(id=id)


def to_file(path, message):
    with open(path, "wb") as file:
        bytes_as_str = message.SerializeToString()
        file.write(bytes_as_str)


def from_file(path, messageType):
    message = None
    with open(path, "rb") as file:
        message = messageType().FromString(file.read())

    return message


def to_json(message):
    return json_format.MessageToJson(message, indent=None )


def from_json(json_str, type):
    return json_format.Parse(json_str, type(), ignore_unknown_fields=True)


if __name__ == '__main__':
    print("================")
    print("Simple Proto")
    print("================")
    print(simple())

    print("================")
    print("Complex Proto")
    print("================")
    print(complex())

    print("================")
    print("Enumeration Proto")
    print("================")
    print(enums())

    print("================")
    print("OneOffs Proto")
    print("================")
    oneof1 = oneofs(True, "5647da56-95ec-11ee-b9d1-0242ac120002")
    print(oneof1)
    print(f'WhichOneMethod: {oneof1.WhichOneof("identifier")}')

    print("================")
    oneof2 = oneofs(False, 56)
    print(oneof2)
    print(f'WhichOneMethod: {oneof2.WhichOneof("identifier")}')

    print("================ - Modifying oneof2")
    oneof2.uuid = "5647da56-95ec-11ee-b9d1-0242ac120003"
    print(oneof2)
    print(f'WhichOneMethod: {oneof2.WhichOneof("identifier")}')

    print("================")
    print("Maps Proto")
    print("================")
    map = maps_pb2.MapExample()

    # Maps in Protobuf cannot be assigned directly otherwise it will result in an error
    # map.ids["X"] = id_wrapper(0)
    map.ids["A"].MergeFrom(id_wrapper(1))
    map.ids["B"].id = 2
    print(map)
    print("=================")

    print("================")
    print("Write Proto to File")
    print("================")
    path = "simple.bin"
    simple = simple()
    to_file(path, simple)
    print("=================")

    print("================")
    print("Read Proto from File")
    print("================")
    simple2 = from_file(path, type(simple))
    print(simple2)
    print("=================")

    print("================")
    print("Proto to Json")
    print("================")
    complex_temp = complex()
    json = to_json(complex_temp)
    print(json)
    print("=================")

    print("================")
    print("Proto from Json")
    print("================")

    complex_temp2 = from_json(json, complex_pb2.Complex)
    print(complex_temp2)