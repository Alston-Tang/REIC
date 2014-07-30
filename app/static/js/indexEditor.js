/**
 * Created by Tang on 2014/6/24.
 */

if(!IndexBoard){
    console.log('Include indexBoard.js before that.');
}

var indexEditor={};

indexEditor.mapName={
    'fade':'fade in',
    'first':'first time'
};

indexEditor.preProcess=function(){
    b.traverse(function(){
        var cur=this;
        this.dom.indexEdit=this;
        $(this.dom).addClass('div-context');
        this.dom.drag=new drag({
            dom:cur.dom,
            size:cur.parent.dom
        });
        $(this.dom)
            .attr('touch-action','none')
            .on('thmdragend',function(){
            var sectionWidth=parseFloat(this.indexEdit.parent.parent.globalWidth);
            var sectionHeight=parseFloat(this.indexEdit.parent.bot)-parseFloat(this.indexEdit.parent.top);
            var sectionTop=parseFloat(this.indexEdit.parent.top);
            var left=parseFloat(this.offsetLeft)/sectionWidth;
            var width=parseFloat(this.offsetWidth)/sectionWidth;
            var top=(parseFloat(this.offsetTop)-sectionTop)/sectionHeight;
            var height=parseFloat(this.offsetHeight)/sectionHeight;

            this.indexEdit.resetWidthLeft(left,left+width);
            this.indexEdit.resetHeightTop(top,top+height);
        });
    });
};
indexEditor.modal={};
indexEditor.modal.size={
    title:'Size',
    con:{
        id:'size-panel',
        data: function(dom){
            var rv={};
            rv.width=parseFloat($(dom).attr('right'))-parseFloat($(dom).attr('left'));
            rv.height=parseFloat($(dom).attr('bot'))-parseFloat($(dom).attr('top'));
            rv.layer=$(dom).css('z-index');
            return rv;
        }
    },
    setValue:function(dom){
    },
    callback:function(){
        $('#edit-modal').modal('hide');
        var curDom=this.point;
        var curLeft=parseFloat($(this.point).attr('left'));
        var curTop=parseFloat($(this.point).attr('top'));
        var $panelDom=$('#edit-panel');
        curDom.indexEdit.resetLayer(parseInt($panelDom.find('.layer').val()));
        curDom.indexEdit.resetWidthLeft(curLeft,curLeft+parseFloat($panelDom.find('.width').val()));
        curDom.indexEdit.resetHeightTop(curTop,curTop+parseFloat($panelDom.find('.height').val()));
        this.point.drag.reHandlePos();
    }
};
indexEditor.modal.advanced={
    title:'Advanced',
    con:{
        id:'advanced-panel',
        data: function(dom){
            var rv={};
            rv.html=$(dom).html();
            return rv;
        }
    },
    setValue:function(dom){
    },
    callback:function(){
        $('#edit-modal').modal('hide');
        this.point.innerHTML=thmTools.textToHtml($('#edit-panel').find('.innerHTML').html());
        this.point.indexEdit.reNew();
        this.point.drag.reHandlePos();
    }
};

indexEditor.modal.delete={
    title:'Delete',
    con:{
        id:'delete-panel'
    },
    callback:function(){
        $('#edit-modal').modal('hide');
        $(this.point).remove();
        this.point.indexEdit.removeSelf();
    }
};

