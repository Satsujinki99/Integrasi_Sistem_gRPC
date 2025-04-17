import grpc
import sys
import os

# Add parent directory to path to import generated modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import todo_pb2
import todo_pb2_grpc

import time

class TodoService(todo_pb2_grpc.TodoServiceServicer):
    def ListTasks(self, request, context):
        while True:
            tasks = get_latest_tasks()  # Ambil data dari DB atau memory
            for task in tasks:
                yield task
            time.sleep(5)  # Kirim ulang setiap 5 detik

import time

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = todo_pb2_grpc.TodoServiceStub(channel)

        while True:
            print("=== Listing All Tasks ===")
            empty = todo_pb2.Empty()
            responses = stub.ListTasks(empty)
            
            for task in responses:
                status = "Completed" if task.completed else "Not Completed"
                print(f"ID: {task.id}")
                print(f"Title: {task.title}")
                print(f"Description: {task.description}")
                print(f"Status: {status}")
                print("-" * 30)

            time.sleep(5)

if __name__ == '__main__':
    run()