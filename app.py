from quart import Quart, request, render_template
from mercapi import Mercapi

m = Mercapi()

app = Quart(__name__)

@app.route('/')
async def index():
    s = request.args.get("q")
    if s:
        result = await m.search(s)
        if result.items:
            first_item = result.items[0]
            print(f"Type of first item: {type(first_item)}")
            print(f"Attributes and methods of first item: {dir(first_item)}")
            print(f"First item data: {first_item.__dict__}")
        return await render_template("search.html", result=result)
    return await render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)