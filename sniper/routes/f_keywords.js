var express = require("express");
var menu = require("../models/menu");
var m_filter = require("../models/filter");
var pagination = require("../models/pagination");
var router = express.Router();

/*过滤词管理 */
router.get("/", (req, res, next) => {
    var g_menu = menu(3);
    res.render("f_keywords", { menu: g_menu });
});

/**
 * 初始化过滤词
 */
router.get("/init", (req, res, next) => {
    let g_pagination = new pagination();
    g_pagination.tableName = "filter";
    g_pagination.sortName = { name: 1 };
    m_filter.pagination(g_pagination).then(page => {
        res.send({ page: page });
    });
});

/**
 * 分页下一页
 */
router.post("/next", (req, res, next) => {
    let g_pagination = new pagination();
    g_pagination.setValues({
        pageSize: req.body.pSize,
        totalPages: req.body.pTotal,
        pageIndex: req.body.pIndex,
        tableName: req.body.pTabName,
        pageCounter: req.body.pCounter,
        sortName: JSON.parse(req.body.pSortName)
    });
    m_filter.pagination(g_pagination).then(page => {
        res.send({ page: page });
    });
});

/**
 * 新增过滤词
 */
router.post("/insert", (req, res, next) => {
    const f_kw = req.body.f_name;
    m_filter.insert({ name: f_kw }).then(
        result => {
            res.send({ msg: `过滤词：${f_kw} 成功创建！`, flg: 0 });
        },
        err => {
            res.send({ msg: `创建过滤词：${f_kw} 失败，${err}`, flg: 1 });
        }
    );
});

/**
 * 删除过滤词
 */
router.post("/delete", (req, res, next) => {
    const f_kw = req.body.f_name;
    m_filter.delMany({ name: f_kw }).then(
        result => {
            res.send({ msg: `${f_kw} 删除成功！`, flg: 0 });
        },
        err => {
            res.send({ msg: `${f_kw} 删除失败，${err}！`, flg: 1 });
        }
    );
});

module.exports = router;
