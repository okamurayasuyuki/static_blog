#coding: utf-8
import os
from flask import Flask,render_template,redirect,url_for
from flask_flatpages import FlatPages,pygments_style_defs
from flask import g
import feedformatter,time
import feedgenerator
import datetime




DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = ".md"

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)

def title(title = None):
	if title is None:
		return 'none'
	return title

@app.route("/sitemap")
def sitemap():
    return render_template("sitemap.xml",pages=pages)



@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/rss")
def rss():
    feed = feedgenerator.Rss201rev2Feed(
            title = u"Pickalize",
            link = u"http://pickalize.info",
            feed_url = u"http://pickalize.info/rss",
            description = u"",
            author_name = u"pickalize",
            pubdate = datetime.datetime.utcnow()
            )
    for e in sorted(pages,reverse = True,key = lambda p: p.meta["date"]):
        feed.add_item(
                title = u'%s' % e.meta['title'],
                link = u'http://pickalize.info/' + e.path,
                description =  e.body.encode('utf-8'),
                pubdate = e.meta['date']
                )

    return feed.writeString('utf-8')
@app.route("/tags/<name>")
def tags(name):
    tag_page = [page for page in pages if page.meta.get("tags") is not None]
    res = []
    for page in tag_page:
        if name in page.meta.get("tags").split(","):
            res.append(page)


    sorted_pages = sorted(res,reverse=True,
    key = lambda p: p.meta["date"] )
    return render_template("all.html",pages=sorted_pages)


@app.route("/archive")
def archive():

    sorted_pages = sorted(pages,reverse=True,

    key = lambda p: p.meta["date"] )
    return render_template("all.html",pages=sorted_pages)


app.jinja_env.globals['title'] = title


def set_keywords(keywords):
    app.jinja_env.globals["keywords"]= keywords

def set_desc(body):
    app.jinja_env.globals["desc"] = body


@app.route("/")
def index():
    sorted_pages = sorted(pages,reverse=True, key = lambda p: p.meta["date"] )

    set_keywords("python,flask,heroku")
    set_desc(u"お気楽Pythonプログラミング")
    return render_template("hello.html",pages=sorted_pages[0:20],page = None)


def relative_pages(tag_name):
    import random
    res = []
    tag_name = tag_name or "python"

    sorted_pages = sorted(pages,reverse=True,
                          key = lambda x: x.meta["date"])
    for page in sorted_pages:
        tags = page.meta.get("tags","").split(",")
        if tag_name in tags:
            res.append(page)
    max_lim = len(res)
    #最大10件までの関連するブログ記事を表示
    max_lim = 10 if max_lim > 10 else max_lim
    #自分のブログ記事を排除してその後、配列をシャッフルする
    res = res[1:]
    random.shuffle(res)
    #最初の記事は自分自身の記事なので表示しない

    return res[1:max_lim]

@app.route("/<path:path>/detail/")
def d(path):
    page = pages.get_or_404(path)
    title = u"%s" % page.meta["title"]
    app.jinja_env.globals['title'] = title
    l = len(page.body.encode("utf-8").replace("\n","").decode("utf-8"))

    page.meta["path"] = path
    tag = (page.meta.get("tags") or "").split(",")[0]
    print(page)
    set_desc(page.body)
    set_keywords(str(page.meta.get("tags")) or "")


    return render_template('page.html', page=page,
                           title=title,
                           length = l,
                           relative_pages = relative_pages(tag))









@app.route("/apps")
def apps():
    return render_template("apps.html")

@app.route("/product")
def product():
    return render_template("product.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

# show other scripts
@app.route("/scripts")
def scripts():
    return render_template("scripts.html")

@app.route("/works")
def works():
    return render_template("works.html")


