import quart
import os
import func
import logging
import asyncio
import werkzeug
from quart import request,render_template,redirect,send_from_directory,url_for,abort

app = quart.Quart(__name__,static_folder="./static",template_folder="templates",static_url_path="/src/static/")

app.config["SECRET_KEY"] = os.getenv("sk")
logger = app.logger
hdlr = logging.FileHandler("quart.log")
logger.addHandler(hdlr)
logger.info("Init")

@app.route("/")
async def home():
	return await render_template("home.html")

@app.route("/about")
@app.route("/about/")
async def about():
	# return await render_template("about.html")
	return 'Unavailable'

@app.route("/beta/qrcode",methods=["GET","POST"])
async def qrtest():
	if request.method.lower() == "post":
		text = (await request.form)["text"]
		i = await func.make_qrcode(text)
		return await render_template("qrcode.html",qrcode=i),200
	return await render_template("qrcode.html"),200

@app.get("/mcserver")
@app.get("/mcserver/")
async def mc_server():
	return await render_template("introduce_mcserver.html")


@app.route("/beta/base64/")
@app.route("/beta/base64")
async def base64_en_decode():
	return await render_template("base64.html")

@app.errorhandler(werkzeug.exceptions.NotFound)
async def _404(e):
	return await render_template("404.html",e=e)

@app.route("/chs")
@app.route("/chs/")
async def chs():
	g = func.get_games()
	return await render_template("chs.html",games=g)

@app.route("/chs/flappy")
@app.route("/chs/flappy/")
async def flappy():
	return await render_template("chs/flappy.html")
	
@app.route("/chs/snake/pc")
@app.route("/chs/snake/pc/")
async def snake_pc():
	return await render_template("chs/snakepc.html")

@app.route("/chs/snake/mobile")
@app.route("/chs/snake/mobile/")
async def snake_mobile():
	return await render_template("chs/snakemb.html")

@app.route("/chs/snake")
@app.route("/chs/snake/")
async def snake_home():
	return await render_template("chs/snakehome.html")

@app.route("/seepagesource/code/<string:s>")
async def sps_c(s):

	if s == "usedbytinvn":
		return """javascript:(function()%7Bvar%20a=window.open('about:blank').document;a.write('%3C!DOCTYPE%20html%3E%3Chtml%3E%3Chead%3E%3Ctitle%3ESource%20of%20'+location.href+'%3C/title%3E%3Cmeta%20name=%22viewport%22%20content=%22width=device-width%22%20/%3E%3C/head%3E%3Cbody%3E%3C/body%3E%3C/html%3E');a.close();var%20b=a.body.appendChild(a.createElement('pre'));b.style.overflow='auto';b.style.whiteSpace='pre-wrap';b.appendChild(a.createTextNode(document.documentElement.innerHTML))%7D)();<br><br><button onclick="navigator.clipboard.writeText('javascript:(function()%7Bvar%20a=window.open('about:blank').document;a.write('%3C!DOCTYPE%20html%3E%3Chtml%3E%3Chead%3E%3Ctitle%3ESource%20of%20'+location.href+'%3C/title%3E%3Cmeta%20name=%22viewport%22%20content=%22width=device-width%22%20/%3E%3C/head%3E%3Cbody%3E%3C/body%3E%3C/html%3E');a.close();var%20b=a.body.appendChild(a.createElement('pre'));b.style.overflow='auto';b.style.whiteSpace='pre-wrap';b.appendChild(a.createTextNode(document.documentElement.innerHTML))%7D)();')">Copy</button>
	"""
	else:
		return redirect(url_for("home"))

@app.route("/cppr")
@app.route("/cppr/")
async def cppr_sv():
	return '<iframe src="https://discord.com/widget?id=1013029731479855224&theme=dark" width="350" height="500" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>'

@app.route("/code.py")
async def cp():
	return """import os
os.system("pip install pypresence")

from pypresence import Presence
from itertools import cycle
import time

rpc = Presence(1075013570414247997)
rpc.connnect()
rpc.update(
	state=str(cycle("Chào,tôi là TinVN :flag_vn:","Hi,I'm TinVN :flag_vn:","Chào mừng đến trang cá nhân của tôi :)","Welcome to my profile :)","404 errorrrrr...","nhìn gì","random text")),
	details=str(cycle("nothing","???")),
	large_image="studying",
	large_text=cycle("Tôi là học sinh :books:","I'm a student :books:"),
	small_image="coding",
	small_text="I love coding and playing games"	
)

while True:
	time.sleep(60)
 
 """

@app.route("/blog/<id>")
async def blog(id):
	id = str(id)
	try:
		return await render_template(f"./blog/{id}.html")
	except:
		abort(404)

def get_domain():
	return request.url.rpartition("//")[-1].partition("/")[0]

@app.before_request
async def br():
	app.add_template_global(get_domain(),"domain")

@app.route("/chs/ztdata/<id>")
async def ztypedata(id):
	id = str(id)
	return await render_template(f"/chs/ztype-data/{id}.html")


if __name__ == "__main__":

	loop = asyncio.get_event_loop()
	loop.run_until_complete(app.run_task(host="0.0.0.0",port=8080,debug=True))
	logger.info("running?")

#reloader=False