/**
 * Created by Tang on 2014/6/24.
 */
var thmTools= {
    propertyRequire: function (obj, require) {
        if (!require) return false;
        for (var i = 0; i < require.length; i++) {
            if (!obj.hasOwnProperty(require[i])) return false;
        }
        return true;
    },
    absPos:function(dom){
        var rtVal={left:dom.offsetLeft,top:dom.offsetTop};
        var fVal=dom.offsetParent?thmTools.absPos(dom.offsetParent):{left:0,top:0};
        rtVal.left+=fVal.left;
        rtVal.top+=fVal.top;
        return rtVal;
    },
    relPos: function (dom) {
        var rtVal = {};
        rtVal.left = ($(dom).css('left') && $(dom).css('left') != 'auto') ? parseFloat($(dom).css('left')) : dom.offsetLeft;
        rtVal.right = rtVal.left + dom.offsetWidth;
        rtVal.top = ($(dom).css('top') && $(dom).css('top') != 'auto') ? parseFloat($(dom).css('top')) : dom.offsetTop;
        rtVal.bot = rtVal.top + dom.offsetHeight;
        return rtVal;
    },
    decodeAttr:function(attr){
        var t=attr.split(';');
        var rt={};
        for(var i=0; i< t.length; i++){
            var t2=t[i].split(':');
            rt[t2[0].trim()]=t2[1]?t2[1]:true;
        }
        return rt;
    },
    textToHtml:function(str){
        str=str.replace(/&quot;/g,'"');
        str=str.replace(/&amp;/g,'&');
        str=str.replace(/&lt;/g,'<');
        str=str.replace(/&gt;/g,'>');
        return str;
    },
    inRange:function(min,max,list){
        for(var i=0; i<list.length; i++){
            if(!isNaN(list[i]) && (list[i]>max || list[i]<min)){
                return i;
            }
        }
        return 'valid';
    },
    isNumber:function(list){
        for(var i=0; i<list.length; i++){
            if (isNaN(list[i])) {return false;}
        }
        return true;
    }
};