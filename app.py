import streamlit as st
import json
import os
import io
import time
import random
import requests
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from pathlib import Path


STYLES = '''
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;600;800&display=swap" rel="stylesheet">
<style>
.header { padding: 6px 0 12px 0; }
.card { background: #ffffff; border-radius: 12px; padding: 8px; box-shadow: 0 6px 18px rgba(15,23,42,0.08); margin-bottom: 14px; }
.badge { display:inline-block; background:#eef2ff; color:#1f2937; padding:4px 8px; border-radius:999px; margin-right:6px; font-size:12px; }
.stButton>button { border-radius: 8px; }
.header h1 { font-family: 'Segoe UI', Roboto, sans-serif; }
.header p { color: #374151 }
img { border-radius: 8px; }
.gallery { display:flex; flex-wrap:wrap; gap:12px; }
.gallery .item { width:240px; border-radius:10px; overflow:hidden; box-shadow:0 6px 18px rgba(15,23,42,0.08); }
.gallery .item img { width:100%; height:160px; object-fit:cover; }
.rubik { font-family: 'Rubik', sans-serif; }
</style>
'''

st.markdown(STYLES, unsafe_allow_html=True)

PLACES = [
	{
		"name": "Kawah Ijen Blue Fire",
		"country": "Indonesia",
		"desc": "A volcanic crater famous for electric-blue flames and sulfur miners.",
		"img": "assets/kawah_ijen.png",
		"remote_img": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80",
		"tags": ["volcano", "adventure"],
	},
	{
		"name": "Svaneti Villages",
		"country": "Georgia",
		"desc": "Remote mountain villages with medieval towers and alpine trails.",
		"img": "assets/svaneti.png",
		"remote_img": "https://images.unsplash.com/photo-1538688387541-1d8d1d0c8d66?auto=format&fit=crop&w=1200&q=80",
	},
	{
		"name": "Islas Cies",
		"country": "Spain",
		"desc": "Pristine beaches and crystal waters on a protected island archipelago.",
		"img": "assets/islas_cies.png",
		"remote_img": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80",
		"tags": ["beach", "relax"],
	},
	{
		"name": "Valle de Viñales",
		"country": "Cuba",
		"desc": "Limestone mogotes, tobacco farms, and colorful rural life.",
		"img": "assets/vinales.png",
		"remote_img": "https://images.unsplash.com/photo-1491553895911-0055eca6402d?auto=format&fit=crop&w=1200&q=80",
	},
	{
		"name": "Kyrgyz Lakes",
		"country": "Kyrgyzstan",
		"desc": "High-altitude alpine lakes with nomadic culture and wild pastures.",
		"img": "assets/kyrgyz_lakes.png",
		"remote_img": "https://images.unsplash.com/photo-1508610048659-a06c9f0d0d3f?auto=format&fit=crop&w=1200&q=80",
		"tags": ["lakes", "nature"],
	},
]


WISHLIST_FILE = "wishlist.json"


def load_wishlist():
	if os.path.exists(WISHLIST_FILE):
		try:
			with open(WISHLIST_FILE, "r", encoding="utf-8") as f:
				return json.load(f)
		except Exception:
			return []
	return []


def save_wishlist(data):
	try:
		with open(WISHLIST_FILE, "w", encoding="utf-8") as f:
			json.dump(data, f, ensure_ascii=False, indent=2)
	except Exception:
		pass


st.set_page_config(page_title="OffMap", layout="wide")


def render_header():
	# Decorative header with columns
	st.markdown(
		"<div class='header'><h1 style='margin:0'>🌍 OffMap — Travel Discovery</h1><p style='margin:4px 0 0 0'>Find hidden gems off the beaten path — curated escapes and local favorites. ✨</p></div>",
		unsafe_allow_html=True,
	)
	st.write("---")


	# small hero with two columns
	c1, c2 = st.columns([2, 3])
	with c1:
		st.image("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=60")
	with c2:
		st.markdown("### Handpicked offbeat spots")
		st.write("Curated destinations for curious travelers. Save favorites, send postcards, and discover more.")


