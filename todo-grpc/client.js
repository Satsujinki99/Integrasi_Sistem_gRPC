const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const packageDefinition = protoLoader.loadSync('./proto/todo.proto');
const todoProto = grpc.loadPackageDefinition(packageDefinition).todo;

const client = new todoProto.TodoService('localhost:50051', grpc.credentials.createInsecure());

// Tambahkan task
client.AddTask({ description: 'Belajar gRPC' }, (err, response) => {
    if (err) {
      console.error('AddTask Error:', err.message);
      return;
    }
    console.log('AddTask:', response.message);
  
    // Lihat semua task
    client.ListTasks({}, (err, response) => {
      if (err) {
        console.error('ListTasks Error:', err.message);
        return;
      }
      console.log('\nListTasks:');
      response.tasks.forEach(task => {
        console.log(`- [${task.done ? 'x' : ' '}] ${task.description} (${task.id})`);
      });

      // Tandai task pertama selesai
      if (response.tasks.length > 0) {
        const firstTask = response.tasks[0];
        client.MarkTaskDone({ id: firstTask.id }, (err, response) => {
          if (err) {
            console.error('MarkTaskDone Error:', err.message);
            return;
          }
          console.log('\nMarkTaskDone:', response.message);

          // Hapus task
          client.DeleteTask({ id: 'd921fb7e-c095-4ff5-895f-34061ab4bb80' }, (err, response) => {
            if (err) console.error("DeleteTask Error:", err.message);
            else console.log('DeleteTask:', response.message);
          });
        });
      }
    });
});
