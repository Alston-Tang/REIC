/**
 * Created by Tang on 2014/6/5.
 */
var list;

var IndexBoard=function(root,opt){
    list=this;
    this.navOff=0;
    if(opt)
    {
        if (opt.navOff) this.navOff=opt.navOff;
    }
    this.root=root;
    this.con=[];
    this.curBackground=null;
    this.sec=[];
    this.backgroundDom=$(this.root).children('.background-board')[0];
    this.backgroundCtx=this.backgroundDom.getContext('2d');
    this.lastTop=this.topY();
    this.lastBot=this.botY();
    this.globalWidth=window.screen.availWidth;
    this.globalHeight=window.screen.availHeight-this.navOff;
    this.down=true;
    this.init();
    window.onscroll=mainLoop;
    //Plug-in setting
    $('.least-gallery').least({'scrollToGallery': false});
};

IndexBoard.prototype.scrPos=function(){
    var pos;
    try{
        pos=window.pageYOffset;
    }
    catch(e){
        pos=(document.documentElement && document.documentElement.scrollTop) ||
            document.body.scrollTop;
    }
    return pos;
};

IndexBoard.prototype.topY=function(){
    return this.scrPos()+this.navOff;
};

IndexBoard.prototype.botY=function(){
    return this.scrPos()+$(window).height();
};

IndexBoard.prototype.init=function(){
    this.setSize();
    this.getCon();
    this.initCon();
    mainLoop();
};

IndexBoard.prototype.getCon= function () {
    var cur=this;
    $(this.root).children('section').each(function(){
        cur.con.push(new section(this,cur));
    })
};

IndexBoard.prototype.setSize=function(){
    $(this.root).css({
        'width':window.screen.availWidth,
        'margin-top':this.navOff
    });
    $(this.root).children('.background-board').css({
        'width':window.screen.availWidth,
        'height':window.screen.availHeight
    }).attr({
        width:window.screen.availWidth,
        height:window.screen.availHeight
    })
};

IndexBoard.prototype.getSec=function(top,bot) {
    var rtVal = [];
    for (var i = 0; i < this.con.length; i++) {
        if (this.con[i].top <= top && this.con[i].bot > top) {
            while(true){
                rtVal.push(i);
                i++;
                if(i>=this.con.length||this.con[i].top>=bot) return(rtVal);
            }
        }
    }
};

IndexBoard.prototype.setBackground=function(){
    if(this.curBackground==null || this.sec[0]>this.curBackground || this.sec[this.sec.length-1]<this.curBackground)
    {
        var img;
        var ctx=this.backgroundCtx;
        var background=null;

        for(var i=this.sec[0]; i<=this.sec[this.sec.length-1]; i++){
            if(this.con[i].backgroundImg) {
                if(!this.con[i].backgroundImg.complete)
                {
                    setTimeout(function(){list.setBackground()},200);
                    return;
                }
                background = i;
                img=this.con[i].backgroundImg;
                break;
            }
        }
        this.curBackground=background;
        if(background==null)
        {
            var guess=this.down?this.sec[this.sec.length-1]+1:this.sec[0]-1;
            if(guess>=0 && guess<this.con.length) img=this.con[guess].backgroundImg;
            background=img?guess:null;
            this.curBackground=background;
            if(background==null) return;
        }
        ctx.drawImage(img,0,0,this.backgroundDom.width,this.backgroundDom.height);
    }
};


IndexBoard.prototype.traverse=function(f){
    for(var i=0; i<this.con.length; i++)
    {
        for(var j=0; j<this.con[i].con.length; j++)
        {
            f.apply(this.con[i].con[j]);
        }
    }
};

IndexBoard.prototype.initCon=function(){
    this.traverse(function(){
        this.init();
    })
};

IndexBoard.prototype.edit=function(){
    this.traverse(function(){
        this.display();
    })
};

IndexBoard.prototype.inArea=function(top,bot){
    if(top<=this.lastTop && bot>this.lastTop) return true;
    if(bot>=this.lastBot && top>this.lastBot) return true;
    if(top>=this.lastTop && bot<=this.lastBot) return true;
    return false;

    //Need fix
};

