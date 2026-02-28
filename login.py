"""
Convex authentication module for GridToDash
Uses Convex HTTP API directly
"""

import streamlit as st
import os
import base64
import hashlib

# Convex deployment URL
CONVEX_URL = os.getenv("CONVEX_URL", "https://first-pigeon-467.eu-west-1.convex.cloud")


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


def convex_query(query_name, args=None):
    """Execute a Convex query via HTTP"""
    import httpx
    
    url = f"{CONVEX_URL}/api/query"
    
    payload = {
        "path": query_name,
        "args": args or {}
    }
    
    try:
        response = httpx.post(url, json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Convex query error: {e}")
        return None


def convex_mutation(mutation_name, args=None):
    """Execute a Convex mutation via HTTP"""
    import httpx
    
    url = f"{CONVEX_URL}/api/mutation"
    
    payload = {
        "path": mutation_name,
        "args": args or {}
    }
    
    try:
        response = httpx.post(url, json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Convex mutation error: {e}")
        return None


def verify_user_convex(email, password):
    """Verify user credentials against Convex"""
    password_hash = hash_password(password)
    
    # Query Convex database directly for user
    result = convex_query("getUserByEmail", {"email": email})
    
    if result and result.get("value"):
        user = result["value"]
        if user["passwordHash"] == password_hash:
            return {"email": user["email"], "name": user.get("name", "")}
    
    return None


def create_user_convex(email, password, name):
    """Create new user in Convex"""
    password_hash = hash_password(password)
    
    # First check if user exists
    existing = convex_query("getUserByEmail", {"email": email})
    if existing and existing.get("value"):
        return {"success": False, "error": "User already exists"}
    
    # Create user
    result = convex_mutation("createUser", {
        "email": email,
        "passwordHash": password_hash,
        "name": name
    })
    
    if result and result.get("value"):
        return {"success": True}
    
    return {"success": False, "error": "Failed to create user"}


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
                # Verify against Convex
                user = verify_user_convex(email, password)
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
                    # Create user in Convex
                    result = create_user_convex(new_email, new_password, new_email.split("@")[0])
                    if result and result.get("success"):
                        st.session_state.authenticated = True
                        st.session_state.user_email = new_email
                        st.session_state.user_name = new_email.split("@")[0]
                        st.success("Conta criada com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao criar conta. O email pode já estar em uso.")
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
