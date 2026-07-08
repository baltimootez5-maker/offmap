"""
OffMap v2 - Premium Travel Discovery Platform
Phase 1: Beautiful UI/UX with Hero Landing
Designed to feel like Airbnb + Apple + Spotify
"""

import streamlit as st
import json
import os
import io
import time
import random
import requests
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from pathlib import Path
from datetime import datetime

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="OffMap - Discover Hidden Gems",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# ==================== MODERN CSS STYLING ====================
MODERN_STYLES = '''
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    :root {
        --primary: #FF6B6B;
        --secondary: #4ECDC4;
        --accent: #FFE66D;
        --dark: #1a1a2e;
        --light: #f8f9fa;
        --text-dark: #2d3436;
        --text-light: #636e72;
        --border-radius: 16px;
        --shadow-sm: 0 2px 8px rgba(0,0,0,0.08);
        --shadow-md: 0 8px 24px rgba(0,0,0,0.12);
        --shadow-lg: 0 16px 48px rgba(0,0,0,0.16);
    }
    
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', sans-serif;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        color: var(--text-dark);
    }
    
    /* Hero Section */
    .hero-container {
        position: relative;
        min-height: 100vh;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .hero-bg {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600"><defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/></pattern></defs><rect width="1200" height="600" fill="url(%23grid)" /></svg>');
        opacity: 0.1;
        animation: drift 20s linear infinite;
    }
    
    @keyframes drift {
        0% { transform: translate(0, 0); }
        100% { transform: translate(40px, 40px); }
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
        text-align: center;
        color: white;
        padding: 60px 40px;
        max-width: 900px;
        animation: fadeInUp 1s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        margin-bottom: 20px;
        letter-spacing: -1px;
        line-height: 1.2;
        animation: slideDown 0.8s ease-out;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        font-weight: 300;
        margin-bottom: 50px;
        opacity: 0.9;
        animation: fadeIn 1s ease-out 0.3s both;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Search Bar */
    .search-container {
        animation: fadeIn 1s ease-out 0.5s both;
        margin-bottom: 50px;
    }
    
    .search-box {
        display: flex;
        gap: 12px;
        background: rgba(255, 255, 255, 0.95);
        padding: 12px;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-lg);
        backdrop-filter: blur(10px);
        max-width: 600px;
        margin: 0 auto;
    }
    
    .search-input {
        flex: 1;
        border: none;
        outline: none;
        font-size: 1.1rem;
        padding: 12px 16px;
        border-radius: 12px;
        background: transparent;
        color: var(--text-dark);
    }
    
    .search-input::placeholder {
        color: var(--text-light);
    }
    
    .search-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 1rem;
    }
    
    .search-btn:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    /* Destination Cards */
    .destinations-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 24px;
        padding: 60px 40px;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .destination-card {
        background: white;
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
    }
    
    .destination-card:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: var(--shadow-lg);
    }
    
    .destination-image {
        width: 100%;
        height: 240px;
        object-fit: cover;
        transition: transform 0.4s ease;
    }
    
    .destination-card:hover .destination-image {
        transform: scale(1.08);
    }
    
    .destination-content {
        padding: 24px;
    }
    
    .destination-location {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.9rem;
        color: var(--text-light);
        margin-bottom: 8px;
    }
    
    .destination-name {
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--text-dark);
        margin-bottom: 12px;
        line-height: 1.3;
    }
    
    .destination-desc {
        font-size: 0.95rem;
        color: var(--text-light);
        line-height: 1.6;
        margin-bottom: 16px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    
    .destination-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 16px;
    }
    
    .tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .destination-actions {
        display: flex;
        gap: 12px;
    }
    
    .btn-action {
        flex: 1;
        padding: 10px 16px;
        border: none;
        border-radius: 10px;
        font-size: 0.9rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .btn-save {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .btn-save:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
    }
    
    .btn-info {
        background: var(--light);
        color: var(--text-dark);
        border: 2px solid #e0e0e0;
    }
    
    .btn-info:hover {
        border-color: var(--primary);
        color: var(--primary);
    }
    
    /* Section Headers */
    .section-header {
        text-align: center;
        margin-bottom: 50px;
        animation: fadeIn 1s ease-out;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--text-dark);
        margin-bottom: 12px;
    }
    
    .section-subtitle {
        font-size: 1.1rem;
        color: var(--text-light);
        font-weight: 400;
    }
    
    /* Filters & Sidebar */
    .filter-container {
        background: white;
        padding: 24px;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-sm);
        margin-bottom: 30px;
    }
    
    .filter-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-dark);
        margin-bottom: 16px;
    }
    
    /* Loading & Animations */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(102, 126, 234, 0.2);
        border-top-color: #667eea;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
        }
        
        .destinations-grid {
            grid-template-columns: 1fr;
            padding: 40px 20px;
        }
        
        .section-title {
            font-size: 1.8rem;
        }
    }
</style>
'''

