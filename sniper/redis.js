var redis = require("redis");
var app = require("./app");
var server = require("http").createServer(app);
var socket = require("socket.io")(server);
var redisClient = redis.createClient(); //默认localhost 没有登录验证

var socketClient = [];

redisClient.on("ready", err => {
    server.listen(3999); //监听3999端口
    socket.on("connection", client => {
        // socketClient = client; //获取当前的socket客户端
        socketClient.push(client);
        client.on("disconnect", () => {
            console.log(`${client.id} disconnected ...`);
        });
        console.log(`Socket：${client.id} connected with port 3999 ...`);
    });
    console.log("Redis Server is ready working...");
});

//监听消息
redisClient.on("message", (channel, message) => {
    if (socketClient) {
        //循环所有客户端，并发送消息
        socketClient.forEach(c => {
            c.emit("pullMessage", { c: channel, m: message }, (err, msg) => {
                //关键词采集结束,则取消该频道的订阅
                if (message.startsWith("<3>")) redisClient.unsubscribe(channel);
            });
        });
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
