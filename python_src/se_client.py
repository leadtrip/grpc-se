from time import sleep
import grpc
import SE_pb2
import SE_pb2_grpc

GRPC_PORT = 50052



def run():
    with grpc.insecure_channel(f"localhost:{GRPC_PORT}") as channel:
        stub = SE_pb2_grpc.SecretEscapesStub(channel)
        print("1. Fetch one SE sale - Unary")
        print("2. Fetch multiple SE sales - server streaming")
        print("3. Fetch multiple SE sales batched - client streaming")
        print("4. Build package - bidirectional streaming")

        rpc_call = input("Which rpc call do you wish to run? ")

        if rpc_call == "1":
            unary_example(stub)
        elif rpc_call == "2":
            server_streaming_example(stub)
        elif rpc_call == "3":
            client_streaming_example(stub)
        elif rpc_call == "4":
            bidirectional_example(stub)

def unary_example(stub):
    se_sale_request = SE_pb2.SeSaleRequest(id = 1)
    se_sale_reply = stub.GetSeSale(se_sale_request)
    print('SeSaleRequest Response received: "%s"' % se_sale_reply)

def server_streaming_example(stub):
    se_sale_range_request = SE_pb2.SeSaleRangeRequest(start = "2025-01-19", end = "2025-01-26")
    se_replies = stub.GetAllSeSales(se_sale_range_request)
    for se_reply in se_replies:
        print('SeSaleRangeRequest Response received: "%s"' % se_reply)

def client_streaming_example(stub):
    def generate_requests():
        sale_ids = [1, 2, 3, 4, 5]
        for sale_id in sale_ids:
            request = SE_pb2.SeSaleRequest(id=sale_id)
            print(f"Sending sale request for ID: {sale_id}")
            yield request
            sleep(0.2)  # Simulate slight delay between requests

    response = stub.GetBatchedSeSales(generate_requests())

    print("\nReceived batched sales reply:")
    for sale_reply in response.replies:
        print(f"Sale ID: {sale_reply.id}, URL: {sale_reply.url_slug}")

def bidirectional_example(stub):
    def generate_requests():
        requests = [
            SE_pb2.PackageRequest(user_id="user123", selection_type="flight", selection_id="FL123", quantity=1),
            SE_pb2.PackageRequest(user_id="user123", selection_type="hotel", selection_id="HT456", quantity=2),
            SE_pb2.PackageRequest(user_id="user123", selection_type="tour", selection_id="TR789", quantity=1),
        ]

        for req in requests:
            print(f"Sending request: {req.selection_type} - {req.selection_id}")
            yield req
            sleep(0.5)  # Simulate delay between requests

    responses = stub.CustomizePackage(generate_requests())

    for response in responses:
        print(f"Received response: {response.selection_type} - {response.selection_id}")
        print(f"Available: {response.available}, Price: ${response.price}, Message: {response.message}")
        print("-" * 40)

if __name__ == '__main__':
    run()