import grpc
import sys
import os

# Add parent directory to path to import generated modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import todo_pb2
import todo_pb2_grpc

def generate_tasks_from_input():
    print("Masukkan task satu per satu. Ketik 'done' untuk selesai.\n")

    while True:
        title = input("📝 Judul task (atau 'done'): ").strip()
        if title.lower() == 'done':
            break

        description = input("📄 Deskripsi: ").strip()
        completed_input = input("✅ Sudah selesai? (y/n): ").strip().lower()
        completed = completed_input in ['y', 'yes']

        task = todo_pb2.Task(
            title=title,
            description=description,
            completed=completed
        )

        print(f"📤 Mengirim task: '{title}'\n")
        yield task

def run():
    print("=== 🛰️  Client Streaming RPC: Tambah Task Manual ===\n")
    
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = todo_pb2_grpc.TodoServiceStub(channel)
            response = stub.AddMultipleTasks(generate_tasks_from_input())

            print("\n✅ Respon dari Server:")
            print(f"Pesan         : {response.message}")
            print(f"Jumlah Ditambah: {response.added_count}")
            print(f"Task IDs      : {', '.join(response.task_ids)}")

    except grpc.RpcError as e:
        print(f"❌ gRPC Error: {e.code()} - {e.details()}")

if __name__ == '__main__':
    run()
