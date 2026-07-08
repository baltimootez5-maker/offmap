# OffMap
# 🗺️ OffMap: Travel Discovery Platform

🚀 **[View Live Interactive Demo](https://offmap-vexna78pulc7xjeskjzsac.streamlit.app/)**

An AI-ready travel discovery platform built using **Python, Streamlit, and FastAPI**. Features a responsive UI with an interactive "Mystery Postcard" generator and a lightweight backend API layer for user wishlist management.

## 🛠️ Tech Stack
* **Frontend UI:** Streamlit
* **Backend API:** FastAPI + Uvicorn
* **Environment:** Python 3.10+
A small Streamlit travel discovery app with a playful "Mystery Postcard" feature and a tiny FastAPI wishlist backend scaffold.

Run the Streamlit app:
```bash
pip install -r requirements.txt
streamlit run app.py
```

Run the API (optional):
```bash
uvicorn api.main:app --reload --port 8000
```

The API exposes `/wishlist` endpoints to get/add/delete wishlist items.
