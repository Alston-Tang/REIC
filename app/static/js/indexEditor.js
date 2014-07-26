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
        width:'text',
        height:'text',
        layer:'text'
    },
    setValue:function(dom){
        var $panelDom=$('#edit-panel');
        $panelDom.find('.width').val(parseFloat($(dom).attr('right'))-parseFloat($(dom).attr('left')));
        $panelDom.find('.height').val(parseFloat($(dom).attr('bot'))-parseFloat($(dom).attr('top')));
        $panelDom.find('.layer').val($(dom).css('z-index'));
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
        innerHTML:'textarea'
    },
    setValue:function(dom){
        $('#edit-panel').find('.innerHTML').html(dom.innerHTML);
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
        type:{
            type:'select',
            select:['none','fade']
        },
        trigger:{
            type:'select',
            select:['first']
        }
    },
    setValue:function(dom){
        $('#edit-panel').find('.type').val($(dom).children('.animation').attr('type'));
        $('#edit-panel').find('.select').val($(dom).children('.animation').attr('trigger'));
    },
    callback:function(){
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
    }
};

indexEditor.disModal=function(type,dom){
    if(indexEditor.modal[type]){
        this.deleteModalContent();
        this.createModalContent(indexEditor.modal[type],dom);
        $('#edit-modal').modal('show');
    }
};

indexEditor.createModalContent=function(m,dom){
    var root=document.getElementById('edit-panel');
    for(var name in m.con){
        var newDom=document.createElement('label');
        newDom.innerHTML=name;
        var newItem;
        switch (m.con[name]) {
            case 'text':
                newItem = document.createElement('input');
                break;
            case 'textarea':
                newItem = document.createElement('textarea');
                $(newItem).attr({'rows':30,'cols':50});
                break;
            default :
                if(typeof(m.con[name])=='object'){
                    switch (m.con[name].type){
                        case 'select':
                            var selObj=m.con[name];
                            newItem=document.createElement('select');
                            for(var i=0; i< selObj.select.length; i++){
                                var listName=indexEditor.mapName[selObj.select[i]]?indexEditor.mapName[selObj.select[i]]:selObj.select[i];
                                newItem.innerHTML+="<option value="+selObj.select[i]+">"+listName+"</option>";
                            }
                            break;
                        default :
                            break;
                    }
                }
        }
        $(newItem).addClass('form-control '+name);
        newDom.appendChild(newItem);
        root.appendChild(newDom);
    }
    $('#edit-panel-title').html(m.title);
    m.setValue(dom);
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