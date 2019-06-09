//分页实体

module.exports = {
  pageCounter: 0, //总页数
  totalPages: 0, //总记录数
  pageIndex: 1, //当前页码
  pageSize: 10, //每一页数据
  sortName: "", //文档排序字段 json格式 {"name":1}
  tableName: "", //集合名
  result: [], //查询结果
  firstPage: true, //是否为第一页标识
  lastPage: false //是否为最后一页标识
};
