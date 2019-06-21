var mongoose = require("../mongo");

//定义集合模板
var s_filter = new mongoose.Schema({
    name: String
});

//指定集合索引,用于排序（1：正序，2：反序）
s_filter.index({ name: 1 });

//指定模板（映射）对应的集合名
s_filter.set("collection", "filter");

//自定义错误，用于中断逻辑链
class BreakSignal {
    constructor(err_msg) {
        this.msgTips = err_msg;
    }
}

//查询
s_filter.statics.query = function(json) {
    return new Promise((resolve, reject) => {
        this.find(json, (err, res) => {
            if (err) reject(err);
            resolve(res);
        });
    });
};

//新增
s_filter.statics.insert = function(json) {
    return new Promise((resolve, reject) => {
        this.find(json)
            .then(res => {
                if (res.length > 0)
                    throw new BreakSignal(` 已存在<strong>${json.name}</strong>，请勿重复添加！`);
                else return res;
            })
            .then(res => {
                return this.insertMany(json);
            })
            .then(res => {
                if (res.length > 0) resolve(res);
                else reject(`系统错误！`);
            })
            .catch(err => {
                reject(err.msgTips);
            });
    });
};

//删除
s_filter.statics.delMany = function(json) {
    return new Promise((resolve, reject) => {
        this.deleteOne(json)
            .then(res => {
                resolve(res);
            })
            .catch(err => {
                reject(err);
            });
    });
};

//分页数据
s_filter.statics.pagination = function(page) {
    return new Promise((resolve, reject) => {
        this.find()
            .sort(page.sortName)
            .skip((page.pageIndex - 1) * page.pageSize)
            .limit(page.pageSize)
            .then(docs => {
                page.result = docs;
                return this.aggregate([
                    { $group: { _id: null, count: { $sum: 1 } } },
                    { $project: { _id: 0 } }
                ]);
            })
            .then(c => {
                page.totalPages = c[0].count;
                page.pageCounter = Math.ceil(page.totalPages / page.pageSize); //求总页数
                page.firstPage = page.pageIndex == 1 ? true : false;
                page.lastPage = page.pageIndex == page.pageCounter ? true : false;
                resolve(page);
            })
            .catch(err => {
                reject(err);
            });
    });
};

module.exports = mongoose.model("filter", s_filter);
