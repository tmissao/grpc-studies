BIN_NAME = .venv/bin/activate
PROTO_DIR = proto
PROTO_GENERATED_DIR = .

generate:
	python -m grpc_tools.protoc -I${PROTO_DIR} --python_out=${PROTO_GENERATED_DIR} --pyi_out=${PROTO_GENERATED_DIR} \
		--grpc_python_out=${PROTO_GENERATED_DIR} ${PROTO_DIR}/*.proto