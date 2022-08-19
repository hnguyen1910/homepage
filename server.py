import quart
import os
import func
import logging
import asyncio
from quart import request,render_template,redirect,send_from_directory

app = quart.Quart(__name__,static_folder="static",template_folder="templates",static_url_path="/root/static/")

app.config["SECRET_KEY"] = os.getenv("sk")
logger = app.logger
hdlr = logging.FileHandler("quart.log")
logger.addHandler(hdlr)
logger.info("Init")

@app.route("/")
async def home():
	return await render_template("home.html")

@app.route("/status/")
@app.route("/status")
async def status():
	return redirect("https://stats.uptimerobot.com/MXpNlh2gWR")

@app.route("/test-qrcode",methods=["GET","POST"])
async def qrtest():
	if str(request.method) == str("POST"):
		text = (await request.form)["text"]
		i = await func.make_qrcode(text)
		print(type(i))
		return await render_template("qrcode.html",qrcode=i),200
	return await render_template("qrcode.html"),200

@app.get("/mcserver")
@app.get("/mcserver/")
async def mc_server():
	return await render_template("introduce_mcserver.html")


@app.get("/mcserver/Tyel_Vietnamese_v1.5.9.zip")
async def send_packs():
	return await send_from_directory("static/files/","Tyel_Vietnamese_v1.5.9.zip")

@app.route("/beta/base64/")
@app.route("/beta/base64")
async def base64_en_decode():
	return await render_template("base64.html")

@app.errorhandler(404)
async def _404(e):
	return await render_template("404.html")


		
if __name__ == "__main__":

	loop = asyncio.get_event_loop()
	loop.run_until_complete(app.run_task(host="0.0.0.0",port=8080,debug=True))
	logger.info("running?")

#reloader=False