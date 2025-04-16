import grpc
import sys
import os

# Add parent directory to path to import generated modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import todo_pb2
import todo_pb2_grpc

def generate_tasks():
    tasks = [
        todo_pb2.Task(title="Buy groceries", description="Milk, eggs, bread", completed=False),
        todo_pb2.Task(title="Call doctor", description="Schedule annual checkup", completed=False),
        todo_pb2.Task(title="Pay utility bills", description="Electricity and water", completed=False),
        todo_pb2.Task(title="Fix bicycle", description="Replace the flat tire", completed=False)
    ]
    
    for task in tasks:
        print(f"Sending task: {task.title}")
        yield task

def run():
    # Create a gRPC channel
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub (client)
        stub = todo_pb2_grpc.TodoServiceStub(channel)
        
        print("=== Client Streaming RPC: Adding Multiple Tasks ===")
        
        # Call the client streaming RPC method
        response = stub.AddMultipleTasks(generate_tasks())
        
        print(f"Response: {response.message}")
        print(f"Added tasks count: {response.added_count}")
        print(f"Task IDs: {', '.join(response.task_ids)}")

if __name__ == '__main__':
    run()