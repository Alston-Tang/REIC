/**
 * Created by tang on 12/14/14.
 */

$(document).ready(function(){
    $('#delete-area').sortable({update:deleteSection});
    $('#assemble-area').sortable({connectWith:"#delete-area",revert:true, update:updatePreview});
    $('.section').draggable({connectToSortable:"#assemble-area", helper:"clone", revert:"Invalid"});
});

var deleteSection=function(e, ui){
    ui.item.remove()
};

var updatePreview=function(e, ui){
    var $assembleArea = $('#assemble-area');
    _clear();
    $assembleArea.children('.section').each(function(){
        var data=$(this).children('.preview-img').html();
        _appendImg(data);
    });
};

var _appendImg=function(data){
    var imgDom=document.createElement('img');
    imgDom.setAttribute('src', data);
    var container=document.getElementById('page-preview');
    container.appendChild(imgDom);
};


var _clear=function(){
    document.getElementById('page-preview').innerHTML="";
};

