/*
页面逻辑
*/

//#region  分页控件逻辑
/*分页逻辑*/
var pagination = {
    //初始化列表数据
    init: function() {
        let req_url = "/initData?" + Math.random();
        if ($(".mkw_page").length > 0) {
            req_url = "/mkw/init?" + Math.random();
        }
        if ($(".fkw_page").length > 0) {
            req_url = "/fkw/init?" + Math.random();
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
                let cust_data = "";
                let func = "home_page.work(this)";
                if (data[i].ip && data[i].channel) {
                    func = "";
                    cust_data = `disabled="disabled" data-channel="${data[i].channel}"`;
                }
                tr_html += "<tr><td>" + data[i].name + "</td>";
                tr_html +=
                    '<td><div class="" style="padding:5px;margin-bottom:0px;">...</div></td>';
                tr_html += '<td><button type="button" class="btn btn-default" title="查看包含词">';
                tr_html += '<span class="glyphicon glyphicon-pushpin"></span> </button>';
                tr_html +=
                    '<button type="button" class="btn btn-primary" title="查看已采集的词" onclick="home_page.result(this)">';
                tr_html += '<span class="glyphicon glyphicon-eye-open"></span> </button>';
                tr_html += `<button type="button" class="btn btn-success" title="开始采集" onclick="${func}" ${cust_data}>`;
                tr_html += '<span class="glyphicon glyphicon-play"></span> </button>';
                tr_html += "</td></tr>";
            }
            //生成主词列表
            if ($(".mkw_page").length > 0) {
                let html_counter = `<strong class="text-danger ts1">0</strong>`;
                if (data[i].includs.length > 0) {
                    const c = data[i].includs[0].words.length;
                    if (c > 0) {
                        html_counter = `<strong class="text-success ts1">${c}</strong>`;
                    }
                }
                tr_html += "<tr><td>" + data[i].name + "</td>";
                tr_html += `<td> ${html_counter} </td>`;
                tr_html += '<td><div class="btn-group" role="group" aria-label="Button group">';
                tr_html +=
                    '<button type="button" class="btn btn-default" title="编辑包含词" onclick="mkw_page.edit(this)">';
                tr_html += '<span class="glyphicon glyphicon-pencil"></span> </button>';
                tr_html +=
                    '<button type="button" class="btn btn-danger" title="删除关键词" onclick="mkw_page.delete(this)">';
                tr_html += '<span class="glyphicon  glyphicon-remove"></span> </button>';
                tr_html += "</td></tr>";
            }
            //生成过滤词列表
            if ($(".fkw_page").length > 0) {
                tr_html += "<tr><td>" + data[i].name + "</td>";
                tr_html += '<td><div class="btn-group" role="group" aria-label="Button group">';
                tr_html +=
                    '<button type="button" class="btn btn-danger" title="删除" onclick="fkw_page.delete(this)">';
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
            req_url = "/fkw/next";
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
                    console.log(error);
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

        p_html += `<li class="${p_pre_class}"><a href="javascript:;" class="pre">&laquo;</a></li>`;
        for (let i = 1; i <= data.pageCounter; i++) {
            if (i > 1) active = "";
            p_html += `<li class="${active}"><a href="javascript:;" class="cur">${i}</a></li>`;
        }
        p_html += `<li class="${p_next_class}"><a href="javascript:;" class="next">&raquo;</a></li></ul>`;

        $("#tab_main").data(page_next); //存储翻页数据
        $("#tab_foot").html(p_html); //初始化分页工具栏
        $(".pagination li").bind("click", pagination.pagination_next); //绑定翻页事件
    }
};

//#endregion

//#region 面板相关逻辑
/*面板逻辑 */
var home_page = {
    /**
     *定义socket服务ip地址
     */
    socketAdress: "",
    /**
     * 定义socket客户端链接对象
     */
    socketClient: null,
    /**
     * 保存采集任务的按钮
     */
    taskButtons: [],
    /**
     *初始化
     */
    init: function() {
        home_page.taskButtons = [];
        home_page.socketClient = io.connect(home_page.socketAdress);
        home_page.socketClient.on("pullMessage", data => {
            console.log(data);
            home_page.displayTips(data);
        });
    },
    /**
     * 开始/停止按钮切换逻辑
     * @param {} btn
     */
    btn_start_logic: function(btn, channel) {
        if (!btn) return false;
        let jq_ele = $(btn);
        if (!jq_ele.data("start")) {
            jq_ele
                .data("start", "start")
                .removeClass("btn-success")
                .addClass("btn-danger")
                .html('<span class="glyphicon glyphicon-stop"></span> ');
            jq_ele.attr("title", "停止采集");
            jq_ele.data("url", "/offwork");
            jq_ele.data("channel", channel); //绑定消息频道号
        } else {
            jq_ele
                .removeData("start")
                .removeClass("btn-danger")
                .addClass("btn-success")
                .html('<span class="glyphicon glyphicon-play"></span> ');
            jq_ele.attr("title", "开始采集");
            jq_ele.removeData("url");
        }
    },
    /**
     * 开始采集关键词
     */
    //prettier-ignore
    work: function(e) {
        let url = "/work";
        const jq_ele = $(e);
        const channel = $(e).data("channel") || "";
        const p_ele = $(e).parent().parent();
        const kw = $(p_ele).find("td").eq(0).text().trim();
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
                    if(jq_ele.data("init")) jq_ele.removeData("init");
                    else home_page.btn_start_logic(jq_ele, data.channel);
                    home_page.taskButtons.push(jq_ele);
                } else {
                    $.alert({
                        theme: "material",
                        animation: "scale",
                        type: "orange",
                        title: "警告",
                        columnClass: "col-md-6 col-md-offset-3",
                        content: data.msg
                    });
                }
            }
        });
    },
    /**
     * 显示当前关键词的采集进度
     */
    //prettier-ignore
    displayTips: function(d) {
        if (!d) return;
        let ele_tr = null;
        let btn_target = null;
        if(home_page.taskButtons.length == 0) {
            const trs = $("#tab_body tr");
            for(let i=0; i<trs.length; i++){
                const btn = $(trs[i]).find("td").eq(2).find("button").eq(2);
                if(btn.attr("disabled")) {
                    home_page.taskButtons.push(btn);
                }
            }
        }
        for (let i = 0; i < home_page.taskButtons.length; i++) {
            if ($(home_page.taskButtons[i]).data("channel") == d.c) {
                btn_target = $(home_page.taskButtons[i]);
                ele_tr = $(home_page.taskButtons[i]).parent().parent();
                break;
            }
        }

        let str_rep = "";
        let class_ele = "";
        const tips_ele = $(ele_tr).find("td").eq(1).find("div");
        $(tips_ele).removeClass(); //删除所有的class
        
        if (d.m.indexOf("<0>") !== -1) {
            str_rep = "<0>";
            class_ele = "alert alert-success";
        }
        if (d.m.indexOf("<1>") !== -1 || d.m.indexOf("<0.1>") != -1) {
            str_rep = d.m.indexOf("<1>") !== -1 ? "<1>" : "<0.1>";
            class_ele = "alert alert-warning";
        }
        if (d.m.indexOf("<2>") !== -1) {
            str_rep = "<2>";
            class_ele = "alert alert-danger";
        }
        if (d.m.indexOf("<3>") != -1) {
            //采集结束
            str_rep = "<3>";
            //重置按钮状态为开始
            if (btn_target[0].className.indexOf("btn-danger") != -1) {
                home_page.btn_start_logic(btn_target, d.c);
            }
            //重置数据库状态
            $(btn_target).data("init","init");
            $(btn_target).data("url","/offwork");
            home_page.work(btn_target);
        }
        d.m = d.m.replace(str_rep, "");
        $(tips_ele).addClass(class_ele).text(d.m);
        if(str_rep == "<3>") {
            //home_page.socketClient.disconnect();//断开socket链接
            //home_page.socketClient.removeAllListeners(); //取消所有监听
        }
    },
    /**
     * 查看已采集的关键词
     */
    result: function(ele, kw) {
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
//#endregion

//#region 主关键词页面逻辑
/*主关键词逻辑 */
var mkw_page = {
    /**
     * 存储模态窗口
     */
    dialogTarget: null,
    /**
     * 初始化
     */
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
    },
    /**
     * 编辑
     * @param {} e
     */
    //prettier-ignore
    edit: function(e) {
        if (!e) return;
        //let htmls = "", i_kws = "";
        let tbody = "", thead = "";
        const ele_tr = $(e).parent().parent().parent();
        const m_kw = ele_tr.find("td").eq(0).text().trim();
        const req_url = "/mkw/get_includes?kw=" + m_kw;
        $.getJSON(req_url, function(data) {
            var i_kws = data.kws;
            if (i_kws != "") {
                i_kws.split(",").forEach(k => {
                    tbody += `<tr><td>${k}</td>`;
                    tbody += `<td><a class="btn btn-primary pull-right" href="javascript:;" role="button" onclick="mkw_page.includs_logic(this)">`;
                    tbody += `<span class="glyphicon glyphicon-remove"></span>删除</a></td></tr>`;
                });
            } else {
                tbody += `<tr class="empty_tr"><td colspan="2">请添加包含词...</td>`;
            }
            
            thead += `<ul class="super_table">`; 
            thead += `<li style="width:381px;"><input id="m_ikw_name" class="form-control" type="text" placeholder="请输入包含词..."></li>`; 
            thead += `<li><button type="button" class="btn btn-primary" onclick="mkw_page.includs_logic(this)">添加</button></li>`;
            thead += `<li><button type="button" data-kw="${m_kw}" class="btn btn-primary" onclick="mkw_page.includs_logic(this)">保存</button></li></ul>`;

            const tb_htmls = `<table class="table table-hover"><tbody id="m_tbody_ikw">${tbody}</tbody></table>`;
            const content_htmls = thead + tb_htmls;

            mkw_page.dialogTarget = $.dialog({
                theme: "material",
                animation: "scale",
                type: "orange",
                title: `<span style="color:#06a3d9;">${m_kw}</span> 所属的包含词`,
                columnClass: "col-md-6 col-md-offset-3",
                content: content_htmls
            });
        });
    },
    /**
     * 包含词处理逻辑
     * @param {*} e
     */
    //prettier-ignore
    includs_logic: function(e) {
        const btn_type = $(e).text();
        if (btn_type == "删除") {
            $(e).parent().parent().remove();
        }
        if (btn_type == "添加") {
            let kw_htmls = ``;
            const kw = $("#m_ikw_name").val().trim();
            const empty_tr = $("#m_tbody_ikw tr[class='empty_tr']");
            kw_htmls += `<tr><td>${kw}</td>`;
            kw_htmls += `<td><a class="btn btn-primary pull-right" href="javascript:;" role="button" onclick="mkw_page.includs_logic(this)">`;
            kw_htmls += `<span class="glyphicon glyphicon-remove"></span>删除</a></td></tr>`;
            $(kw_htmls).appendTo($("#m_tbody_ikw"));
            if(empty_tr.length > 0) empty_tr.remove();
        }
        if (btn_type == "保存") {
            let kws = "";
            const m_kw = $(e).data("kw");
            const trs = $("#m_tbody_ikw").find("tr");
            for (let i = 0; i < trs.length; i++) {
                kws += $(trs[i]).find("td").eq(0).text().trim() + ",";
            }
            if (m_kw == "" || kws == "") return;
            kws = kws.substr(0, kws.length -1);
            $.ajax({
                url: "/mkw/save_includes",
                type: "POST",
                data: { i_kws: kws, m_kw: m_kw },
                dataType: "JSON",
                success: function(data) {
                    mkw_page.dialogTarget.close();
                    pagination.init();//刷新列表数据
                }
            });
        }
    }
};
//#endregion

