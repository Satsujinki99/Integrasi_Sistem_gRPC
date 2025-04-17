import grpc
import sys
import os

# Add parent directory to path to import generated modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import todo_pb2
import todo_pb2_grpc

def run():
    # Membuat channel gRPC
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = todo_pb2_grpc.TodoServiceStub(channel)

        print("=== 🔨 Tambah Task Baru (Unary RPC) ===")

        # Input manual dari user
        title = input("📝 Judul Task        : ").strip()
        description = input("📄 Deskripsi Task    : ").strip()
        completed_input = input("✅ Sudah selesai? (y/n): ").strip().lower()

        # Validasi
        if not title:
            print("❌ Judul tidak boleh kosong!")
            return

        completed = completed_input in ['y', 'yes']

        # Buat objek task
        task = todo_pb2.Task(
            title=title,
            description=description,
            completed=completed
        )

        try:
            # Panggil RPC
            response = stub.AddTask(task)
            print("\n📬 Respon dari Server:")
            print(f"🆔 ID      : {response.task_id}")
            print(f"📢 Pesan   : {response.message}")
            print(f"✅ Success : {response.success}")
        except grpc.RpcError as e:
            print(f"❌ Gagal menambahkan task: {e.details()}")

if __name__ == '__main__':
    run()
