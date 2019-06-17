var path = require("path");
var express = require("express");
var redisClient = require("redis");
var redis_sub = require("../redis").redis;
var menu = require("../models/menu");
var pagination = require("../models/pagination");
var m_main = require("../models/main");
var spawn = require("child_process").spawn;
var router = express.Router();

/* GET home page. */
router.get("/", function(req, res, next) {
    var g_menu = menu(0);
    res.render("index", { title: "Express", menu: g_menu });
});

/**
 * 初始化分页数据
 */
router.get("/initData", function(req, res, next) {
    let g_pagination = new pagination();
    g_pagination.tableName = "main";
    g_pagination.sortName = { name: 1 };
    m_main.pagination(g_pagination).then(page => {
        res.send({ page: page });
    });
});

/**
 * 分页下一页逻辑
 */
router.post("/nextPage", function(req, res, next) {
    let g_pagination = new pagination();
    g_pagination.setValues({
        pageSize: req.body.pSize,
        totalPages: req.body.pTotal,
        pageIndex: req.body.pIndex,
        tableName: req.body.pTabName,
        pageCounter: req.body.pCounter,
        sortName: JSON.parse(req.body.pSortName)
    });
    m_main.pagination(g_pagination).then(page => {
        res.send({ page: page });
    });
});

/**
 * 调用python 开始采集关键词
 */
router.post("/work", function(req, res, next) {
    try {
        const kw = req.body.kw;
        const channel = Date.now(); // 设置当前关键词的消息发布频道
        const env_path = "/home/bbei/Documents/pythonVenv/anycode/bin/python3";
        const py_path = path.join(path.dirname(__dirname), "sniper.py");
        redis_sub.subscribe(channel); //redis 订阅消息频道
        const py_procss = spawn(env_path, [py_path, kw, channel]);
        res.send({ msg: "success", flg: 0, channel: channel });
    } catch (error) {
        res.send({ msg: "采集失败，请重试！" + error, flg: 1 });
    }
});

/**
 * 停止关键词采集
 */
router.post("/offwork", function(req, res, next) {
    try {
        //链接到localhost，没有密码相关
        const redis = redisClient.createClient();
        const kw = req.body.kw;
        const channel = req.body.channel;
        redis.hset(kw, "status", "stop");
        redis_sub.unsubscribe(channel); //取消消息频道订阅
        res.send({ msg: "", flg: 0 });
    } catch (error) {
        res.send({ msg: "停止错误，请重！", flg: 1 });
    }
});

/**
 * 拉取关键词采集进度
 */
router.get("/tips", function(req, res, next) {
    const params = req.query;
    // redisClient.hvals(params["kw"], (err, res) => {
    //     res.send({ msg: res[0], flg: res[1] });
    // });
});

module.exports = router;