st.markdown(MODERN_STYLES, unsafe_allow_html=True)

# ==================== DATA ====================
PLACES = [
    {
        "name": "Kawah Ijen Blue Fire",
        "country": "Indonesia",
        "desc": "A volcanic crater famous for electric-blue flames and sulfur miners.",
        "img": "assets/kawah_ijen.png",
        "remote_img": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80",
        "tags": ["volcano", "adventure"],
        "mood": "Adventure",
        "price": "€450-650",
    },
    {
        "name": "Svaneti Villages",
        "country": "Georgia",
        "desc": "Remote mountain villages with medieval towers and alpine trails.",
        "img": "assets/svaneti.png",
        "remote_img": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1200&q=80",
        "tags": ["mountains", "culture"],
        "mood": "Cultural",
        "price": "€300-500",
    },
    {
        "name": "Islas Cies",
        "country": "Spain",
        "desc": "Pristine beaches and crystal waters on a protected island archipelago.",
        "img": "assets/islas_cies.png",
        "remote_img": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80",
        "tags": ["beach", "relax"],
        "mood": "Relaxing",
        "price": "€250-400",
    },
    {
        "name": "Valle de Viñales",
        "country": "Cuba",
        "desc": "Limestone mogotes, tobacco farms, and colorful rural life.",
        "img": "assets/vinales.png",
        "remote_img": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=1200&q=80",
        "tags": ["nature", "culture"],
        "mood": "Adventure",
        "price": "€350-550",
    },
    {
        "name": "Cappadocia Hot Air Balloons",
        "country": "Turkey",
        "desc": "Ancient cave dwellings, fairy chimneys, and sunrise hot air balloon rides over surreal landscapes.",
        "img": "assets/cappadocia.png",
        "remote_img": "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?auto=format&fit=crop&w=1200&q=80",
        "tags": ["adventure", "scenic"],
        "mood": "Hidden Gem",
        "price": "€400-700",
    },
]

WISHLIST_FILE = "wishlist.json"
BASE_API_URL = "http://localhost:8000"

# ==================== UTILITIES ====================
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


def ensure_assets():
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    for p in PLACES:
        path = Path(p["img"])
        if not path.exists():
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


