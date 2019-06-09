var express = require("express");
var menu = require("../models/menu");
var pagination = require("../models/pagination");
var m_main = require("../models/main");
var router = express.Router();

/* GET home page. */
router.get("/", function(req, res, next) {
  var g_menu = menu(0);
  var g_pagination = pagination;
  g_pagination.tableName = "main";
  g_pagination.sortName = { name: 1 };
  m_main.pagination(g_pagination).then(page => {
    res.render("index", { title: "Express", menu: g_menu, page: page });
  });
});

module.exports = router;
