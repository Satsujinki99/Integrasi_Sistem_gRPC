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
        
        print("=== Unary RPC: Adding a Task ===")
        
        # Create a task
        task = todo_pb2.Task(
            id="",  # Server will generate ID
            title="Complete gRPC assignment",
            description="Implement a To-Do list using gRPC's four communication patterns",
            completed=False
        )
        
        # Call the unary RPC method
        response = stub.AddTask(task)
        
        print(f"Response: {response.message}")
        print(f"Task ID: {response.task_id}")
        print(f"Success: {response.success}")

if __name__ == '__main__':
    run()