import uuid
import time
import grpc
from concurrent import futures
import sys
import os

# Add parent directory to path to import generated modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import todo_pb2
import todo_pb2_grpc

class TodoServiceServicer(todo_pb2_grpc.TodoServiceServicer):
    def __init__(self):
        # In-memory database of tasks
        self.tasks = {}
    
    def AddTask(self, request, context):
        """Unary RPC: Add a single task and return response"""
        task_id = str(uuid.uuid4())
        task = {
            'id': task_id,
            'title': request.title,
            'description': request.description,
            'completed': request.completed
        }
        self.tasks[task_id] = task
        
        print(f"Added task: {task}")
        
        return todo_pb2.TaskResponse(
            success=True,
            message=f"Task '{request.title}' added successfully",
            task_id=task_id
        )
    
    def ListTasks(self, request, context):
        """Server streaming RPC: Stream all tasks back to client"""
        print("Listing all tasks...")
        for task_id, task in self.tasks.items():
            yield todo_pb2.Task(
                id=task_id,
                title=task['title'],
                description=task['description'],
                completed=task['completed']
            )
            # Small delay to demonstrate streaming
            time.sleep(0.5)
    
    def AddMultipleTasks(self, request_iterator, context):
        """Client streaming RPC: Receive multiple tasks from client"""
        added_count = 0
        task_ids = []
        
        for request in request_iterator:
            task_id = str(uuid.uuid4())
            self.tasks[task_id] = {
                'id': task_id,
                'title': request.title,
                'description': request.description,
                'completed': request.completed
            }
            added_count += 1
            task_ids.append(task_id)
            print(f"Received task: {request.title}")
        
        return todo_pb2.TaskSummary(
            added_count=added_count,
            task_ids=task_ids,
            message=f"Successfully added {added_count} tasks"
        )
    
    def UpdateTasks(self, request_iterator, context):
        """Bidirectional streaming RPC: Update tasks and stream responses"""
        for update_request in request_iterator:
            task_id = update_request.id
            success = False
            message = f"Task with ID {task_id} not found"
            
            if task_id in self.tasks:
                if update_request.HasField('title'):
                    self.tasks[task_id]['title'] = update_request.title
                
                if update_request.HasField('description'):
                    self.tasks[task_id]['description'] = update_request.description
                
                if update_request.HasField('completed'):
                    self.tasks[task_id]['completed'] = update_request.completed
                
                success = True
                message = f"Task {task_id} updated successfully"
                print(f"Updated task: {self.tasks[task_id]}")
            
            yield todo_pb2.TaskUpdateResponse(
                id=task_id,
                success=success,
                message=message
            )
            time.sleep(0.5)  # Small delay to demonstrate streaming

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServiceServicer_to_server(TodoServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        print("Server stopped")

if __name__ == '__main__':
    serve()