IndexBoard.prototype.reInit=function(){
    for(var i=0; i<this.con.length; i++){
        this.con[i].reInit();
    }
};

//Section

var section=function(dom,parent){
    this.dom=dom;
    this.parent=parent;
    this.canDom=$(this.dom).children('.section-board')[0];

    this.setSize();
    this.top=this.dom.offsetTop;
    this.bot=this.dom.offsetHeight+this.dom.offsetTop;

    this.backgroundImg=this.getBackground();
    this.setCanColor();

    this.con=[];
    this.getCon();
};

section.prototype={
    setCanColor:function(){
        var cur=this.canDom;
        cur.width=cur.parentNode.offsetWidth;
        cur.height=cur.parentNode.offsetHeight;
        $(cur).css({'width':cur.width,'height':cur.height});
        var color=$(cur).attr('color');
        var opacity=$(cur).attr('opacity');
        var ctx=cur.getContext('2d');
        ctx.globalAlpha=opacity;
        ctx.fillStyle=color;
        ctx.fillRect(0,0,cur.width,cur.height);
    },

    getBackground:function(){
        var backStr=$(this.dom).attr('background');
        if(!backStr)
        {
            return null;
        }
        var img=document.createElement('img');
        $(img).attr('src',backStr);
        return img;
    },

    getCalPos:function(co){
        var rtVal={};
        rtVal.left=co.left*this.parent.globalWidth;
        rtVal.right=co.right*this.parent.globalWidth;
        rtVal.top=this.top+co.top*(this.bot-this.top);
        rtVal.bot=this.top+co.bot*(this.bot-this.top);
        return rtVal;
    },

    getCon:function(){
        var cur=this;
        $(this.dom).children('div').each(function(){
           cur.con.push(new div(this,cur));
        })
    },
    setSize:function(){
        var height=$(this.dom).attr('height');
        $(this.dom).css('height',height*this.parent.globalHeight-this.parent.navOff);
    },
    divControl:function(){
        for(var i=0; i<this.con.length; i++){
            if(this.parent.inArea(this.con[i].absPos.top,this.con[i].absPos.bot)){
                for(var j=0; j<this.con[i].animation.length; j++){
                    if(this.con[i].animation[j].shouldPlay()) this.con[i].animation[j].con.play();
                }
                this.con[i].first=false;
            }
        }
    },
    reInit:function(){
        for(var i=0; i<this.con.length; i++){
            this.con[i].reInit();
        }
    }
};

//Div

var div=function(dom,parent){
    var cur=this;
    this.dom=dom;
    this.parent=parent;
    this.type=$(this.dom).attr('type');
    this.absPos=this.parent.getCalPos({
        left:$(this.dom).attr('left'),
        right:$(this.dom).attr('right'),
        top:$(this.dom).attr('top'),
        bot:$(this.dom).attr('bot')
    });
    this.height=this.absPos.bot-this.absPos.top;
    this.width=this.absPos.right-this.absPos.left;
    this.layer=$(this.dom).attr('layer');

    this.animation=[];
    $(this.dom).children('.animation').each(function(){
        cur.animation.push(new animation(this,cur));
    });
    this.first=true;
};

