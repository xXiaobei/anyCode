//main文档mapping
/// <reference path="../typings/index.d.ts" />

var mongoose = require("../mongo");

//定义模板
var s_main = mongoose.Schema({
  name: String
});

//定义索引器 1:正序 -1:反序
s_main.index({ name: 1 });
//指定模板对应的集合名称
s_main.set("collection", "main");

//按条件查询
s_main.statics.query = function(json, callback) {
  //this 指向 Model 而非函数本身或scheme
  return this.find(json, callback);
};

//新增
s_main.statics.insert = function(json, callback) {
  return this.insertMany(json, (err, m) => {
    if (err) throw err;
    callback(m);
  });
};

//更新
s_main.statics.update = function(condition, json, callback) {
  return this.update(condition, json, (err, raw) => {
    if (err) throw err;
    callback(raw);
  });
};

//删除
s_main.statics.delete = function(json, callback) {
  this.remove(json).exec(callback);
};

//分页
s_main.statics.pagination = function(page, callback) {
  return new Promise((resolve, reject) => {
    this.find()
      .sort(page.sortName)
      .skip((page.pageIndex - 1) * page.pageSize)
      .limit(page.pageSize)
      .then(docs => {
        page.result = docs;
        return this.count();
      })
      .then(c => {
        page.totalPages = c;
        page.pageCounter = Math.ceil(page.totalPages / page.pageSize); //求总页数
        page.firstPage = page.pageIndex == 1 ? true : false;
        page.lastPage = page.pageIndex == page.pageCounter ? true : false;
        resolve(page);
      })
      .catch(err => {
        throw err;
      });
  });
};

module.exports = mongoose.model("main", s_main);