def render_filter_sidebar():
	with st.sidebar.expander("Filters", expanded=True):
		# Authentication area
		if "auth_token" not in st.session_state:
			st.session_state.auth_token = None
		if "username" not in st.session_state:
			st.session_state.username = None

		if st.session_state.auth_token:
			st.markdown(f"**Signed in as {st.session_state.get('username')}**")
			if st.button("Logout"):
				st.session_state.auth_token = None
				st.session_state.username = None
		else:
			with st.expander("Sign in / Register"):
				mode = st.radio("Action", ["Login", "Register"], index=0)
				u = st.text_input("Username", key="auth_user")
				p = st.text_input("Password", type="password", key="auth_pass")
				if mode == "Register":
					if st.button("Create account"):
						ok = backend_register(u, p)
						if ok:
							st.success("Account created — you can now login")
						else:
							st.error("Could not create account")
				else:
					if st.button("Login"):
						res = backend_login(u, p)
						if res:
							st.success("Logged in")
							st.session_state.auth_token = res.get("access_token")
							st.session_state.username = u
						else:
							st.error("Login failed")

		countries = sorted({p["country"] for p in PLACES})
		countries.insert(0, "All")
		country = st.selectbox("Choose a country", countries)
		all_tags = sorted({t for p in PLACES for t in p.get("tags", [])})
		tags = st.multiselect("Tags", all_tags)
		storage = st.radio("Storage", ["Local", "Backend"], index=0)
		st.markdown("---")
		st.markdown("### 💖 Wishlist")
		# load wishlist from selected storage
		st.session_state.storage = storage
		if storage == "Backend":
			items = backend_get_wishlist()
			if items is None:
				st.write("Backend not reachable — using local wishlist.")
				if "wishlist" not in st.session_state:
					st.session_state.wishlist = load_wishlist()
			else:
				st.session_state.wishlist = items
		else:
			if "wishlist" not in st.session_state:
				st.session_state.wishlist = load_wishlist()

		if st.session_state.wishlist:
			for item in st.session_state.wishlist:
				st.write(f"- {item}")
			if st.button("Clear wishlist"):
				if storage == "Backend":
					ok = backend_clear_wishlist()
					if ok:
						st.session_state.wishlist = []
						st.success("Cleared wishlist on server")
					else:
						st.error("Could not clear wishlist on server")
				else:
					st.session_state.wishlist = []
					save_wishlist([])
					st.experimental_rerun()
		else:
			st.write("No saved items yet.")

		return country, tags, storage


def add_to_wishlist(name):
	mode = st.session_state.get("storage", "Local")
	if mode == "Backend":
		ok = backend_add_wishlist(name)
		if ok:
			st.session_state.wishlist = backend_get_wishlist() or st.session_state.get("wishlist", [])
		return
	# fallback local
	if "wishlist" not in st.session_state:
		st.session_state.wishlist = load_wishlist()
	if name not in st.session_state.wishlist:
		st.session_state.wishlist.append(name)
		save_wishlist(st.session_state.wishlist)


def remove_from_wishlist(name):
	mode = st.session_state.get("storage", "Local")
	if mode == "Backend":
		backend_remove_wishlist(name)
		st.session_state.wishlist = backend_get_wishlist() or []
		return
	if "wishlist" not in st.session_state:
		st.session_state.wishlist = load_wishlist()
	if name in st.session_state.wishlist:
		st.session_state.wishlist.remove(name)
		save_wishlist(st.session_state.wishlist)


BASE_API_URL = "http://localhost:8000"


def backend_get_wishlist():
	try:
		headers = backend_headers()
		resp = requests.get(f"{BASE_API_URL}/wishlist", headers=headers, timeout=3)
		resp.raise_for_status()
		return resp.json()
	except Exception:
		return None


def backend_add_wishlist(name):
	try:
		headers = backend_headers()
		resp = requests.post(f"{BASE_API_URL}/wishlist", json={"name": name}, headers=headers, timeout=3)
		return resp.status_code == 201
	except Exception:
		return False


def backend_register(username, password):
	try:
		resp = requests.post(f"{BASE_API_URL}/auth/register", json={"username": username, "password": password}, timeout=4)
		return resp.status_code == 200 or resp.status_code == 201
	except Exception:
		return False


def backend_login(username, password):
	try:
		resp = requests.post(f"{BASE_API_URL}/auth/login", json={"username": username, "password": password}, timeout=4)
		resp.raise_for_status()
		return resp.json()
	except Exception:
		return None


def backend_remove_wishlist(name):
	try:
		headers = backend_headers()
		resp = requests.delete(f"{BASE_API_URL}/wishlist/{name}", headers=headers, timeout=3)
		return resp.status_code == 200
	except Exception:
		return False


def backend_clear_wishlist():
	try:
		headers = backend_headers()
		resp = requests.delete(f"{BASE_API_URL}/wishlist/clear", headers=headers, timeout=3)
		return resp.status_code == 200
	except Exception:
		return False


