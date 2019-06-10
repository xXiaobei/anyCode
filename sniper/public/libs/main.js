/*
页面逻辑
*/

/*分页逻辑*/
var pagination = {
    //初始化列表数据
    init: function() {
        $.getJSON("/initData", function(data) {
            const jd = data.page;
            const page_data = {
                firstPage: jd.firstPage,
                lastPage: jd.lastPage,
                pageSize: jd.pageSize,
                totalPages: jd.totalPages,
                sortName: jd.sortName,
                tableName: jd.tableName,
                pageCounter: jd.pageCounter
            };

            pagination.dashboard_table(jd.result);
            pagination.pagination_table(page_data);
        });
    },
    //显示数据到 面板 table
    dashboard_table: function(data) {
        if (!data) return;
        let tr_html = "";
        for (let i = 0; i < data.length; i++) {
            tr_html += "<tr><td>" + data[i].name + "</td>";
            tr_html += "<td><a>已获取50个关键词...点击查看结果</a></td>";
            tr_html += '<td><div class="btn-group" role="group" aria-label="Button group">';
            tr_html += '<button type="button" class="btn btn-default" title="查看过滤词">';
            tr_html += '<span class="glyphicon glyphicon-filter"></span> </button>';
            tr_html += '<button type="button" class="btn btn-default" title="查看包含词">';
            tr_html += '<span class="glyphicon glyphicon-pushpin"></span> </button>';
            tr_html += '<button type="button" class="btn btn-default" title="开始采集">';
            tr_html += '<span class="glyphicon glyphicon-play"></span> </button>';
            tr_html += '<button type="button" class="btn btn-default" title="暂停采集">';
            tr_html += '<span class="glyphicon glyphicon-pause"></span> </button>';
            tr_html += '<button type="button" class="btn btn-default" title="停止采集">';
            tr_html += '<span class="glyphicon glyphicon-stop"></span> </button></td></tr>';
        }
        $("#tab_body").html(tr_html);
    },
    //分页下一页
    pagination_next: function(e) {
        const ele_a = e.target;
        const ele_li = e.target.parentElement;
        if (ele_li.className == "disabled" || ele_li.className == "active") {
            return false;
        }

        const pdata = $("#tab_main").data();
        const next_num = ele_a.innerText.trim();
        const cur_num = $(".pagination li[class='active']");

        $.ajax({
            type: "POST",
            url: "/nextPage",
            dataType: "JSON",
            data: {
                pTotal: pdata.totalPages,
                pSize: pdata.pageSize,
                pTabName: pdata.tableName,
                pSortName: JSON.stringify(pdata.sortName),
                pCounter: pdata.pageCounter
            },
            success: function(data) {
                console.log(data);
            },
            error: function(error) {
                throw error;
            }
        });

        //console.log(ele_live.text());
        e.preventDefault();
    },
    //分页面板生成
    pagination_table: function(data) {
        if (!data) return;
        if (data.pageCounter <= 1) return;
        let active = "active";
        let p_pre_class = data.firstPage ? "disabled" : "";
        let p_next_class = data.lastPage ? "disabled" : "";
        let p_html = '<ul class="pagination pull-right" style="margin-top:0px;">';

        const page_next = {
            pageSize: data.pageSize,
            tableName: data.tableName,
            sortName: data.sortName,
            pageCounter: data.pageCounter,
            totalPages: data.totalPages
        };

        p_html += '<li class="' + p_pre_class + '"><a href="#" class="pre">&laquo;</a></li>';
        for (let i = 1; i <= data.pageCounter; i++) {
            if (i > 1) active = "";
            p_html += '<li class="' + active + '"><a href="#" class="cur">' + i + "</a></li>";
        }
        p_html += '<li class="' + p_next_class + '"><a href="#" class="next">&raquo;</a></li>';

        $("#tab_main").data(page_next); //存储翻页数据
        $("#tab_foot").html(p_html); //初始化分页工具栏
        $(".pagination li").bind("click", pagination.pagination_next); //绑定翻页事件
    }
};

/*面板逻辑 */
var home_page = {};

/*主关键词逻辑 */
var mkw_page = {};

/*过滤词逻辑 */
var fkw_page = {};

/*包含词语逻辑 */
var ikw_page = {};

$(function() {
    //分页初始化
    pagination.init();

    if ($("#main_page")) {
    }
    if ($("#mkw_page")) {
    }
    if ($("#ikw_page")) {
    }
    if ($("#fkw_page")) {
    }
});
