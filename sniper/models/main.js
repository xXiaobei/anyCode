//main文档mapping

var mongoose = require("../mongo");
var m_filter = require("./filter");
var m_include = require("./include");

//定义模板
var s_main = mongoose.Schema({
    ip: String,
    name: String,
    channel: String,
    status: String
});

//定义索引器 1:正序 -1:反序
s_main.index({ name: 1 });
//指定模板对应的集合名称
s_main.set("collection", "main");

//按条件查询
s_main.statics.query = function(json) {
    //this 指向 Model 而非函数本身或scheme
    return new Promise((resolve, reject) => {
        this.find(json, (err, result) => {
            if (err) reject(err);
            resolve(result);
        });
    });
};

//新增
s_main.statics.insert = function(json, callback) {
    return new Promise((resolve, reject) => {
        this.insertMany(json.mkw)
            .then(res => {
                return m_include.insertMany(json.ikw);
            })
            .then(res => {
                resolve(res);
            })
            .catch(err => {
                reject(err);
                console.log(err);
            });
    });
};

//更新
s_main.statics.edit = function(condition, json) {
    return new Promise((resolve, reject) => {
        this.updateOne(condition, json, (err, res) => {
            if (err) reject(err);
            resolve(res);
        });
    });
};

//删除主词
s_main.statics.delMany = function(json) {
    return new Promise((resolve, reject) => {
        this.deleteMany(json, (err, res) => {
            if (err) reject(err);
            resolve(res);
        });
    });
};

//删除(包含包含词)
s_main.statics.delete = function(json) {
    return new Promise((resolve, reject) => {
        let kw_includes = null;
        this.query(json)
            .then(res => {
                //查找主词、主词包含词
                if (res.length > 0) return m_include.query({ parent: res[0].name });
                else resolve("主词 " + json.name + " 不存在 ");
            })
            .then(res => {
                //删除主词
                kw_includes = res;
                return this.delMany(json);
            })
            .then(res => {
                //删除包含词
                if (kw_includes) {
                    return m_include.delete({ parent: json.name });
                } else {
                    resolve("主词 " + json.name + " 成功删除！");
                }
            })
            .then(res => {
                if (res) {
                    resolve(
                        `主词：${json.name} 和 ${kw_includes[0].words.length} 个包含词，成功删除！`
                    );
                }
            })
            .catch(function(err) {
                reject(err);
                console.log(err);
            });
    });
};

//获取活动的采集词个数
s_main.statics.live_counter = function() {
    return new Promise((resolve, reject) => {
        this.aggregate([
            { $match: { channel: { $ne: "" } } },
            { $group: { _id: null, count: { $sum: 1 } } }
        ])
            .then(res => {
                if (res.length > 0) resolve(res[0].count);
                else resolve(1); //首次执行默认为１
            })
            .catch(err => {
                reject(err);
                throw err;
            });
    });
};

//分页
s_main.statics.pagination = function(page, callback) {
    return new Promise((resolve, reject) => {
        this.aggregate([
            {
                $lookup: {
                    from: "include",
                    localField: "name",
                    foreignField: "parent",
                    as: "includs"
                }
            },
            { $project: { _id: 0, name: 1, channel: 1, ip: 1, status: 1, includs: { words: 1 } } },
            { $sort: page.sortName },
            { $skip: (page.pageIndex - 1) * page.pageSize },
            { $limit: page.pageSize }
        ])
            .then(docs => {
                page.result = docs;
                return this.aggregate([{ $group: { _id: null, count: { $sum: 1 } } }]);
            })
            .then(res => {
                page.totalPages = res[0].count;
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

module.exports = mongoose.model("main", s_main);
