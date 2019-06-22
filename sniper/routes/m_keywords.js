var express = require("express");
var menu = require("../models/menu");
var pagination = require("../models/pagination");
var m_main = require("../models/main");
var m_include = require("../models/include");
var router = express.Router();

/*主关键词管理 */
router.get("/", (req, res, next) => {
    var g_menu = menu(1);
    res.render("m_keywords", { menu: g_menu });
});

/**
 * 初始化分页数据
 */
router.get("/init", (req, res, next) => {
    let g_pagination = new pagination();
    g_pagination.tableName = "main";
    g_pagination.sortName = { name: 1 };
    m_main.pagination(g_pagination).then(page => {
        res.send({ page: page });
    });
});

/**
 * 分页下一页数据
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
    m_main.pagination(g_pagination).then(page => {
        res.send({ page: page });
    });
});

/**
 * 主关键词保存
 */
router.post("/insert", (req, res, next) => {
    let ikw_ary = [];
    const mkw_name = req.body.m_name;
    const include_words = req.body.i_name;

    if (include_words != "" && include_words.indexOf(",") != -1) {
        ikw_ary = include_words.split(",");
    }

    const d_json = {
        mkw: { name: mkw_name, ip: "", status: "", channel: "" },
        ikw: { parent: mkw_name, words: ikw_ary }
    };

    m_main.find(d_json.mkw, (err, result) => {
        if (result.length > 0) {
            res.send({ result: `主词${d_json.mkw.name}已存在，请勿重复添加！`, flg: 1 });
        } else {
            m_main.insert(d_json).then(
                result => {
                    res.send({ result: result, flg: 0 });
                },
                err => {
                    res.send({ result: err, flg: 1 });
                }
            );
        }
    });
});

/**
 * 主关键词删除
 */
router.post("/delete", (req, res, next) => {
    const mkw_name = req.body.m_name;
    const d_json = { name: mkw_name };
    m_main.delete(d_json).then(
        result => {
            res.send({ msg: result, flg: 1 });
        },
        result => {
            res.send({ msg: result, flg: 0 });
        }
    );
});

/**
 *获取当前主关键词的包含词
 */
router.get("/get_includes", (req, res, next) => {
    const m_kw = req.query["kw"];
    m_include.query({ parent: m_kw }).then(
        docs => {
            let kws = "";
            if (docs.length > 0) {
                docs[0].words.forEach(k => {
                    kws += k + ",";
                });
                kws = kws.substr(0, kws.length - 1);
            }
            res.send({ kws: kws, flg: 0 });
        },
        err => {
            res.send({ kws: "", flg: 1 });
        }
    );
});

/**
 * 主关键词所属的包含词的修改
 */
router.post("/save_includes", (req, res, next) => {
    const i_kws = req.body.i_kws;
    const m_kw = req.body.m_kw;

    let ary_ikw = [];
    if (i_kws.indexOf(",") != -1) ary_ikw = i_kws.split(",");
    else ary_ikw.push(i_kws);

    const c_json = { parent: m_kw };
    const u_json = { $set: { words: ary_ikw } };

    m_include.update(c_json, u_json).then(
        result => {
            res.send({ msg: "", flg: 0 });
        },
        err => {
            res.send({ msg: "", flg: 1 });
        }
    );
});

module.exports = router;
