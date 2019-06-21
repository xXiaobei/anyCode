//菜单实体

//定义实体
var Menu = {
    // 实例化
    create: () => {
        var menu = {};
        menu.id = 0; //菜单id
        menu.url = ""; //菜单url
        menu.name = ""; //菜单名称
        menu.active = ""; //是否激活
        return menu;
    }
};

/**
 * 生成默认菜单
 * @param id  菜单的id
 */
const generator = function(id) {
    let menus = [];
    let m_id = id || 0;

    const m_home = Menu.create();
    m_home.url = "/";
    m_home.name = "面板";
    m_home.active = "active";
    menus.push(m_home);

    const m_mkw = Menu.create();
    m_mkw.id = 1;
    m_mkw.url = "/mkw";
    m_mkw.name = "主词管理";
    m_mkw.active = "";
    menus.push(m_mkw);

    const m_ikw = Menu.create();
    m_ikw.id = 2;
    m_ikw.url = "/ikw";
    m_ikw.name = "包含词管理";
    m_ikw.active = "";
    //menus.push(m_ikw);

    const m_fkw = Menu.create();
    m_fkw.id = 3;
    m_fkw.url = "/fkw";
    m_fkw.name = "过滤词管理";
    m_fkw.active = "";
    menus.push(m_fkw);

    menus.forEach(ele => {
        if (ele.id == m_id) {
            ele.active = "active";
        } else {
            ele.active = "";
        }
    });

    return menus;
};

//module.exports.menu = Menu; //将自定义模块menu 映射到generator函数, module.exports 暴露出去的为一个类
//exports.menu = generator; //将自定义模块menu 映射到generator函数，暴露出去的为一个函数
module.exports = generator;
