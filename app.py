import math
from flask import Flask, request, render_template
from sqlalchemy import create_engine, MetaData, Table

engine = create_engine('sqlite:///app/data.sqlite', convert_unicode=True)
metadata = MetaData(bind=engine)

posts = Table('posts', metadata, autoload=True)

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/blog')
def blog():
	limit = 10
	result = engine.execute(f'SELECT * FROM posts ORDER BY id DESC LIMIT {limit}')
	count = engine.execute('SELECT COUNT(*) FROM posts').first()
	count = math.ceil(count[0]/limit)
	return render_template('blog.html', result=result, count=count)

@app.route('/blog/page/<page>')
def page(page):
	if page.isdecimal() == True:
		limit = 10
		if int(page) == 1:
			offset = 0
		elif int(page) == 2:
			offset = limit
		else:
			offset = (int(page)*limit)-limit

		count = engine.execute('SELECT COUNT(*) FROM posts').first()
		count = math.ceil(count[0]/limit)
		result = engine.execute(f'SELECT * FROM posts ORDER BY id DESC LIMIT {limit} OFFSET {offset}')
		fetch = result.fetchall()
		if not fetch:
			return render_template('404.html')
		else:
			return render_template('blog.html', result=fetch, page=page, count=count)
	else:
		return render_template('404.html')

@app.route('/blog/<slug>')
def single(slug):
	result = posts.select(posts.c.slug  == slug).execute().first()
	if not result:
		return render_template('404.html')
	else:
		return render_template('single.html', slug=slug, result=result)

@app.route('/blog/search/<search>')
def search(search):
	result = engine.execute(f'SELECT * FROM posts WHERE title LIKE "%{search.lower()}%" ORDER BY id DESC')
	return render_template('search.html', result=result, search=search)

@app.errorhandler(404)
def notfoud(e):
	return render_template('404.html'), 404

if __name__=='__main__':
	app.run()