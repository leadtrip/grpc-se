from concurrent import futures
from time import sleep
from se_database import db, InMemoryDatabase
import grpc
import SE_pb2
import SE_pb2_grpc
from se_client import GRPC_PORT


class SeServer(SE_pb2_grpc.SecretEscapesServicer):
    def GetSeSale(self, request, context):
        print(f"GetSeSale called {request}")
        se_sale_reply = SE_pb2.SeSaleReply()
        db_sale = db.get_record_by_id(request.id)
        se_sale_reply.id = db_sale["id"]
        se_sale_reply.url_slug = db_sale["url_slug"]
        return se_sale_reply

    def GetAllSeSales(self, request, context):
        print(f"GetAllSeSales called {request}")

        for i in range(1, 3):
            se_sale_reply = SE_pb2.SeSaleReply()
            db_sale = db.get_record_by_id(i)
            se_sale_reply.id = db_sale["id"]
            se_sale_reply.url_slug = db_sale["url_slug"]
            yield se_sale_reply
            sleep(1) # simulate a delay fetching from somewhere

    def GetBatchedSeSales(self, request_iterator, context):
        print("GetBatchedSeSales called")
        batch_reply = SE_pb2.BatchSeSaleReply()
        for request in request_iterator:
            print(f"SeSaleRequest {request}")
            se_sale_reply = SE_pb2.SeSaleReply()
            db_sale = db.get_record_by_id(request.id)
            se_sale_reply.id = db_sale["id"]
            se_sale_reply.url_slug = db_sale["url_slug"]
            batch_reply.replies.append(se_sale_reply)
            sleep(0.5) # simulate a delay fetching from somewhere

        return batch_reply

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    SE_pb2_grpc.add_SecretEscapesServicer_to_server(SeServer(), server)
    server.add_insecure_port(f"[::]:{GRPC_PORT}")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()