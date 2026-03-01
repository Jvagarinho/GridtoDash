"""
Authentication module for GridToDash
Uses MongoDB for user storage
"""

import streamlit as st
import os
import base64
import hashlib
from pymongo import MongoClient


# MongoDB connection - MUST come from environment variable for security
MONGODB_URI = os.getenv("MONGODB_URI", "")
MONGODB_DB = os.getenv("MONGODB_DB", "gridtodash")


# Translations for login page
LOGIN_TRANSLATIONS = {
    "pt": {
        "subtitle": "Transforme os seus ficheiros Excel/CSV em relatórios PDF profissionais",
        "login_title": "Iniciar Sessão",
        "email": "Email",
        "password": "Password",
        "login_button": "Entrar",
        "error_empty": "Por favor, insere o email e password",
        "error_invalid": "Email ou password incorretos",
        "no_account": "Não tens conta?",
        "signup_title": "Criar Conta",
        "new_email": "Novo Email",
        "new_password": "Nova Password",
        "confirm_password": "Confirmar Password",
        "signup_button": "Criar Conta",
        "error_passwords_dont_match": "As passwords não coincidem",
        "error_password_short": "A password deve ter pelo menos 6 caracteres",
        "error_empty_fields": "Por favor, preenche todos os campos",
        "error_email_exists": "Email já está registado",
        "success_created": "Conta criada com sucesso!",
        "error_connection": "Erro de conexão com base de dados",
    },
    "en": {
        "subtitle": "Transform your Excel/CSV files into professional PDF reports",
        "login_title": "Sign In",
        "email": "Email",
        "password": "Password",
        "login_button": "Sign In",
        "error_empty": "Please enter email and password",
        "error_invalid": "Invalid email or password",
        "no_account": "Don't have an account?",
        "signup_title": "Create Account",
        "new_email": "New Email",
        "new_password": "New Password",
        "confirm_password": "Confirm Password",
        "signup_button": "Create Account",
        "error_passwords_dont_match": "Passwords don't match",
        "error_password_short": "Password must be at least 6 characters",
        "error_empty_fields": "Please fill in all fields",
        "error_email_exists": "Email is already registered",
        "success_created": "Account created successfully!",
        "error_connection": "Database connection error",
    }
}


def get_mongo_client():
    """Get MongoDB client"""
    try:
        client = MongoClient(MONGODB_URI)
        return client
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return None


def get_users_collection():
    """Get users collection"""
    client = get_mongo_client()
    if client:
        db = client[MONGODB_DB]
        return db.users
    return None


def get_logo_base64():
    try:
        with open("logo.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None


LOGO_BASE64 = get_logo_base64()


def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_user(email, password):
    """Verify user credentials from MongoDB"""
    password_hash = hash_password(password)
    
    collection = get_users_collection()
    if collection is None:
        return None
    
    user = collection.find_one({"email": email})
    if user and user.get("passwordHash") == password_hash:
        return {"email": user["email"], "name": user.get("name", "")}
    
    return None


def create_user(email, password, name):
    """Create new user in MongoDB"""
    lang = st.session_state.get("language", "pt")
    t = LOGIN_TRANSLATIONS.get(lang, LOGIN_TRANSLATIONS["pt"])
    
    collection = get_users_collection()
    if collection is None:
        return {"success": False, "error": t["error_connection"]}
    
    # Check if user exists
    existing = collection.find_one({"email": email})
    if existing:
        return {"success": False, "error": t["error_email_exists"]}
    
    # Create user
    password_hash = hash_password(password)
    user_doc = {
        "email": email,
        "passwordHash": password_hash,
        "name": name
    }
    
    try:
        collection.insert_one(user_doc)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def show_login():
    """Show login page"""
    
    lang = st.session_state.get("language", "pt")
    t = LOGIN_TRANSLATIONS.get(lang, LOGIN_TRANSLATIONS["pt"])
    
    # Center everything with columns
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        # Logo - centered
        if LOGO_BASE64:
            st.markdown(f'''
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="data:image/png;base64,{LOGO_BASE64}" width="150" style="border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
            </div>
            ''', unsafe_allow_html=True)
        
        # Title - centered with gradient
        st.markdown('''
        <div style="text-align: center; margin-bottom: 10px;">
            <h1 style="color: #1E3A5F; font-size: 36px; font-weight: 700; margin: 0;">GridToDash</h1>
        </div>
        ''', unsafe_allow_html=True)
        
        # Subtitle - centered
        st.markdown(f'<div style="text-align: center; margin-bottom: 15px;"><p style="color: #64748B; font-size: 14px;">{t["subtitle"]}</p></div>', unsafe_allow_html=True)
        
        # Language selector - right after subtitle
        col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
        with col_l2:
            new_lang = st.selectbox(
                "Idioma / Language",
                options=["pt", "en"],
                format_func=lambda x: "🇵🇹 PT" if x == "pt" else "🇬🇧 EN",
                key="lang_select"
            )
             if new_lang != lang:
                st.session_state.language = new_lang
                st.rerun()
        
        # Login form - all inside one white box
        with st.container():
            st.markdown('''
            <div style="background: white; border-radius: 16px; padding: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-bottom: 20px;">
                <h3 style="text-align: center; color: #1E3A5F; margin-bottom: 25px; font-size: 22px; font-weight: 600;">Iniciar Sessão / Sign In</h3>
            </div>
            ''', unsafe_allow_html=True)
            
            email = st.text_input(t["email"], key="login_email")
            password = st.text_input(t["password"], type="password", key="login_password")
            
            if st.button(t["login_button"], type="primary", use_container_width=True):
                if email and password:
                    user = verify_user(email, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user_email = user["email"]
                        st.session_state.user_name = user.get("name", "")
                        st.rerun()
                    else:
                        st.error(t["error_invalid"])
                else:
                    st.error(t["error_empty"])
        
        # Sign up form - all inside one white box
        with st.container():
            st.markdown('''
            <div style="background: white; border-radius: 16px; padding: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-top: 10px;">
                <p style="text-align: center; color: #64748B; margin-bottom: 20px; font-size: 14px;">Não tens conta? / Don't have an account?</p>
            </div>
            ''', unsafe_allow_html=True)
            
            new_email = st.text_input(t["new_email"], key="signup_email")
            new_password = st.text_input(t["new_password"], type="password", key="signup_password")
            confirm_password = st.text_input(t["confirm_password"], type="password", key="signup_confirm")
            
            if st.button(t["signup_button"], use_container_width=True):
                if new_email and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error(t["error_passwords_dont_match"])
                    elif len(new_password) < 6:
                        st.error(t["error_password_short"])
                    else:
                        result = create_user(new_email, new_password, new_email.split("@")[0])
                        if result and result.get("success"):
                            st.session_state.authenticated = True
                            st.session_state.user_email = new_email
                            st.session_state.user_name = new_email.split("@")[0]
                            st.success(t["success_created"])
                            st.rerun()
                        else:
                            error_msg = result.get("error", "Error") if result else "Error"
                            st.error(f"Error: {error_msg}")
                else:
                    st.error(t["error_empty_fields"])
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Powered by
        st.markdown(f'''
        <div style="text-align: center; margin-top: 25px;">
            <p style="color: #94A3B8; font-size: 12px;">Powered by <b>IterioTech</b></p>
        </div>
        ''', unsafe_allow_html=True)
    
    # CSS for styling
    st.markdown("""
    <style>
    [data-testid="stSelectbox"] {
        max-width: 150px;
        margin: 0 auto;
    }
    div[data-testid="stHorizontalBlock"] {
        justify-content: center;
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
    }
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
