import base64
import os
import qrcode
from io import BytesIO

async def solve_message(mes):
	return "hello"

async def encode_base64(txt):
	txt = base64.b64encode(txt)
	return txt.decode("utf-8")

async def decode_base64(txt):
	txt = base64.b64decode(txt)
	return txt.decode("utf-8")


class NoMCSV(Exception):
	def __init__(self,sl:list):
		_str = ""
		for z in sl:
			_str += f"{z},"
		super().__init__(f"Không thể tìm thấy MCSV,các server hiện có: {_str}")

async def make_qrcode(text):
	qr = qrcode.make(text).convert("RGBA")
	buffer = BytesIO()
	qr.save(buffer,format="png")
	buffer.seek(0)
	img = base64.b64encode(buffer.getvalue())
	img=str(img).replace(" ","")
	return img
