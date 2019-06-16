//分页实体

class pagination {
    constructor() {
        this.pageCounter = 0; //总页数
        this.totalPages = 0; //总记录数
        this.pageIndex = 1; //当前页码
        this.pageSize = 10; //每一页数据
        this.sortName = {}; //文档排序字段 json格式 {"name":1}
        this.tableName = ""; //集合名
        this.result = []; //查询结果
        this.firstPage = true; //是否为第一页标识
        this.lastPage = false; //是否为最后一页标识
    }
    setValues(obj) {
        if (obj) {
            try {
                if (obj.sortName) this.sortName = obj.sortName;
                if (obj.tableName) this.tableName = obj.tableName;
                if (obj.result) this.result = obj.result;
                if (obj.firstPage) this.firstPage = obj.firstPage;
                if (obj.lastPage) this.lastPage = obj.lastPage;
                if (obj.pageCounter) this.pageCounter = parseInt(obj.pageCounter);
                if (obj.totalPages) this.totalPages = parseInt(obj.totalPages);
                if (obj.pageIndex) this.pageIndex = parseInt(obj.pageIndex);
                if (obj.pageSize) this.pageSize = parseInt(obj.pageSize);
            } catch (error) {
                throw error;
            }
        }
    }
}
module.exports = pagination;

// module.exports = {
//     pageCounter: 0,
//     totalPages: 0,
//     pageIndex: 1,
//     pageSize: 10,
//     sortName: "",
//     tableName: "",
//     result: [],
//     firstPage: true,
//     lastPage: false
// };
