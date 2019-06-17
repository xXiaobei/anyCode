var redis = require("redis");
var app = require("./app");
var server = require("http").createServer(app);
var socket = require("socket.io")(server);
var redisClient = redis.createClient(); //默认localhost 没有登录验证

var socketClient = null;

redisClient.on("ready", err => {
    server.listen(3999); //监听3999端口
    socket.on("connection", client => {
        socketClient = client; //获取当前的socket客户端
        client.on("disconnect", () => {
            console.log(`${client.id} disconnected ...`);
        });
        console.log("Socket connected with port 3999 ...");
    });
    console.log("Redis Server is ready working...");
});

//监听消息
redisClient.on("message", (channel, message) => {
    if (socketClient) {
        socketClient.emit("pullMessage", { c: channel, m: message });
    }
});

//订阅监听
redisClient.on("subscribe", (channel, count) => {
    console.log("client subscribed to " + channel + "," + count + " total subscriptions");
});

//退订监听
redisClient.on("unsubscribe", (channel, count) => {
    console.log("client unsubscribed from " + channel + ", " + count + " total subscriptions");
});

//redis错误监听
redisClient.on("error", err => {
    console.log("Redis Error " + error);
});

module.exports.redis = redisClient;
