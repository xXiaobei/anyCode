/*
页面逻辑
*/

/*分页逻辑*/
var pagination = {
    //初始化列表数据
    init: function() {
        let req_url = "/initData?" + Math.random();
        if ($(".mkw_page").length > 0) {
            req_url = "/mkw/init?" + Math.random();
        }
        if ($(".fkw_page").length > 0) {
            req_url = "/initData?" + Math.random();
        }
        if ($(".ikw_page").length > 0) {
            req_url = "/initData?" + Math.random();
        }
        $.getJSON(req_url, function(data) {
            pagination.pagination_dispaly(data, true);
        });
    },
    /**
     * 显示数据到 面板 table
     * @param {*} data
     */
    dashboard_table: function(data) {
        if (!data) return;
        let tr_html = "";
        for (let i = 0; i < data.length; i++) {
            // 生成面板列表
            if ($("#main_page").length > 0) {
                tr_html += "<tr><td>" + data[i].name + "</td>";
                tr_html +=
                    '<td><div class="" style="padding:5px;margin-bottom:0px;">...</div></td>';
                tr_html += '<td><button type="button" class="btn btn-default" title="查看包含词">';
                tr_html += '<span class="glyphicon glyphicon-pushpin"></span> </button>';
                tr_html +=
                    '<button type="button" class="btn btn-primary" title="查看已采集的词" onclick="home_page.result(this)">';
                tr_html += '<span class="glyphicon glyphicon-eye-open"></span> </button>';
                tr_html +=
                    '<button type="button" class="btn btn-success" title="开始采集" onclick="home_page.work(this)">';
                tr_html += '<span class="glyphicon glyphicon-play"></span> </button>';
                // tr_html += '<button type="button" class="btn btn-default" title="暂停采集">';
                //tr_html += '<span class="glyphicon glyphicon-pause"></span> </button>';
                //tr_html += '<button type="button" class="btn btn-default" title="停止采集">';
                //tr_html += '<span class="glyphicon glyphicon-stop"></span> </button>';
                tr_html += "</td></tr>";
            }
            //生成主词列表
            if ($(".mkw_page").length > 0) {
                tr_html += "<tr><td>" + data[i].name + "</td>";
                tr_html += '<td><div class="btn-group" role="group" aria-label="Button group">';
                tr_html += '<button type="button" class="btn btn-default" title="查看过滤词">';
                tr_html += '<span class="glyphicon glyphicon-filter"></span> </button>';
                tr_html += '<button type="button" class="btn btn-default" title="查看包含词">';
                tr_html += '<span class="glyphicon glyphicon-pushpin"></span> </button>';
                tr_html +=
                    '<button type="button" class="btn btn-danger" title="删除关键词" onclick="mkw_page.delete(this)">';
                tr_html += '<span class="glyphicon  glyphicon-remove"></span> </button>';
                tr_html += "</td></tr>";
            }
        }
        $("#tab_body").html(tr_html);
    },
    /**
     * 加载分页数据到table
     * @param {} p
     * @param {是否生成分页的table} is_ptab
     */
    pagination_dispaly: function(p, is_ptab) {
        if (!p) return false;
        const page_data = p.page;
        const next_data = {
            firstPage: page_data.firstPage,
            lastPage: page_data.lastPage,
            pageSize: page_data.pageSize,
            totalPages: page_data.totalPages,
            sortName: page_data.sortName,
            tableName: page_data.tableName,
            pageCounter: page_data.pageCounter
        };
        pagination.dashboard_table(page_data.result);
        if (is_ptab) {
            pagination.pagination_table(next_data);
        }
    },
    /**
     * 分页下一页
     * @param {*} e
     */
    pagination_next: function(e) {
        const pdata = $("#tab_main").data();
        const page_index = pagination.pagination_logic(e, pdata);
        let req_url = "/nextPage";
        if ($(".mkw_page").length > 0) {
            req_url = "/mkw/next";
        }
        if ($(".fkw_page").length > 0) {
            req_url = "/initData?";
        }
        if ($(".ikw_page").length > 0) {
            req_url = "/initData?";
        }
        if (page_index) {
            $.ajax({
                type: "POST",
                url: req_url,
                dataType: "JSON",
                data: {
                    pIndex: page_index,
                    pTotal: pdata.totalPages,
                    pSize: pdata.pageSize,
                    pTabName: pdata.tableName,
                    pSortName: JSON.stringify(pdata.sortName),
                    pCounter: pdata.pageCounter
                },
                success: function(data) {
                    $("#tab_body").html("");
                    pagination.pagination_dispaly(data, false);
                },
                error: function(error) {
                    throw error;
                }
            });
        }
    },
    /**
     * 分页控件逻辑
     * @param {*} args
     * @param {*} page
     */
    pagination_logic: function(args, page) {
        if (!args) return false;

        let ele_a = args.target;
        let page_index = ele_a.innerText.trim();
        const ele_li = args.target.parentElement;
        const cur_idnex = $('.pagination li[class="active"]');
        const num_cur_index = parseInt(cur_idnex.text().trim());
        const ele_li_pre = $(".pagination .pre").parent();
        const ele_li_next = $(".pagination .next").parent();

        if (ele_li.className == "disabled" || ele_li.className == "active") {
            return false;
        }
        if (ele_a.className == "pre") {
            page_index = num_cur_index == 1 ? num_cur_index : num_cur_index - 1;
        }
        if (ele_a.className == "next") {
            page_index = num_cur_index == page.pageCounter ? num_cur_index : num_cur_index + 1;
        }
        if (ele_a.className == "next" || ele_a.className == "pre") {
            let ary_links = $(".pagination a[class='cur']");
            for (let i = 0; i < ary_links.length; i++) {
                if (ary_links[i].innerText.trim() == page_index) {
                    ele_a = ary_links[i];
                    break;
                }
            }
        }

        //分页元素样式控制
        if (page_index == 1) {
            ele_li_pre.addClass("disabled");
            ele_li_next.removeClass("disabled");
        } else {
            ele_li_pre.removeClass("disabled");
            ele_li_next.addClass(page_index == page.pageCounter ? "disabled" : "");
        }
        $(".pagination li").removeClass("active");
        ele_a.parentElement.className = "active";

        return page_index;
    },
    /**
     *分页面板生成
     * @param {*} data
     */
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

        p_html +=
            '<li class="' + p_pre_class + '"><a href="javascript:;" class="pre">&laquo;</a></li>';
        for (let i = 1; i <= data.pageCounter; i++) {
            if (i > 1) active = "";
            p_html +=
                '<li class="' + active + '"><a href="javascript:;" class="cur">' + i + "</a></li>";
        }
        p_html +=
            '<li class="' +
            p_next_class +
            '"><a href="javascript:;" class="next">&raquo;</a></li></ul>';

        $("#tab_main").data(page_next); //存储翻页数据
        $("#tab_foot").html(p_html); //初始化分页工具栏
        $(".pagination li").bind("click", pagination.pagination_next); //绑定翻页事件
    }
};

