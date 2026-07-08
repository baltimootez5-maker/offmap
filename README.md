# OffMap

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
