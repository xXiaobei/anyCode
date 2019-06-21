var express = require("express");
var menu = require("../models/menu");
var router = express.Router();

/*包含词管理 */
router.get("/", (req, res, next) => {
    var g_menu = menu(2);
    res.render("i_keywords", { menu: g_menu });
});

module.exports = router;