div.prototype={
    display:function(){
        var cur=this;
        this.setPos();
        cur.autoFit();
    },
    autoFit:function(){
        if(existAutoFit[this.type]) existAutoFit[this.type](this);
        else
            $(this.dom).children('img,video,iframe').first().css({
            'height':this.height,
            'width':this.width
        });
    },
    setPos:function(left,top,width,height,layer){
        if(!left || !top || !width || !height || !layer)
        {
            left=this.absPos.left;
            top=this.absPos.top;
            width=this.width;
            height=this.height;
            layer=this.layer;
        }
        $(this.dom).css({
            'left':left.toString()+'px',
            'width':width.toString()+'px',
            'top':top.toString()+'px',
            'height':height.toString+'px',
            'z-index':layer
        });
    },
    init:function(){
        var cur=this;
        this.display();
        for(var i=0; i<this.animation.length; i++)
        {
            this.animation[i].con.init();
        }
    },
    reInit:function(){
        this.first=true;
        this.display();
        for(var i=0; i<this.animation.length; i++)
        {
            this.animation[i].con.init();
        }
    },
    reHandleAnimation:function(){
        var cur=this;
        this.animation=[];
        $(this.dom).children('.animation').each(function(){
            cur.animation.push(new animation(this,cur));
        });
    },
    reHandlePos:function(){
        this.absPos=this.parent.getCalPos({
            left:$(this.dom).attr('left'),
            right:$(this.dom).attr('right'),
            top:$(this.dom).attr('top'),
            bot:$(this.dom).attr('bot')
        });
        this.height=this.absPos.bot-this.absPos.top;
        this.width=this.absPos.right-this.absPos.left;
        this.layer=$(this.dom).attr('layer');
        this.display();
    },
    reNew:function(){
        var cur=this;
        this.type=$(this.dom).attr('type');
        this.reHandlePos();
        this.animation=[];
        $(this.dom).children('.animation').each(function(){
            cur.animation.push(new animation(this,cur));
        });
        this.first=true;
    },
    removeAnimation:function(aniObj){
        var find=-1;
        for(var i=0; i<this.animation.length; i++) {
            if (this.animation[i] === aniObj) {
                find = i;
                break;
            }
        }
        if(find<0) return false;
        for(i=find+1; i<this.animation.length; i++){
            this.animation[i-1]=this.animation[i];
        }
        this.animation.pop();
        return true;
    }
};

//animations
var aniCollections={};
var noInit=function(){
    alert("No initial function defined!");
};
var noPlay=function(){
    alert("No play function defined!");
};
var baseAnimation=function(targetDiv,parent,type){
    this.parent=parent;
    this.targetDiv=targetDiv;
    this.init=aniCollections[type].init;
    this.play=aniCollections[type].play;
};

aniCollections.fade={
    init:function(){
        $(this.targetDiv.dom).css('display','none');
    },
    play:function(){
        this.init(this.targetDiv.dom);
        $(this.targetDiv.dom).fadeIn(3000);
    }
};
var animation=function(dom,parent){
    this.dom=dom;
    this.parent=parent;
    this.type=$(this.dom).attr('type');
    this.trigger=$(this.dom).attr('trigger');
    this.con=new baseAnimation(this.parent,this,this.type);
};
animation.prototype={
    shouldPlay:function(){
        return(
            (this.parent.first && this.trigger=='first')
            );
    },
    reNew:function(){
        if(!this.dom){
            this.removeThis();
        }
        this.type=$(this.dom).attr('type');
        this.trigger=$(this.dom).attr('trigger');
        this.con=new baseAnimation(this.parent,this,this.type);
    },
    removeThis:function(){
        this.parent.removeAnimation(this);
    }
};
//tools
var secComp=function(sec1,sec2){
    if(sec1.length!=sec2.length) return false;
    for(var i=0; i<sec1.length; i++) if(sec1[i]!=sec2[i]) return false;
    return true;
};

//autoFit function

var existAutoFit={
    bootstrapCarousel:function(div){
        $(div.dom).find('.carousel-inner img').css({
            'width':div.width,
            'height':div.height
        });
    }
};

//main loop
var mainLoop=function(){
    var top=list.topY();
    var bot=list.botY();
    //if (list.lastTop-top<15 && list.lastTop-top>-15 && list.lastBot-bot<15 && list.lastBot-bot>-15) return;
    list.down=(list.lastTop<top);
    list.lastBot=bot;
    list.lastTop=top;
    var curSec=list.getSec(top,bot);
    if(!secComp(curSec,list.sec))
    {
        list.sec=curSec;
        list.setBackground();
    }
    for(var i=curSec[0]; i<=curSec[curSec.length-1]; i++)
    list.con[i].divControl();
};