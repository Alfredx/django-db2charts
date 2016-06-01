function isDeviceMobile() {
    var sUserAgent = navigator.userAgent.toLowerCase();
    var bIsIpad = sUserAgent.match(/ipad/i) == "ipad";
    var bIsIphoneOs = sUserAgent.match(/iphone os/i) == "iphone os";
    var bIsMidp = sUserAgent.match(/midp/i) == "midp";
    var bIsUc7 = sUserAgent.match(/rv:1.2.3.4/i) == "rv:1.2.3.4";
    var bIsUc = sUserAgent.match(/ucweb/i) == "ucweb";
    var bIsAndroid = sUserAgent.match(/android/i) == "android";
    var bIsCE = sUserAgent.match(/windows ce/i) == "windows ce";
    var bIsWM = sUserAgent.match(/windows mobile/i) == "windows mobile";
    var bIsWeChat = sUserAgent.match(/micromessenger/i) == 'micromessenger'
    if (bIsIpad || bIsIphoneOs || bIsMidp || bIsUc7 || bIsUc || bIsAndroid || bIsCE || bIsWM || bIsWeChat) {
        return true
    } else {
        return false
    }
}

function isWeChat() {
    return navigator.userAgent.toLowerCase().match(/micromessenger/i) == 'micromessenger';
}

function isAndroid() {
    return navigator.userAgent.toLowerCase().match(/android/i) == 'android';
}

function getState_ZHCN(state) {
    stateZHCN = {
        1: '购物车中',
        2: '已下单',
        3: '等待支付',
        4: '已付款',
        5: '付款已超时',
        6: '等待发货',
        7: '等待收货',
        8: '已收货',
        9: 'evaluating',
        10: '退款审核中',
        11: '退款申请拒绝',
        12: '退款申请通过',
        13: '等待买家退货',
        14: '买家已发货',
        15: '卖家已收货',
        16: '退款中',
        17: '已退款',
        18: '交易完成',
        19: '订单已删除',
        20: '交易关闭',
        24: '等待汇款审核',
    }
    var word = stateZHCN[Number(state)];
    if (!word)
        word = '未定义状态' + state;
    return word;
}


function getOrderType_ZHCN(type) {
    if (type.toLowerCase() == 'derivative')
        return '衍生品';
    else if (type.toLowerCase() == 'exhibit')
        return '展品'
}


function alert(msg) {
    $('#alert_msg').html(String(msg).replace(/\n/g, '<br>'));
    $('.modal-backdrop').css('z-index', 9000);
    $('#alert_btn').click();
}

function getUrlParam(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    var r = window.location.search.substr(1).match(reg); //匹配目标参数
    if (r != null) return decodeURI(r[2]);
    return null; //返回参数值
}
