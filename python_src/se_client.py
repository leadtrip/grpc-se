import grpc
import SE_pb2
import SE_pb2_grpc

GRPC_PORT = 50052

def run():
    with grpc.insecure_channel(f"localhost:{GRPC_PORT}") as channel:
        stub = SE_pb2_grpc.SecretEscapesStub(channel)
        print("1. Fetch one SE sale - Unary")
        print("2. Fetch multiple SE sales - server streaming")


        rpc_call = input("Which rpc call do you wish to run? ")

        if rpc_call == "1":
            se_sale_request = SE_pb2.SeSaleRequest(id = "A9928")
            se_sale_reply = stub.GetSeSale(se_sale_request)
            print('SeSaleRequest Response received: "%s"' % se_sale_reply)
        elif rpc_call == "2":
            se_sale_range_request = SE_pb2.SeSaleRangeRequest(start = "2025-01-19", end = "2025-01-26")
            se_replies = stub.GetAllSeSales(se_sale_range_request)

            for se_reply in se_replies:
                print('SeSaleRangeRequest Response received: "%s"' % se_reply)

if __name__ == '__main__':
    run()