def backend_headers():
    headers = {}
    token = st.session_state.get("auth_token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def add_to_wishlist(name):
    if "wishlist" not in st.session_state:
        st.session_state.wishlist = load_wishlist()
    if name not in st.session_state.wishlist:
        st.session_state.wishlist.append(name)
        save_wishlist(st.session_state.wishlist)


def remove_from_wishlist(name):
    if "wishlist" not in st.session_state:
        st.session_state.wishlist = load_wishlist()
    if name in st.session_state.wishlist:
        st.session_state.wishlist.remove(name)
        save_wishlist(st.session_state.wishlist)


# ==================== COMPONENTS ====================
def render_hero():
    """Cinematic hero section with search"""
    hero_html = f'''
    <div class="hero-container">
        <div class="hero-bg"></div>
        <div class="hero-content">
            <h1 class="hero-title">✨ OffMap</h1>
            <p class="hero-subtitle">Discover hidden gems off the beaten path — curated for curious travelers</p>
            <div class="search-container">
                <div class="search-box">
                    <input class="search-input" type="text" placeholder="🌍 Where's your next adventure?" id="hero-search">
                    <button class="search-btn" onclick="document.getElementById('search-scroll').scrollIntoView({{behavior: 'smooth'}})">Explore</button>
                </div>
            </div>
        </div>
    </div>
    '''
    st.markdown(hero_html, unsafe_allow_html=True)
    st.markdown("<div id='search-scroll'></div>", unsafe_allow_html=True)


def render_destination_card(place):
    """Beautiful destination card with hover effects"""
    tags_html = "".join([f'<span class="tag">{t}</span>' for t in place.get("tags", [])])
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f'''
        <div class="destination-card">
            <img src="{place.get('remote_img')}" class="destination-image" onerror="this.src='{place.get('img')}'">
            <div class="destination-content">
                <div class="destination-location">
                    📍 {place['country']} • {place.get('price', 'N/A')}
                </div>
                <div class="destination-name">{place['name']}</div>
                <div class="destination-desc">{place['desc']}</div>
                <div class="destination-tags">{tags_html}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Action buttons
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button(f"❤️ Save", key=f"save_{place['name']}", use_container_width=True):
            add_to_wishlist(place['name'])
            st.success(f"Saved {place['name']}!")
    
    with col_btn2:
        if st.button(f"ℹ️ Details", key=f"info_{place['name']}", use_container_width=True):
            st.session_state.selected_place = place


def render_destinations_section(country_filter=None, tags_filter=None, search_query=None):
    """Display destinations with filters"""
    visible = PLACES[:]
    
    if country_filter and country_filter != "All":
        visible = [p for p in visible if p["country"] == country_filter]
    
    if tags_filter:
        visible = [p for p in visible if any(t in p.get("tags", []) for t in tags_filter)]
    
    if search_query:
        q = search_query.lower()
        visible = [p for p in visible if q in p["name"].lower() or q in p["desc"].lower()]
    
    st.markdown('''
    <div class="section-header">
        <h2 class="section-title">🗺️ Hidden Gems Await</h2>
        <p class="section-subtitle">Carefully curated destinations for the curious traveler</p>
    </div>
    ''', unsafe_allow_html=True)
    
    if not visible:
        st.info("No destinations match your filters. Try adjusting them!")
        return
    
    cols = st.columns(3)
    for i, place in enumerate(visible):
        with cols[i % 3]:
            render_destination_card(place)


def render_sidebar_filters():
    """Modern sidebar with filters"""
    with st.sidebar:
        st.markdown("### 🎯 Filters & Settings")
        
        countries = sorted({p["country"] for p in PLACES})
        countries.insert(0, "All")
        selected_country = st.selectbox("Country", countries)
        
        all_tags = sorted({t for p in PLACES for t in p.get("tags", [])})
        selected_tags = st.multiselect("Tags", all_tags)
        
        st.markdown("---")
        st.markdown("### 💖 Wishlist")
        if "wishlist" not in st.session_state:
            st.session_state.wishlist = load_wishlist()
        
        if st.session_state.wishlist:
            for item in st.session_state.wishlist:
                st.write(f"✨ {item}")
            if st.button("Clear Wishlist", use_container_width=True):
                st.session_state.wishlist = []
                save_wishlist([])
                st.rerun()
        else:
            st.write("*No saved destinations yet*")
        
        return selected_country, selected_tags


# ==================== MAIN ====================
def main():
    ensure_assets()
    
    # Hero Section
    render_hero()
    
    # Main Content
    st.markdown("<hr style='margin: 40px 0; border: none; height: 1px; background: linear-gradient(90deg, transparent, #e0e0e0, transparent);'>", unsafe_allow_html=True)
    
    country_filter, tags_filter = render_sidebar_filters()
    
    search_query = st.text_input("", placeholder="Search destinations...", label_visibility="collapsed")
    
    render_destinations_section(country_filter, tags_filter, search_query)
    
    # Footer
    st.markdown("---")
    st.markdown('''
    <div style="text-align: center; padding: 40px 20px; color: #636e72;">
        <p style="font-size: 0.95rem; margin-bottom: 10px;">✨ <strong>OffMap</strong> - Discover Hidden Gems</p>
        <p style="font-size: 0.85rem; opacity: 0.7;">Curated for curious travelers • Phase 1 Launch</p>
    </div>
    ''', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
