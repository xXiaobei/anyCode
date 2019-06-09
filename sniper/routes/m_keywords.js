var express = require("express");
var menu = require("../models/menu");
var router = express.Router();

/*主关键词管理 */
router.get("/", (req, res, next) => {
  var g_menu = menu(1);
  res.render("m_keywords", { menu: g_menu });
});

module.exports = router;
