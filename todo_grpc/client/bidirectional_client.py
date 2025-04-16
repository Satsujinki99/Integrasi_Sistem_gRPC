import grpc
import sys
import os
import time

# Add parent directory to path to import generated modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import todo_pb2
import todo_pb2_grpc

def generate_updates(task_ids):
    # First need to get some task IDs to update
    if not task_ids:
        print("No task IDs provided. Please run the client streaming client first to add tasks.")
        return
    
    # Create updates
    updates = [
        todo_pb2.TaskUpdate(id=task_ids[0], title="Updated grocery list"),
        todo_pb2.TaskUpdate(id=task_ids[1], completed=True),
        todo_pb2.TaskUpdate(id=task_ids[2], description="Updated description: Pay all bills"),
        # Non-existent task ID to demonstrate error handling
        todo_pb2.TaskUpdate(id="non-existent-id", title="This task doesn't exist")
    ]
    
    for update in updates:
        print(f"Sending update for task ID: {update.id}")
        yield update
        time.sleep(1)  # Small delay to demonstrate streaming

def run():
    # Create a gRPC channel
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub (client)
        stub = todo_pb2_grpc.TodoServiceStub(channel)
        
        # First list all tasks to get IDs
        print("Getting all tasks to retrieve IDs...")
        empty = todo_pb2.Empty()
        task_responses = stub.ListTasks(empty)
        
        task_ids = []
        for task in task_responses:
            task_ids.append(task.id)
        
        if not task_ids:
            print("No tasks found. Please add some tasks first.")
            return
            
        print(f"Found {len(task_ids)} tasks.")
        
        print("\n=== Bidirectional Streaming RPC: Updating Tasks ===")
        
        # Call the bidirectional streaming RPC method
        responses = stub.UpdateTasks(generate_updates(task_ids))
        
        # Process the stream of responses
        for response in responses:
            status = "Successful" if response.success else "Failed"
            print(f"Update for task {response.id}: {status}")
            print(f"Message: {response.message}")

if __name__ == '__main__':
    run()