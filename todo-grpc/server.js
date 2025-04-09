const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const { v4: uuidv4 } = require('uuid');

const packageDefinition = protoLoader.loadSync('./proto/todo.proto');
const todoProto = grpc.loadPackageDefinition(packageDefinition).todo;

const tasks = [];

function AddTask(call, callback) {
  const task = {
    id: uuidv4(),
    description: call.request.description,
    done: false,
  };
  tasks.push(task);
  callback(null, { message: `Task "${task.description}" added.` });
}

function ListTasks(call, callback) {
  callback(null, { tasks });
}

function MarkTaskDone(call, callback) {
  const task = tasks.find(t => t.id === call.request.id);
  if (task) {
    task.done = true;
    callback(null, { message: `Task "${task.description}" marked as done.` });
  } else {
    callback(null, { message: 'Task not found.' });
  }
}

DeleteTask: (call, callback) => {
    const taskId = call.request.id;
    const index = tasks.findIndex(t => t.id === taskId);
  
    if (index !== -1) {
      const removed = tasks.splice(index, 1);
      callback(null, { message: `Task "${removed[0].name}" deleted.` });
    } else {
      callback(null, { message: "Task not found." });
    }
  }
  

const server = new grpc.Server();
server.addService(todoProto.TodoService.service, {
  AddTask,
  ListTasks,
  MarkTaskDone,
});

server.bindAsync('0.0.0.0:50051', grpc.ServerCredentials.createInsecure(), () => {
  console.log('gRPC To-Do server running on port 50051');
});