/**========================================================================== */
/*面板逻辑 */
var home_page = {
    /**
     * 定义消息通讯
     */
    socket: null,
    /**
     * 开始采集关键词
     */
    work: function(e) {
        let url = "/work";
        const jq_ele = $(e);
        const channel = $(e).data("channel") || "";
        const p_ele = $(e)
            .parent()
            .parent();
        const kw = $(p_ele)
            .find("td")
            .eq(0)
            .text()
            .trim();
        if ($(e).data("url")) {
            url = $(e).data("url");
        }
        $.ajax({
            type: "POST",
            url: url,
            dataType: "JSON",
            data: { kw: kw, channel: channel },
            success: function(data) {
                if (data.flg == 0) {
                    if (!jq_ele.data("start")) {
                        jq_ele
                            .data("start", "start")
                            .removeClass("btn-success")
                            .addClass("btn-danger")
                            .html('<span class="glyphicon glyphicon-stop"></span> ');
                        jq_ele.attr("title", "停止采集");
                        $(e).data("url", "/offwork");
                        $(e).data("channel", data.channel); //绑定消息频道号
                        home_page.socket.on("pullMessage", data => {
                            console.log(data);
                        });
                    } else {
                        jq_ele
                            .removeData("start")
                            .removeClass("btn-danger")
                            .addClass("btn-success")
                            .html('<span class="glyphicon glyphicon-play"></span> ');
                        jq_ele.attr("title", "开始采集");
                        $(e).removeData("url");
                    }
                    //home_page.displayTips(p_ele, kw);
                } else {
                    console.log(data.msg);
                }
            }
        });
    },
    /**
     * 显示当前关键词的采集进度
     */
    displayTips: function(ele, kw) {
        let interval = 1000; //魂环间隔为1000ms
        if (!ele) return false;
        let ele_tips = $(ele)
            .find("td")
            .eq(1)
            .find("div");
        if (ele_tips[0].className == "") {
            ele_tips.addClass("alert alert-success");
        }
        let tips = setInterval(() => {
            $.getJSON("/tips?kw=" + kw, data => {
                ele_tips.text(data.msg);
                if (data.flg == 1) clearInterval(tips);
            });
        }, interval);
    },
    /**
     * 查看已采集的关键词
     */
    result: function(ele, kw) {
        const client = io.connect("http://localhost:3999");
        if (!client) return;
        client.emit("pullMessage", "一肖一码", data => {
            console.log(data);
        });
        // kw = "一肖一码";
        // $.getJSON("/tips?kw=" + kw, data => {
        //     if (!data.msg) return;
        //     if (data.msg.startsWith("<")) {
        //         if (data.msg.startsWith("<1>")) {
        //             ele_tips.removeClass("alert-success").addClass("alert-warning");
        //         }
        //         if (data.msg.startsWith("<2>")) {
        //             ele_tips.removeClass("alert-success").addClass("alert-danger");
        //         }else{
        //             ele_tips.addClass("alert-success");
        //         }
        //     }
        //     ele_tips.text(data.msg);
        //     if (data.flg == "stop") clearInterval(tips);
        // });
    }
};

