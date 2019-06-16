var express = require("express");
var path = require("path");
var menu = require("../models/menu");
var pagination = require("../models/pagination");
var m_main = require("../models/main");
var router = express.Router();
var spawn = require("child_process").spawn;
var redis = require("redis");
var redisClient = redis.createClient(); //默认localhost 没有登录验证

/**
 * 判断redis是否登录成功
 */
redisClient.on("ready", err => {
    console.log("Redis Server working...");
});

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
        const tipMsg = "程序准备中...";
        const env_path = "/home/bbei/Documents/pythonVenv/anycode/bin/python3";
        const py_path = path.join(path.dirname(__dirname), "sniper.py");
        redisClient.hmset(kw, "status", "start", "msg", tipMsg);
        const py_procss = spawn(env_path, [py_path, kw]);
        res.send({ msg: "success", flg: 0 });
    } catch (error) {
        res.send({ msg: "采集失败，请重试！" + error, flg: 1 });
    }
});

/**
 * 停止关键词采集
 */
router.post("/offwork", function(req, res, next) {
    try {
        const kw = req.body.kw;
        redisClient.hset(kw, "status", "stop");
        res.send({ msg: "", flg: 0 });
    } catch (error) {
        res.send({ msg: "停止错误，请重！", flg: 1 });
    }
});

module.exports = router;