//#region 过滤词逻辑
/*过滤词逻辑 */
var fkw_page = {
    /**
     *初始化
     */
    init: function() {
        $("#btnInsert").bind("click", fkw_page.insert);
    },
    /**
     *新增过滤词
     */
    insert: function() {
        const jc = $.confirm({
            theme: "material",
            closeIcon: true,
            animation: "scale",
            type: "orange",
            title: "新增过滤词",
            columnClass: "col-md-6 col-md-offset-3",
            content:
                '<div class="form-group">' +
                "<label>过滤词：</label>" +
                '<input type="text" id="f_name" class="form-control" placeholder="请输入过滤词名称..." required /></div>',
            buttons: {
                save: {
                    text: "保存",
                    btnClass: "btn-blue",
                    action: function() {
                        const f_name = this.$content.find("input#f_name").val();
                        if (f_name.trim()) {
                            $.ajax({
                                type: "POST",
                                dataType: "JSON",
                                url: "/fkw/insert",
                                data: { f_name: f_name.trim() },
                                success: function(data) {
                                    if (data.flg == 0) {
                                        pagination.init();
                                        jc.close();
                                    } else {
                                        jc.setContent(
                                            `<div class="alert alert-danger">${data.msg}</div>`
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
     * 删除过滤词
     */
    //prettier-ignore
    delete: function(e) {        
        const ele_tr = $(e).parent().parent().parent();
        const name_kw = ele_tr.find("td").eq(0).text().trim();
        var jc = $.confirm({
            title: "提示！",
            theme: "material",
            closeIcon: true,
            animation: "scale",
            type: "orange",
            columnClass: "col-md-6 col-md-offset-3",
            content: "确定要删除过滤词 <strong>" + name_kw + "</strong> ？",
            buttons: {
                save: {
                    text: "确认",
                    btnClass: "btn-blue",
                    action: function() {
                        $.ajax({
                            url: "/fkw/delete",
                            type: "POST",
                            dataType: "JSON",
                            data: { f_name: name_kw },
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
//#endregion

$(function() {
    //分页初始化
    pagination.init();

    //面板页逻辑
    if ($("#main_page").length > 0) {
        const ip = $("#main_page").data("ip");
        home_page.socketAdress = ip + ":3999";
        home_page.init();
    }
    //主词逻辑
    if ($(".mkw_page").length > 0) {
        mkw_page.init();
    }
    //过滤词逻辑
    if ($(".fkw_page").length > 0) {
        fkw_page.init();
    }
});
