// 数据库辅助类

var mongoose = require("mongoose");
//修改mongoose的promise为全局的promise
//mongoose提供的promise是不完整的promise
mongoose.Promise = global.Promise;

const db_host = "localhost";
const db_port = "27017";
const db_name = "keywords";
const db_link_url = "mongodb://" + db_host + ":" + db_port + "/" + db_name;

// 定义数据库对象
class app {
    // 多次连接共享实例对象
    static getInstance() {
        if (!app.instance) {
            app.instance = new app();
        }
        // 简化性能提升
        return app.instance;
    }

    //默认初始化执行方法
    constructor() {
        //初始化连接对象
        mongoose.connect(db_link_url, {
            useCreateIndex: true,
            useNewUrlParser: true
        });
        //存放mongoose对象
        this.db = mongoose;
    }
}

// 成功链接
mongoose.connection.on("connected", () => {
    console.log("Mongodb connected successfuly!");
});
// 链接错误
mongoose.connection.on("error", err => {
    console.log("Mongodb connected with err!");
    throw err;
});
//断开链接
mongoose.connection.on("error", () => {
    console.log("Mongodb disconnected...");
});

//导出模块
module.exports = app.getInstance().db;
