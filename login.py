"""
Login module for GridToDash
Simple login with Clerk authentication
"""

import streamlit as st
import os
import base64


# Clerk Keys
CLERK_PUBLISHABLE_KEY = os.getenv("NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY", "pk_test_Y2xvc2luZy1iYXQtNjYuY2xlcmsuYWNjb3VudHMuZGV2JA")

# Get the redirect URL - can be set via environment variable for production
REDIRECT_URL = os.getenv("REDIRECT_URL", "https://gridtodash.streamlit.app")


def get_logo_base64():
    try:
        with open("logo.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None


LOGO_BASE64 = get_logo_base64()


def show_login():
    """Show login page"""
    
    lang = st.session_state.get("language", "pt")
    
    # Get translations
    if lang == "pt":
        subtitle = "Transforme os seus ficheiros Excel/CSV em relatórios PDF profissionais"
        btn_text = "Aceder"
    else:
        subtitle = "Transform your Excel/CSV files into professional PDF reports"
        btn_text = "Get Started"
    
    # Center everything with columns - use full width middle column
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        # Logo - centered
        if LOGO_BASE64:
            st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{LOGO_BASE64}" width="120" style="margin-bottom: 10px;"></div>', unsafe_allow_html=True)
        
        # Title - centered
        st.markdown('<div style="text-align: center;"><h1 style="color: #1E3A5F; font-size: 28px; margin: 10px 0;">GridToDash</h1></div>', unsafe_allow_html=True)
        
        # Subtitle - centered
        st.markdown(f'<div style="text-align: center;"><p style="color: #64748B; font-size: 14px; margin-bottom: 20px;">{subtitle}</p></div>', unsafe_allow_html=True)
        
        # Button - link to Clerk with redirect back to app
        clerk_url = f"https://closing-bat-66.accounts.dev/sign-in?redirect_url={REDIRECT_URL}"
        st.markdown(f'''
        <div style="text-align: center;">
            <a href="{clerk_url}" target="_self" style="
                display: inline-block;
                background: #059669;
                color: #ffffff;
                padding: 10px 40px;
                border-radius: 8px;
                text-decoration: none;
                font-weight: 600;
            ">{btn_text}</a>
        </div>
        '''.format(btn_text=btn_text), unsafe_allow_html=True)
        
        # Instructions
        st.markdown('<div style="text-align: center; margin-top: 15px; color: #64748B; font-size: 12px;">1. Clica em Aceder<br>2. Faz login no Clerk<br>3. Após login, serás redirecionado para a app</div>', unsafe_allow_html=True)
        
        # Powered by - centered
        st.markdown('<div style="text-align: center;"><p style="color: #94A3B8; font-size: 12px; margin-top: 15px;">Powered by <b>IterioTech</b></p></div>', unsafe_allow_html=True)
        
        # Language selector - centered
        col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
        with col_l2:
            new_lang = st.selectbox(
                "Idioma",
                options=["pt", "en"],
                format_func=lambda x: "PT" if x == "pt" else "EN",
                key="lang_select"
            )
            if new_lang != lang:
                st.session_state.language = new_lang
                st.rerun()
    
    # CSS to make selectbox narrower and centered
    st.markdown("""
    <style>
    [data-testid="stSelectbox"] {
        max-width: 100px;
        margin: 0 auto;
    }
    div[data-testid="stHorizontalBlock"] {
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)