def ensure_assets():
	assets_dir = Path("assets")
	assets_dir.mkdir(exist_ok=True)
	for p in PLACES:
		path = Path(p["img"])
		if not path.exists():
			# try download remote image first
			remote = p.get("remote_img")
			if remote:
				try:
					resp = requests.get(remote, timeout=8)
					resp.raise_for_status()
					with open(path, "wb") as f:
						f.write(resp.content)
					continue
				except Exception:
					pass
			# fallback: generate a simple placeholder image
			img = Image.new("RGB", (1200, 800), tuple([random.randint(80, 220) for _ in range(3)]))
			d = ImageDraw.Draw(img)
			try:
				fnt = ImageFont.truetype("arial.ttf", 48)
			except Exception:
				fnt = ImageFont.load_default()
			text = p["name"]
			bbox = d.textbbox((0, 0), text, font=fnt)
			w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
			d.text(((1200-w)/2, (800-h)/2), text, font=fnt, fill=(255,255,255))
			img.save(path)



def render_places(selected_country, tags_filter=None, search_query=None):
	if selected_country and selected_country != "All":
		visible = [p for p in PLACES if p["country"] == selected_country]
	else:
		visible = PLACES[:]

	# apply tags filter
	if tags_filter:
		visible = [p for p in visible if any(t in p.get("tags", []) for t in tags_filter)]

	# apply search
	if search_query:
		q = search_query.lower()
		visible = [p for p in visible if q in p["name"].lower() or q in p["desc"].lower()]

	st.markdown("### 🗺️ Hidden Places")
	st.markdown("Discover offbeat destinations — click expanders for more details.")

	for i in range(0, len(visible), 3):
		cols = st.columns(3)
		for col, place in zip(cols, visible[i:i+3]):
			with col:
				st.markdown(f"<div class='card'>", unsafe_allow_html=True)
				st.image(place.get("img"))
				st.markdown(f"#### {place['name']} — {place['country']}")
				st.write(place["desc"])
				# tags
				if place.get("tags"):
					tag_html = "".join([f"<span class='badge'>{t}</span>" for t in place["tags"]])
					st.markdown(tag_html, unsafe_allow_html=True)
				with st.expander("More info"):
					st.write("This spot is a local favorite. Add photos, travel tips, and how to get there.")
				save_key = f"save_{place['name']}"
				remove_key = f"remove_{place['name']}"
				if st.button("Save to wishlist", key=save_key):
					add_to_wishlist(place['name'])
					st.success(f"Saved {place['name']} to wishlist")
				if st.button("Remove from wishlist", key=remove_key):
					remove_from_wishlist(place['name'])
				st.markdown("</div>", unsafe_allow_html=True)


def fetch_image(url):
	try:
		if isinstance(url, str) and url.startswith("http"):
			resp = requests.get(url, timeout=6)
			resp.raise_for_status()
			return Image.open(io.BytesIO(resp.content)).convert("RGB")
		else:
			# local file
			return Image.open(url).convert("RGB")
	except Exception:
		return None


def make_postcard(image: Image.Image, title: str, message: str) -> bytes:
	# Create a postcard-like image (1200x800)
	W, H = 1200, 800
	canvas = Image.new("RGB", (W, H), (255, 255, 255))

	# Resize and paste the photo
	img_w = W
	img_h = int(H * 0.65)
	img = image.copy()
	img.thumbnail((img_w, img_h))
	x = (W - img.width) // 2
	canvas.paste(img, (x, 0))

	# Draw caption area
	draw = ImageDraw.Draw(canvas)
	caption_y = img_h + 20
	rect_h = H - caption_y - 40
	draw.rectangle([(40, caption_y), (W - 40, H - 40)], fill=(245, 245, 250))

	# Load a default font
	try:
		font_title = ImageFont.truetype("arial.ttf", 36)
		font_msg = ImageFont.truetype("arial.ttf", 24)
	except Exception:
		font_title = ImageFont.load_default()
		font_msg = ImageFont.load_default()

	# Title
	draw.text((60, caption_y + 10), title, fill=(20, 20, 40), font=font_title)

	# Message (wrap)
	lines = []
	words = message.split()
	line = ""
	for w in words:
		test = f"{line} {w}".strip()
		wsize = draw.textsize(test, font=font_msg)[0]
		if wsize > W - 140:
			lines.append(line)
			line = w
		else:
			line = test
	if line:
		lines.append(line)

	y = caption_y + 60
	for ln in lines:
		draw.text((60, y), ln, fill=(50, 50, 70), font=font_msg)
		y += 32

	# Save to bytes
	buf = io.BytesIO()
	canvas.save(buf, format="PNG")
	return buf.getvalue()


