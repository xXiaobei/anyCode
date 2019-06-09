var express = require("express");
var menu = require("../models/menu");
var router = express.Router();

/*过滤词管理 */
router.get("/", (req, res, next) => {
  var g_menu = menu(3);
  res.render("f_keywords", { menu: g_menu });
});

module.exports = router;
