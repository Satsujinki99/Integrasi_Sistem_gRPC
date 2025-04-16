import grpc
import sys
import os

# Add parent directory to path to import generated modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import todo_pb2
import todo_pb2_grpc

def run():
    # Create a gRPC channel
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub (client)
        stub = todo_pb2_grpc.TodoServiceStub(channel)
        
        print("=== Server Streaming RPC: Listing All Tasks ===")
        
        # Call the server streaming RPC method
        empty = todo_pb2.Empty()
        responses = stub.ListTasks(empty)
        
        # Process the stream of responses
        for task in responses:
            status = "Completed" if task.completed else "Not Completed"
            print(f"ID: {task.id}")
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
            print(f"Status: {status}")
            print("-" * 30)

if __name__ == '__main__':
    run()