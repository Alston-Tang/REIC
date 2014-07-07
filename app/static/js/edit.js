/**
 * Created by Tang on 2014/6/24.
 */
/**
 * Created by Tang on 2014/6/5.
 */

var root;
var b;


var initial=function(){
    root=document.getElementById('index-board');

    var opt={
        navOff:thmTools.absPos(document.getElementById('nav-bar')).top
    };
    b=new IndexBoard(root,opt);

    indexEditor.preProcess();
    $(function(){
        $.contextMenu({
            selector: '.div-context',
            zIndex:100,
            callback: function(key, options) {
                switch (key){
                    case 'edit':
                        indexEditor.disModal('size',this[0]);
                        break;
                    case 'advanced':
                        indexEditor.disModal('advanced',this[0]);
                        break;
                    case 'animation':
                        indexEditor.disModal('animation',this[0]);
                        break;
                }
                //var m = "clicked: " + key + " on " + $(this).html();
                //window.console && console.log(m) || alert(m);
            },
            items: {
                "edit": {name: "Edit"},
                "animation": {name: "Animation"},
                "copy": {name: "Copy"},
                "paste": {name: "Paste"},
                "delete": {name: "Delete"},
                "sep1": "---------",
                "advanced": {name: "Advanced"}
            }
        });
    });
};
$(document).ready(initial);