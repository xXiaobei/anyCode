var express = require("express");
var router = express.Router();

/*主关键词管理 */
router.get("/", (req, res, next) => {
    res.render('m_keywords');
});

module.exports = router;
