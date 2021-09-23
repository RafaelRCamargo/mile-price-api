const http = require("http");

//Routes
const app = require("./app");

//Projects starts on default project port 
//but if its busy jumps to another one
const port = process.env.PORT || 3000;

//Start Http Server
const server = http.createServer(app);
server.listen(port);