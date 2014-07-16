__author__ = 'tang'


import pymongo
from app.model import Section, Page

def fill_selection():
    t = Section()
    content = []
    content.append('''
    <section id="1" height="1" background="static/resource/img/big/1.jpg">
        <canvas class="section-board" color="black" opacity=0.7>
        </canvas>
        <div left="0.5" top="0.4" right="0.8" bot="0.5" style="text-align: center">
            <p>Of course</p>
        </div>
        <div left="0.4" right="0.6" top="0.2" bot="0.8">
            <img src="static/resource/icon/reic.png">
            <span class="animation" type="fade" trigger="first"> </span>
        </div>
    </section>
    ''')
    content.append('''
    <section id="2" height="1.5" background="">
        <canvas class="section-board" color="white" opacity=0.5>
        </canvas>
        <div left="0.4" right="0.6" top="0.1" bot="0.2" style="text-align: center">
            <h2>Title</h2>
        </div>
        <div left='0.1' top='0.1' right='0.3' bot='0.3' style="text-align: center" type="bootstrapPanel">
            <div class="panel panel-default" style="border-color: rgba(0,0,0,1)">
                <div class="panel-heading" style="background-color: rgba(121,230,131,0.5);border-color: black">This is a panel</div>
                <div class="panel-body" style="background-color: rgba(255,255,255,0.2)">
                    Panel content
                </div>
            </div>
        </div>
        <div left="0.4" right="0.8" top="0.1" bot="0.5" type="bootstrapJumbotron">
            <div class="jumbotron" style="background-color: white">
                <h1>Hello, world!</h1>
                <p>This is jumbotron</p>
                <p><a class="btn btn-primary btn-lg" role="button">Learn more</a></p>
            </div>
        </div>
        <div left="0.1" top="0.4" right="0.3" bot="0.5">
            <button type="button" class="btn btn-default">Button</button>
        </div>
    </section>
    ''')
    content.append('''
    <section id="3" height="1" background="static/resource/img/big/3.jpg">
        <canvas class="section-board" color="black" opacity=0.7>
        </canvas>
        <div left="0.0" right="1" top="0" bot="1" style="text-align: center" type="bootstrapCarousel">
                <div class="carousel slide" id="carousel-example-captions" data-ride="carousel">
                    <ol class="carousel-indicators">
                        <li data-target="#carousel-example-captions" data-slide-to="0"></li>
                        <li data-target="#carousel-example-captions" data-slide-to="1"></li>
                        <li class="active" data-target="#carousel-example-captions" data-slide-to="2"></li>
                    </ol>
                    <div class="carousel-inner">
                        <div class="item">
                            <img alt="900x500" src="static/resource/img/big/3.jpg">
                            <div class="carousel-caption">
                                <h3>First slide label</h3>
                                <p>Nulla vitae elit libero, a pharetra augue mollis interdum.</p>
                            </div>
                        </div>
                        <div class="item">
                            <img alt="900x500" src="static/resource/img/big/2.jpg">
                            <div class="carousel-caption">
                                <h3>Second slide label</h3>
                                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                            </div>
                        </div>
                        <div class="item active">
                            <img alt="900x500" src="static/resource/img/big/1.jpg">
                            <div class="carousel-caption">
                                <h3>Third slide label</h3>
                                <p>Praesent commodo cursus magna, vel scelerisque nisl consectetur.</p>
                            </div>
                        </div>
                    </div>
                    <a class="left carousel-control" href="#carousel-example-captions" data-slide="prev">
                        <i class="fa fa-angle-left icon-prev"></i>
                    </a>
                    <a class="right carousel-control" href="#carousel-example-captions" data-slide="next">
                        <i class="fa fa-angle-right icon-next"></i>
                    </a>
                </div>
        </div>
    </section>
    ''')

    content.append('''
    <section id="4" height="1" background="">
        <canvas class="section-board" color="black" opacity=1>
        </canvas>
        <div left="0.1" top="0.05" right="0.9" bot="1">
            <!--test -->
            <!-- Least Gallery -->
            <section id="least">

                <!-- Least Gallery: Fullscreen Preview -->
                <div class="least-preview"></div>

                <!-- Least Gallery: Thumbnails -->
                <ul class="least-gallery">
                    <!-- 1 -->
                    <li>
                        <a href="static/resource/img/big/01.jpg" title="Skateboard" data-caption="<strong>Lorem ipsum dolor</strong> sit amet, consetetur sadipscing" >
                            <img src="static/resource/img/thumbnails/01.jpg" alt="Alt Image Text" />
                        </a>
                    </li>

                    <!-- 2 -->
                    <li>
                        <a href="static/resource/img/big/02.jpg" title="Train Rails">
                            <img src="static/resource/img/thumbnails/02.jpg" alt="Alt Image Text" />
                        </a>
                    </li>

                    <!-- 3 -->
                    <li>
                        <a href="static/resource/img/big/03.jpg" title="Apple">
                            <img src="static/resource/img/thumbnails/03.jpg" alt="Alt Image Text" />
                        </a>
                    </li>

                    <!-- 4 -->
                    <li>
                        <a href="static/resource/img/big/04.jpg" title="Road Trip">
                            <img src="static/resource/img/thumbnails/04.jpg" alt="Alt Image Text" />
                        </a>
                    </li>

                    <!-- 5 -->
                    <li>
                        <a href="static/resource/img/big/05.jpg" title="Desert">
                            <img src="static/resource/img/thumbnails/05.jpg" alt="Alt Image Text" />
                        </a>
                    </li>

                    <!-- 6 -->
                    <li>
                        <a href="static/resource/img/big/06.jpg" title="Tree">
                            <img src="static/resource/img/thumbnails/06.jpg" alt="Alt Image Text" />
                        </a>
                    </li>

                    <!-- 7 -->
                    <li>
                        <a href="static/resource/img/big/07.jpg" title="MacBook">
                            <img src="static/resource/img/thumbnails/07.jpg" alt="Alt Image Text" />
                        </a>
                    </li>

                    <!-- 8 -->
                    <li>
                        <a href="static/resource/img/big/08.jpg" title="Clock">
                            <img src="static/resource/img/thumbnails/08.jpg" alt="Alt Image Text" />
                        </a>
                    </li>

                    <!-- 9 -->
                    <li>
                        <a href="static/resource/img/big/09.jpg" title="iPhone">
                            <img src="static/resource/img/thumbnails/09.jpg" alt="Alt Image Text" />
                        </a>
                    </li>

                    <!-- 10 -->
                    <li>
                        <a href="static/resource/img/big/10.jpg" title="Test">
                            <img src="static/resource/img/thumbnails/10.jpg" alt="Alt Image Text" />
                        </a>
                    </li>
                </ul>
            </section>
            <!-- Least Gallery end -->
        </div>
    </section>
    ''')

    for s in content:
        t.insert(content=s)

def fill_demo_page():
    p=Page()
    s=Section()
    docs=s.get_all()
    section=[]
    for doc in docs:
        section.append(doc['_id'])
    p.insert(section=section)

