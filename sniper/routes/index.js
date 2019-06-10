var express = require("express");
var menu = require("../models/menu");
var pagination = require("../models/pagination");
var m_main = require("../models/main");
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
    var g_pagination = pagination;
    g_pagination.tableName = "main";
    g_pagination.sortName = { name: 1 };
    m_main.pagination(g_pagination).then(page => {
        res.send({ page: page });
        // res.render("index", { title: "Express", page: page });
    });
});

/**
 * 分页下一页逻辑
 */
router.post("/nextPage", function(req, res, next) {
    let [pageSize, totalPages, tableName, sortName, pageCounter] = [
        req.body.pSize,
        req.body.pTotal,
        req.body.pTabName,
        req.body.pSortName,
        req.body.pCounter
    ];
});

module.exports = router;
