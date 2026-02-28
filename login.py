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
# Add to Streamlit Cloud secrets:
# MONGODB_URI = "mongodb+srv://username:password@cluster.mongodb.net/?appName=AppName"
MONGODB_URI = os.getenv("MONGODB_URI", "")
MONGODB_DB = os.getenv("MONGODB_DB", "gridtodash")


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
    collection = get_users_collection()
    if collection is None:
        return {"success": False, "error": "Erro de conexão com base de dados"}
    
    # Check if user exists
    existing = collection.find_one({"email": email})
    if existing:
        return {"success": False, "error": "Email já está registado"}
    
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
    
    # Get translations
    if lang == "pt":
        subtitle = "Transforme os seus ficheiros Excel/CSV em relatórios PDF profissionais"
    else:
        subtitle = "Transform your Excel/CSV files into professional PDF reports"
    
    # Center everything with columns
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        # Logo - centered
        if LOGO_BASE64:
            st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{LOGO_BASE64}" width="120" style="margin-bottom: 10px;"></div>', unsafe_allow_html=True)
        
        # Title - centered
        st.markdown('<div style="text-align: center;"><h1 style="color: #1E3A5F; font-size: 28px; margin: 10px 0;">GridToDash</h1></div>', unsafe_allow_html=True)
        
        # Subtitle - centered
        st.markdown(f'<div style="text-align: center;"><p style="color: #64748B; font-size: 14px; margin-bottom: 20px;">{subtitle}</p></div>', unsafe_allow_html=True)
        
        # Email login form
        st.markdown("---")
        st.markdown('<div style="text-align: center;"><p style="color: #1E3A5F; font-size: 16px; margin-bottom: 15px;">Iniciar Sessão</p></div>', unsafe_allow_html=True)
        
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Entrar", type="primary"):
            if email and password:
                # Verify user
                user = verify_user(email, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user_email = user["email"]
                    st.session_state.user_name = user.get("name", "")
                    st.rerun()
                else:
                    st.error("Email ou password incorretos")
            else:
                st.error("Por favor, insere o email e password")
        
        # Sign up link
        st.markdown("---")
        st.markdown('<div style="text-align: center;"><p style="color: #64748B; font-size: 14px;">Não tens conta?</p></div>', unsafe_allow_html=True)
        
        new_email = st.text_input("Novo Email", key="signup_email")
        new_password = st.text_input("Nova Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirmar Password", type="password", key="signup_confirm")
        
        if st.button("Criar Conta"):
            if new_email and new_password and confirm_password:
                if new_password != confirm_password:
                    st.error("As passwords não coincidem")
                elif len(new_password) < 6:
                    st.error("A password deve ter pelo menos 6 caracteres")
                else:
                    # Create user
                    result = create_user(new_email, new_password, new_email.split("@")[0])
                    if result and result.get("success"):
                        st.session_state.authenticated = True
                        st.session_state.user_email = new_email
                        st.session_state.user_name = new_email.split("@")[0]
                        st.success("Conta criada com sucesso!")
                        st.rerun()
                    else:
                        error_msg = result.get("error", "Erro desconhecido") if result else "Erro de conexão"
                        st.error(f"Erro: {error_msg}")
            else:
                st.error("Por favor, preenche todos os campos")
        
        # Powered by - centered
        st.markdown("---")
        st.markdown('<div style="text-align: center;"><p style="color: #94A3B8; font-size: 12px; margin-top: 15px;">Powered by <b>IterioTech</b></div>', unsafe_allow_html=True)
        
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
