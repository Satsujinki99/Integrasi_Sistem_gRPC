import grpc
import sys
import os
import time

# Add parent directory to path to import generated modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import todo_pb2
import todo_pb2_grpc

def list_tasks(stub):
    print("📋 Daftar Task:")
    tasks = list(stub.ListTasks(todo_pb2.Empty()))
    for task in tasks:
        status = "✅ Selesai" if task.completed else "❌ Belum"
        print(f"- ID: {task.id} | Judul: {task.title} | Status: {status}")
    return tasks

def input_updates(tasks):
    print("\n🔄 Masukkan ID task yang ingin diupdate. Ketik 'done' untuk selesai.\n")
    while True:
        task_id = input("🆔 Task ID: ").strip()
        if task_id.lower() == 'done':
            break

        matching = next((t for t in tasks if t.id == task_id), None)
        if not matching:
            print("⚠️ Task ID tidak ditemukan.")
            continue

        title = input(f"  Ubah judul (kosong = tetap): ").strip()
        description = input(f"  Ubah deskripsi (kosong = tetap): ").strip()
        completed_input = input(f"  Tandai selesai? (y/n/kosong): ").strip().lower()

        update = todo_pb2.TaskUpdate(id=task_id)
        if title: update.title = title
        if description: update.description = description
        if completed_input in ['y', 'yes']:
            update.completed = True
        elif completed_input in ['n', 'no']:
            update.completed = False
        else:
            pass  # keep as is

        print(f"📤 Mengirim update untuk task ID: {task_id}")
        yield update
        time.sleep(0.5)

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = todo_pb2_grpc.TodoServiceStub(channel)

        tasks = list_tasks(stub)
        if not tasks:
            print("⚠️ Tidak ada task. Tambahkan task terlebih dahulu.")
            return

        print("\n=== 🔁 Bidirectional Streaming RPC: Update Task ===\n")
        updates = input_updates(tasks)
        responses = stub.UpdateTasks(updates)

        print("\n📬 Respon dari Server:")
        for res in responses:
            status = "✅ Berhasil" if res.success else "❌ Gagal"
            print(f"Task ID: {res.id} | Status: {status} | Pesan: {res.message}")

if __name__ == '__main__':
    run()