indexEditor.modal.animation={
    title:'Animation',
    con:{
        id:'animation-panel',
        data:function(dom){
            var rv={};
            rv.animation=[];
            $(dom).children('.animation').each(function(){
                var curAn={};
                curAn.type=$(this).attr('type');
                curAn.trigger=$(this).attr('trigger');
                curAn.speed=$(this).attr('speed');
                switch (curAn.type){
                    case 'fade':
                        break;
                    case 'move':
                        curAn.oriTop=$(this).attr('oriTop');
                        curAn.oriLeft=$(this).attr('oriLeft');
                        curAn.dstTop=$(this).attr('dstTop');
                        curAn.dstLeft=$(this).attr('dstLeft');
                        break;
                    case 'resize':
                        curAn.oriWidth=$(this).attr('oriWidth');
                        curAn.oriHeight=$(this).attr('oriHeight');
                        curAn.dstWidth=$(this).attr('dstWidth');
                        curAn.dstHeight=$(this).attr('dstHeight');
                        break;
                }
                rv.animation.push(curAn);
            });
            return rv;
        }
    },
    setValue:function(dom){
        $('.fa-minus').css({'cursor':'pointer'}).click(function(){
            $(this.parentNode).remove();
        });
        $('.fa-plus').css({'cursor':'pointer'}).click(function(){
            var newDiv=document.createElement('div');
            $(newDiv).addClass('animation').html(tmpl("animation-new-panel")).
                find('button').click(function(){
                    var type=$(newDiv).find('select').val();
                    var html="";
                    html+=tmpl("commonPanel",{'type':type});
                    html+=tmpl(type+"Panel",{});
                    html+="<hr>";
                    $(newDiv).html(html);
                    $('.fa-minus').css({'cursor':'pointer'}).click(function(){
                        $(this.parentNode).remove();
                    });
                });
            this.parentNode.insertBefore(newDiv,this);
        });
    },
    callback:function(){
        var animations=[];
        var panel=document.getElementById('edit-modal');
        $(panel).find('.animation').each(function(){
            var attr={};
            attr.type=$(this).find('.type').val();
            attr.trigger=$(this).find('.trigger').val();
            attr.speed=parseInt($(this).find('.speed').val());
            if (!attr.speed || attr.speed<=0){
                alert("speed should be a positive integer");
                return;
            }
            switch (attr.type){
                case 'fade':
                    break;
                case 'move':
                    attr.oriLeft=parseFloat($(this).find('.oriLeft').val());
                    attr.oriTop=parseFloat($(this).find('.oriTop').val());
                    attr.dstLeft=parseFloat($(this).find('.dstLeft').val());
                    attr.dstTop=parseFloat($(this).find('.dstTop').val());
                    if(!thmTools.isNumber([attr.dstLeft,attr.dstTop])){
                        alert("dstLeft and dstTop can not be empty");
                        return;
                    }
                    if(thmTools.inRange(0.0,1.0,[attr.oriLeft,attr.oriTop,attr.dstLeft,attr.dstTop])!='valid'){
                        alert(("left and top should be float number between 0.0 and 1.0"));
                        return;
                    }
                    break;
                case 'resize':
                    attr.oriWidth=parseFloat($(this).find('.oriWidth').val());
                    attr.oriHeight=parseFloat($(this).find('.oriHeight').val());
                    attr.dstWidth=parseFloat($(this).find('.dstWidth').val());
                    attr.dstHeight=parseFloat($(this).find('.dstHeight').val());
                    if(!thmTools.isNumber([attr.dstWidth,attr.dstHeight])){
                        alert("dstHeight and dstWidth can not be empty");
                        return;
                    }
                    if(thmTools.inRange(0.0,1.0,[attr.oriWidth,attr.oriHeight,attr.dstHeight,attr.dstWidth])!='valid'){
                        alert(("width and height should be float number between 0.0 and 1.0"));
                        return;
                    }
                    break;
            }
            animations.push(attr);
        });
        $('#edit-modal').modal('hide');
        var cur=this;
        $(this.point).find('.animation').each(function(){
            $(this).remove();
        });
        for (var i=0; i<animations.length; i++){
            var animation=document.createElement('span');
            $(animation).attr('class','animation');
            var element;
            for (element in animations[i]){
                //noinspection JSUnfilteredForInLoop
                if(!isNaN(animations[i][element]) || animations[i][element]) {
                    $(animation).attr(element, animations[i][element]);
                }
            }
            cur.point.appendChild(animation);
        }
        this.point.indexEdit.resetAnimation();
    }
};

indexEditor.disModal=function(type,dom){
    var m=indexEditor.modal[type];
    if(indexEditor.modal[type]){
        this.deleteModalContent();
        this.createModalContent(m,dom);
        if (m.setValue) m.setValue(dom);
        $('#edit-modal').modal('show');
    }
};

indexEditor.createModalContent=function(m,dom){
    var root=document.getElementById('edit-panel');
    var data= m.con.data? m.con.data(dom):{};
    $(root).html(tmpl(m.con.id,data));
    $('#edit-panel-title').html(m.title);
    var button=document.getElementById('edit-panel-save');
    button.point=dom;
    button.onclick=m.callback;
};
indexEditor.deleteModalContent=function(){
    var root=document.getElementById('edit-panel');
    root.innerHTML="";
};

//Extend Index Board
section.prototype.getCalPosReverse=function(absPos){
    var rtVal={};
    rtVal.left=absPos.left/this.parent.globalWidth;
    rtVal.right=absPos.right/this.parent.globalWidth;
    rtVal.top=(absPos.top-this.top)/(this.bot-this.top);
    rtVal.bot=(absPos.bot-this.top)/(this.bot-this.top);
    return rtVal;
};
section.prototype.reGetSize=function(){
    this.top=this.dom.offsetTop;
    this.bot=this.dom.offsetHeight+this.dom.offsetTop;
};
section.prototype.reCorrectHeight=function(){
    var _actBot=this.actBot;
    this.correctHeight();
    var pos;
    if(_actBot!=this.actBot){
        for(var i=0; i<this.parent.con.length; i++){
            if(this.parent.con[i]==this){
                pos=i;
                break;
            }
        }
        for(i=pos+1; i<this.parent.con.length; i++){
            this.parent.con[i].reGetSize();
            for(var j=0; j<this.parent.con[i].con.length; j++){
                this.parent.con[i].con[j].setTop();
                this.parent.con[i].con[j].dom.drag.reHandlePos();
            }
        }
    }
};
div.prototype.resetWidthLeft=function(left,right){
    if (left==undefined || right==undefined) return;
    $(this.dom).attr({'left':left,'right':right});
    this.setLeft();
    this.setWidth();
};
div.prototype.resetHeightTop=function(top,bot){
    if (top==undefined || bot==undefined) return;
    $(this.dom).attr({'top':top,'bot':bot});
    this.setTop();
    this.setHeight();
};
div.prototype.resetLayer=function(layer){
    if (layer==undefined) return;
    $(this.dom).attr({'layer':layer});
    this.setLayer();
};
div.prototype.resetAnimation=function(){
    this.setAnimation();
};
div.prototype.removeSelf=function(){
    for(var i=0; i<this.parent.con.length; i++){
        if(this.parent.con[i]==this){
            this.parent.con.splice(i,1);
            break;
        }
    }
    this.parent.reCorrectHeight();
};