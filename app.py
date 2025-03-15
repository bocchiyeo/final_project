from quart import Quart, request, render_template
from mercapi import Mercapi
from amiami_scraper import scrape_amiami, scrape_amiami_featured
from asyncio import to_thread

m = Mercapi()

app = Quart(__name__)

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/search')
async def search():
    s = request.args.get("q")
    if s:
        mercari = await m.search(s)
        mresult = mercari.items
        # rename the mercapi results to match amiami scraper result names
        for item in mresult:
            item_dict = item.__dict__
            item_dict['productName'] = item_dict.pop('name', None)
            item_dict['productPrice'] = item_dict.pop('price', None)
            item_dict['productImg'] = item_dict.pop('thumbnails', [None])[0]
            item_dict['productLink'] = "https://jp.mercari.com/item/" + item_dict.pop('id_', "")
            item_dict['source'] = "Mercari"

        aresult = await to_thread(scrape_amiami, s, 1)
        results = []
        results.extend(aresult)
        results.extend(mresult)
        return await render_template("search.html", results=results, s=s)
    return await render_template("search.html")

@app.route('/figures')
async def figures():
    item = "Figures"
    results = await to_thread(scrape_amiami_featured, "bishoujo")
    return await render_template("featured.html", results=results, item=item)

@app.route("/plushies")
async def plushies():
    item = "Plushies"
    results = await to_thread(scrape_amiami_featured, "plush")
    return await render_template("featured.html", item=item, results=results)

@app.route("/posters")
async def posters():
    item = "Posters"
    results = await to_thread(scrape_amiami, "posters", 2)
    return await render_template("featured.html", item=item, results=results)

if __name__ == "__main__":
    app.run(debug=True)