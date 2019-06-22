var mongoose = require("../mongo");

//定义集合的模板
var s_include = new mongoose.Schema({
    parent: String,
    words: [{ type: String }]
});

//指定模板对应的集合名称
s_include.set("collection", "include");

//查询
s_include.statics.query = function(json) {
    return new Promise((resolve, reject) => {
        this.find(json, (err, res) => {
            if (err) reject(err);
            resolve(res);
        });
    });
};

//删除
s_include.statics.delete = function(json) {
    return new Promise((resolve, reject) => {
        this.deleteMany(json, (err, res) => {
            if (err) reject(err);
            resolve(res);
        });
    });
};

//新增
s_include.statics.insert = function(json) {
    return new Promise((resolve, reject) => {
        this.insertMany(json, (err, res) => {
            if (err) reject(err);
            resolve(res);
        });
    });
};

//更新
s_include.statics.update = function(condition, json) {
    return new Promise((resolve, reject) => {
        this.find({ parent: condition.parent })
            .then(res => {
                if (res.length > 0) return this.updateOne(condition, json);
                else return this.insertMany({ parent: condition.parent, words: json.$set.words });
            })
            .then(res => {
                resolve(res);
            })
            .catch(err => {
                reject(err);
                throw err;
            });
        // this.updateOne(condition, json, (err, res) => {
        //     if (err) reject(err);
        //     resolve(res);
        // });
    });
};

module.exports = mongoose.model("include", s_include);
