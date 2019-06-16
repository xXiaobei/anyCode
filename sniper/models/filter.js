var mongoose = require("../mongo");

//定义集合模板
var s_filter = new mongoose.Schema({
    name: String
});

//指定集合索引,用于排序（1：正序，2：反序）
s_filter.index({ name: 1 });

//指定模板（映射）对应的集合名
s_filter.set("collection", "filter");

//查询
s_filter.statics.query = function(json) {
    return new Promise((resolve, reject) => {
        this.find(json, (err, res) => {
            if (err) reject(err);
            resolve(res);
        });
    });
};

module.exports = mongoose.model("filter", s_filter);
