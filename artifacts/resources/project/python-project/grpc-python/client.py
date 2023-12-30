import grpc

import average_pb2
import max_pb2
import prime_decomposition_pb2
import prime_pb2
import sqrt_pb2
import sum_pb2
import calculator_pb2_grpc
from typing import Iterator
from grpc._channel import _InactiveRpcError


def create_grpc_client() -> calculator_pb2_grpc.CalculatorStub:
    channel = grpc.insecure_channel('localhost:50051')
    return calculator_pb2_grpc.CalculatorStub(channel)


# Unary Request
def call_sum(client: calculator_pb2_grpc.CalculatorStub, first_number, second_number):
    req = sum_pb2.SumRequest(first_number=first_number, second_number=second_number)
    res: sum_pb2.SumResponse = client.Sum(req)
    print(res.result)


# Server Streaming Request
def call_prime_decomposition(client: calculator_pb2_grpc.CalculatorStub, number):
    req = prime_decomposition_pb2.PrimeDecompositionRequest(number=number)
    res: Iterator[prime_decomposition_pb2.PrimeDecompositionResponse] = client.PrimeDecomposition(req)
    for r in res:
        print(r.prime)


# Client Streaming Request
def call_average(client: calculator_pb2_grpc.CalculatorStub, numbers: list[int]):

    def generate_messages():
        for e in numbers:
            yield average_pb2.AverageRequest(number=e)

    res: average_pb2.AverageResponse = client.Average(generate_messages())
    print(res.result)


# Bidirectional Streaming
def call_max(client: calculator_pb2_grpc.CalculatorStub, numbers: list[int]):

    # One Way
    # def generate_messages():
    #     for e in numbers:
    #         yield max_pb2.MaxRequest(number=e)
    # res: Iterator[max_pb2.MaxResponse] = client.Max(generate_messages())

    payload = []
    for e in numbers:
        payload.append(max_pb2.MaxRequest(number=e))
    res: Iterator[max_pb2.MaxResponse] = client.Max(payload.__iter__())
    for r in res:
        print(r.result)


# Error Handler
def call_sqrt(client: calculator_pb2_grpc.CalculatorStub, number: int):
    req = sqrt_pb2.SqrtRequest(number=number)
    try:
        res: sqrt_pb2.SqrtResponse = client.Sqrt(req)
        print(res.result)
    except grpc.RpcError as err:
        print(f'An Exception Happened')
        if isinstance(err, _InactiveRpcError):
            print(f'Error Code: {err.code()}, details: {err.details()}')


# Error Handler Bidirectional Stream, server aborts the connection
def call_many_sqrt(client: calculator_pb2_grpc.CalculatorStub, numbers: list[int]):
    reqs = [sqrt_pb2.SqrtRequest(number=e) for e in numbers]
    try:
        res: Iterator[sqrt_pb2.SqrtResponse] = client.ManySqrt(reqs.__iter__())
        for r in res:
            print(r.result)
    except grpc.RpcError as err:
        print(f'Error Code: {err.code()}, details: {err.details()}')


# Setting Timeout
def call_nth_prime(client: calculator_pb2_grpc.CalculatorStub, nth_prime: int):
    req = prime_pb2.NthPrimeRequest(number=nth_prime)
    try:
        res: prime_pb2.NthPrimeResponse = client.GetNthPrime(req, timeout=3)
        print(res.result)
    except grpc.RpcError as err:
        print(f'An Exception Happened')
        if isinstance(err, _InactiveRpcError):
            print(f'Error Code: {err.code()}, details: {err.details()}')


def run():
    client = create_grpc_client()
    # call_sum(client=client, first_number=10, second_number=15)
    # call_prime_decomposition(client=client, number=120)
    # call_average(client, numbers=[1, 2, 3, 4])
    # call_max(client, numbers=[1, 5, 3, 6, 2, 21, 13])
    # call_sqrt(client, 36)
    # call_sqrt(client, -36) # Should raise an Error
    call_many_sqrt(client, [4, 16, 36, -16, 121])
    # call_nth_prime(client, nth_prime=1000)
    # call_nth_prime(client, nth_prime=20000) # Example with Timeout



if __name__ == '__main__':
    run()
