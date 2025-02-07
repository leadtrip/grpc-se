from concurrent import futures

import grpc
import SE_pb2
import SE_pb2_grpc
from se_client import GRPC_PORT


class SeServer(SE_pb2_grpc.SecretEscapesServicer):
    def GetSeSale(self, request, context):
        print("getSeSale called")
        print(request)
        se_sale_reply = SE_pb2.SeSaleReply()
        se_sale_reply.id = request.id
        se_sale_reply.url_slug = 'nice.place.near.the.beach'
        return se_sale_reply

    def GetAllSeSales(self, request, context):
        print("getAllSeSale called")
        print(request)

        for i in range(3):
            se_sale_reply = SE_pb2.SeSaleReply()
            se_sale_reply.id = "A"+str(i)
            se_sale_reply.url_slug = 'nice.place.near.the.beach'+str(i)
            yield se_sale_reply

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    SE_pb2_grpc.add_SecretEscapesServicer_to_server(SeServer(), server)
    server.add_insecure_port(f"[::]:{GRPC_PORT}")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()