def mystery_postcard_widget():
	st.markdown("---")
	st.markdown("## 🎴 Mystery Postcard — Reveal & Share")
	st.markdown("Pick a mood or press **Surprise me** to reveal a mystery destination as a postcard.")

	moods = ["Relaxing", "Adventure", "Cultural", "Hidden Gem"]
	mood = st.selectbox("Mood", moods)
	if st.button("Surprise me"):
		chosen = random.choice(PLACES)
		st.session_state.chosen = chosen

	chosen = st.session_state.get("chosen", None)
	if chosen:
		place = chosen
		st.markdown(f"### {place['name']} — {place['country']}")

		if st.button("Reveal postcard"):
			with st.spinner("Revealing…"):
				img = fetch_image(place.get("img"))
				if img is None:
					st.error("Could not load image.")
					return
				# animated blur reveal
				for radius in [30, 20, 12, 6, 3, 0]:
					tmp = img.filter(ImageFilter.GaussianBlur(radius=radius))
					buf = io.BytesIO()
					tmp.save(buf, format="PNG")
					st.image(buf.getvalue())
					time.sleep(0.25)

				st.balloons()

				# message and postcard generation
				msg = st.text_area("Write a short postcard message", value=f"Greetings from {place['name']}!")
				if st.button("Generate postcard"):
					data = make_postcard(img, place['name'], msg)
					st.success("Postcard ready — download and share!")
					st.download_button("Download postcard", data=data, file_name=f"postcard_{place['name'].replace(' ', '_')}.png", mime="image/png")
					# upload option if backend selected
					if st.session_state.get("storage", "Local") == "Backend":
						if st.button("Upload postcard to OffMap"):
							resp = backend_upload_postcard(data, f"postcard_{place['name'].replace(' ', '_')}.png", place['name'])
							if resp is not None:
								st.success("Uploaded — URL: " + resp.get("url", ""))
							else:
								st.error("Upload failed — is the API running?")


	def backend_upload_postcard(data_bytes: bytes, filename: str, title: str):
		try:
			headers = backend_headers()
			files = {"file": (filename, data_bytes, "image/png")}
			resp = requests.post(f"{BASE_API_URL}/postcards", files=files, data={"title": title}, headers=headers, timeout=6)
			resp.raise_for_status()
			return resp.json()
		except Exception:
			return None


	def backend_headers():
		headers = {}
		token = st.session_state.get("auth_token")
		if token:
			headers["Authorization"] = f"Bearer {token}"
		return headers



def render_suggestions():
	with st.expander("💡 Upgrade ideas for OffMap — MVP features", expanded=False):
		st.markdown(
			"- Personal wishlist (save favorites)\n- User-contributed tips & photos\n- Simple map view (embed static map)\n- Country filters and tags\n- Lightweight backend to persist wishlists"
		)


def render_uploaded_postcards():
	if st.session_state.get("storage", "Local") != "Backend":
		return
	try:
		resp = requests.get(f"{BASE_API_URL}/postcards", timeout=3)
		resp.raise_for_status()
		items = resp.json()
	except Exception:
		st.write("Could not fetch uploaded postcards.")
		return

	if not items:
		st.write("No uploaded postcards yet.")
		return

	st.markdown("### 📮 Uploaded Postcards")
	cols = st.columns(3)
	for i, item in enumerate(items):
		col = cols[i % 3]
		with col:
			url = f"{BASE_API_URL}{item['url']}" if item.get('url') else f"{BASE_API_URL}/postcards/{item['filename']}"
			st.image(url)
			st.markdown(item.get('filename', ''))


def main():
	ensure_assets()
	render_header()
	selected, tags, storage = render_filter_sidebar()
	search = st.text_input("Search places", value="")

	left, right = st.columns([3, 1])
	with left:
		render_places(selected, tags_filter=tags, search_query=search)
	with right:
		st.markdown("### ✨ Featured")
		st.info("Fresh picks every week — follow for updates!")
		render_suggestions()


if __name__ == "__main__":
	main()

	import streamlit as st

st.title("OffMap 🚀")
st.write("Your travel planner is running successfully!")
import streamlit as st

st.title("OffMap 🚀")
st.write("Your travel planner is running successfully!")


