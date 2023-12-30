import math
import grpc
import average_pb2
import max_pb2
import prime_pb2
import sqrt_pb2
import sum_pb2
import prime_decomposition_pb2
import calculator_pb2_grpc
from concurrent import futures
from typing import Iterator


class CalculatorService(calculator_pb2_grpc.CalculatorServicer):

    def GetNthPrime(self, request: prime_pb2.NthPrimeRequest, context):
        nth_prime = request.number
        primes = [2]
        number = 3

        while len(primes) < nth_prime:
            is_prime = True
            for e in primes:
                if number % e == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(number)
            number = number + 1
        print(primes)
        return prime_pb2.NthPrimeResponse(result=primes[len(primes)-1])

    def Sqrt(self, request: sqrt_pb2.SqrtRequest, context):
        if request.number < 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f'Invalid Argument, the number should be an int, received: {request.number}')
            return sqrt_pb2.SqrtResponse()

        return sqrt_pb2.SqrtResponse(result= int(math.sqrt(request.number)))

    def Max(self, request_iterator: Iterator[max_pb2.MaxRequest], context):
        max_number = None
        for r in request_iterator:
            number = r.number
            if max_number is None or max_number < number:
                max_number = number
                yield max_pb2.MaxResponse(result=max_number)

    def Average(self, request_iterator: Iterator[average_pb2.AverageRequest], context):
        average = 0
        count = 0

        for r in request_iterator:
            average = average + r.number
            count = count + 1

        return average_pb2.AverageResponse(result=average/count)

    def Sum(self, request: sum_pb2.SumRequest, context):
        num1 = request.first_number
        num2 = request.second_number
        return sum_pb2.SumResponse(result=num1+num2)

    def PrimeDecomposition(self, request: prime_decomposition_pb2.PrimeDecompositionRequest, context):
        number = request.number
        prime = 2
        while number > 1:
            if number % prime == 0:
                number = number/prime
                res = prime_decomposition_pb2.PrimeDecompositionResponse(prime=prime)
                yield res
            else:
                prime = prime + 1


def create_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorService(), server)
    print('Starting server. Listening on port 50051')
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    create_grpc_server()
