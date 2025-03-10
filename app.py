from quart import Quart, request, render_template
from mercapi import Mercapi

m = Mercapi()

app = Quart(__name__)

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/search')
async def search():
    s = request.args.get("q")
    if s:
        result = await m.search(s)
        return await render_template("search.html", result=result)
    return await render_template("search.html")

if __name__ == "__main__":
    app.run(debug=True)