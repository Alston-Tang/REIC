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
        var panel=document.getElementById('edit-modal');
        $(panel).find('.animation').each(function(){
            switch ($(this).find('.type').val()){
                case 'fade':
                    break;
                case 'move':
                    var oriLeft=parseFloat($(this).find('.oriLeft').val());
                    var oriTop=parseFloat($(this).find('.oriTop').val());
                    var dstLeft=parseFloat($(this).find('.dstLeft').val());
                    var dstTop=parseFloat($(this).find('.dstTop').val());
                    break;
                case 'resize':
                    var oriWidth=parseFloat($(this).find('.oriWidth').val());
                    var oriHeight=parseFloat($(this).find('.oriHeight').val());
                    var dstWidth=parseFloat($(this).find('.dstWidth').val());
                    var dstHeight=parseFloat($(this).find('.dstHeight').val());
                    break;
            }
        });
        /*
        $('#edit-modal').modal('hide');
        if($(this.point).find('.animation').length==0){
            if($('#edit-panel').find('.type').val()!='none'){
                var aniDom=document.createElement('span');
                $(aniDom).addClass('animation').attr({
                    type:$('#edit-panel').find('.type').val(),
                    trigger:$('#edit-panel').find('.trigger').val()
                });
                this.point.appendChild(aniDom);
            }
        }
        else{
            if($('#edit-panel').find('.type').val()=='none'){
                $(this.point).find('.animation').remove();
            }
            else{
                $(this.point).find('.animation').attr({
                    type:$('#edit-panel').find('.type').val(),
                    trigger:$('#edit-panel').find('.trigger').val()
                });
            }
        }
        this.point.indexEdit.reHandleAnimation();
        */
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