/**========================================================================== */
/*主关键词逻辑 */
var mkw_page = {
    init: function() {
        $("#btn_insert").bind("click", mkw_page.insert);
    },
    /**
     * 插入主关键词
     */
    insert: function() {
        const jc = $.confirm({
            theme: "material",
            closeIcon: true,
            animation: "scale",
            type: "orange",
            title: "新增主关键词",
            columnClass: "col-md-6 col-md-offset-3",
            content:
                '<div class="form-group">' +
                "<label>主词：</label>" +
                '<input type="text" id="m_name" class="form-control" placeholder="请输入主关键词名称..." required /></div>' +
                '<div class="form-group">' +
                "<label>包含词：</label>" +
                '<input type="text" id="i_name" class="form-control" placeholder="请输入主关键词的包含词，多个用英文逗号（,）隔开..." required /></div>',
            buttons: {
                save: {
                    text: "保存",
                    btnClass: "btn-blue",
                    action: function() {
                        const m_name = this.$content.find("input#m_name").val();
                        const i_name = this.$content.find("input#i_name").val();
                        if (m_name.trim()) {
                            $.ajax({
                                type: "POST",
                                dataType: "JSON",
                                url: "/mkw/insert",
                                data: { m_name: m_name.trim(), i_name: i_name.trim() },
                                success: function(data) {
                                    if (data.flg == 0) {
                                        pagination.init();
                                        return true;
                                    } else {
                                        jc.setContent(
                                            `<div class="alert alert-danger">${data.result}</div>`
                                        );
                                        jc.buttons.save.hide();
                                    }
                                }
                            });
                        }
                        return false;
                    }
                },
                cancel: {
                    text: "关闭",
                    btnClass: "btn-blue",
                    action: function() {}
                }
            }
        });
    },
    /**
     * 删除关键词
     */
    delete: function(ele) {
        const ele_parent = ele.parentElement.parentElement.parentElement;
        const name_kw = $(ele_parent)
            .find("td")
            .eq(0)
            .text();
        var jc = $.confirm({
            title: "提示！",
            theme: "material",
            closeIcon: true,
            animation: "scale",
            type: "orange",
            columnClass: "col-md-6 col-md-offset-3",
            content: "确定要删除主词 " + name_kw + " 以及它的 包含词？",
            buttons: {
                save: {
                    text: "确认",
                    btnClass: "btn-blue",
                    action: function() {
                        $.ajax({
                            url: "/mkw/delete",
                            type: "POST",
                            dataType: "JSON",
                            data: { m_name: name_kw },
                            success: function(data) {
                                jc.setContent(data.msg);
                                jc.buttons.save.hide();
                                pagination.init(); //刷新分页数据
                            }
                        });
                        return false;
                    }
                },
                cancel: {
                    text: "关闭",
                    btnClass: "btn-blue",
                    action: function() {}
                }
            }
        });
    }
};

/*过滤词逻辑 */
var fkw_page = {};

/*包含词语逻辑 */
var ikw_page = {};

$(function() {
    //分页初始化
    pagination.init();

    //面板页逻辑
    if ($("#main_page").length > 0) {
        home_page.socket = io.connect("http://localhost:3999");
    }
    //主词逻辑
    if ($(".mkw_page").length > 0) {
        mkw_page.init();
    }
    if ($(".ikw_page").length > 0) {
    }
    if ($(".fkw_page").length > 0) {
    }
});
