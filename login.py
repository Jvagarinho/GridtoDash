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
        "forgot_password": "Esqueceu a password?",
        "recover_title": "Recuperar Password",
        "recover_instruction": "Introduz o teu email para receberes um código de recuperação",
        "recover_button": "Gerar Código",
        "reset_title": "Nova Password",
        "reset_instruction": "Introduz o código que recebeste e a nova password",
        "reset_button": "Alterar Password",
        "code": "Código de Recuperação",
        "new_password_repeat": "Nova Password",
        "error_invalid_code": "Código inválido",
        "error_user_not_found": "Email não encontrado",
        "success_recovery": "Código gerado! Copia e usa para redefinir a tua password.",
        "success_reset": "Password alterada com sucesso!",
        "back_to_login": "Voltar ao Login",
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
        "forgot_password": "Forgot password?",
        "recover_title": "Recover Password",
        "recover_instruction": "Enter your email to receive a recovery code",
        "recover_button": "Generate Code",
        "reset_title": "New Password",
        "reset_instruction": "Enter the code you received and your new password",
        "reset_button": "Change Password",
        "code": "Recovery Code",
        "new_password_repeat": "New Password",
        "error_invalid_code": "Invalid code",
        "error_user_not_found": "Email not found",
        "success_recovery": "Code generated! Copy and use it to reset your password.",
        "success_reset": "Password changed successfully!",
        "back_to_login": "Back to Login",
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


import secrets


def generate_recovery_code(email):
    """Generate a recovery code for the user"""
    lang = st.session_state.get("language", "pt")
    t = LOGIN_TRANSLATIONS.get(lang, LOGIN_TRANSLATIONS["pt"])
    
    collection = get_users_collection()
    if collection is None:
        return {"success": False, "error": t["error_connection"]}
    
    user = collection.find_one({"email": email})
    if not user:
        return {"success": False, "error": t["error_user_not_found"]}
    
    code = secrets.token_hex(8)
    
    try:
        collection.update_one(
            {"email": email},
            {"$set": {"recoveryCode": code}}
        )
        return {"success": True, "code": code}
    except Exception as e:
        return {"success": False, "error": str(e)}


def reset_password(email, code, new_password):
    """Reset user password using recovery code"""
    lang = st.session_state.get("language", "pt")
    t = LOGIN_TRANSLATIONS.get(lang, LOGIN_TRANSLATIONS["pt"])
    
    collection = get_users_collection()
    if collection is None:
        return {"success": False, "error": t["error_connection"]}
    
    user = collection.find_one({"email": email, "recoveryCode": code})
    if not user:
        return {"success": False, "error": t["error_invalid_code"]}
    
    password_hash = hash_password(new_password)
    
    try:
        collection.update_one(
            {"email": email},
            {"$set": {"passwordHash": password_hash}, "$unset": {"recoveryCode": ""}}
        )
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def show_login():
    """Show login page"""
    
    lang = st.session_state.get("language", "pt")
    t = LOGIN_TRANSLATIONS.get(lang, LOGIN_TRANSLATIONS["pt"])
    
    # CSS for forgot password and language selector
    st.markdown("""
    <style>
    button[key="forgot_password_btn"] {
        background: none !important;
        border: none !important;
        padding: 0 !important;
        color: #059669 !important;
        text-decoration: underline !important;
        font-size: 14px !important;
        font-weight: normal !important;
        box-shadow: none !important;
    }
    button[key="forgot_password_btn"]:hover {
        background: none !important;
        color: #047857 !important;
    }
    [data-testid="stSelectbox"] {
        text-align: center;
    }
    [data-testid="stSelectbox"] > div {
        justify-content: center;
    }
    div[data-testid="stHorizontalBlock"] {
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
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
        
        # Language selector - toggle switch
        col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
        with col_l2:
            new_lang = "en" if lang == "pt" else "pt"
            st.markdown(f'''
            <style>
            .toggle-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                margin-bottom: 20px;
                gap: 10px;
            }}
            .toggle-label {{
                font-weight: bold;
                font-size: 14px;
                color: #64748B;
            }}
            .toggle-label.active {{
                color: #059669;
            }}
            .toggle-switch {{
                position: relative;
                width: 56px;
                height: 28px;
                background: #059669;
                border-radius: 28px;
                cursor: pointer;
                transition: 0.3s;
            }}
            .toggle-switch::before {{
                content: "";
                position: absolute;
                width: 22px;
                height: 22px;
                background: white;
                border-radius: 50%;
                top: 3px;
                left: 3px;
                transition: 0.3s;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }}
            .toggle-switch.en::before {{
                transform: translateX(28px);
            }}
            </style>
            <div class="toggle-container">
                <span class="toggle-label {"active" if lang == "pt" else ""}">PT</span>
                <div class="toggle-switch {"en" if lang == "en" else ""}" onclick="document.querySelector('button[key=\\'lang_toggle_btn\\']').click()"></div>
                <span class="toggle-label {"active" if lang == "en" else ""}">EN</span>
            </div>
            ''', unsafe_allow_html=True)
            
            if st.button("Toggle", key="lang_toggle_btn", help="Toggle language"):
                st.session_state.language = new_lang
                st.rerun()
        
        # Login form - all inside one white box
        with st.container():
            st.markdown(f'''
            <div style="background: white; border-radius: 16px; padding: 5px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-bottom: 20px;">
                <h3 style="text-align: center; color: #1E3A5F; margin-bottom: 0px; font-size: 22px; font-weight: 500;">{t["login_title"]}</h3>
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
        
        # Forgot Password link
        if "show_recovery" not in st.session_state:
            st.session_state.show_recovery = False
        if "show_reset" not in st.session_state:
            st.session_state.show_reset = False
        
        if not st.session_state.show_recovery and not st.session_state.show_reset:
            # Check if recovery was triggered via URL param
            if st.query_params.get("recover") == "1":
                st.session_state.show_recovery = True
                st.query_params.clear()
                st.rerun()
            
            st.markdown(f'''
            <style>
            .forgot-password-link {{
                text-align: center;
                margin-top: 10px;
                margin-bottom: 20px;
            }}
            .forgot-password-link a {{
                color: #059669;
                text-decoration: underline;
                cursor: pointer;
                font-size: 14px;
            }}
            .forgot-password-link a:hover {{
                color: #047857;
            }}
            </style>
            <div class="forgot-password-link">
                <a href="?recover=1">{t["forgot_password"]}</a>
            </div>
            ''', unsafe_allow_html=True)
        
        # Recovery form - generate code
        if st.session_state.show_recovery and not st.session_state.show_reset:
            with st.container():
                st.markdown(f'''
                <div style="background: white; border-radius: 16px; padding: 5px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-top: 20px; margin-bottom: 20px;">
                    <h3 style="text-align: center; color: #1E3A5F; margin-bottom: 0px; font-size: 22px; font-weight: 500;">{t["recover_title"]}</h3>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown(f'<p style="text-align: center; color: #64748B; margin-bottom: 15px;">{t["recover_instruction"]}</p>', unsafe_allow_html=True)
                
                recover_email = st.text_input(t["email"], key="recover_email")
                
                col_r1, col_r2 = st.columns([1, 1])
                with col_r1:
                    if st.button(t["recover_button"], type="primary", use_container_width=True):
                        if recover_email:
                            result = generate_recovery_code(recover_email)
                            if result.get("success"):
                                st.session_state.recovery_code = result["code"]
                                st.session_state.recovery_email = recover_email
                                st.session_state.show_recovery = False
                                st.session_state.show_reset = True
                                st.rerun()
                            else:
                                st.error(result.get("error", t["error_connection"]))
                        else:
                            st.error(t["error_empty_fields"])
                with col_r2:
                    if st.button(t["back_to_login"], use_container_width=True):
                        st.session_state.show_recovery = False
                        st.rerun()
        
        # Reset form - enter new password
        if st.session_state.show_reset:
            with st.container():
                st.markdown(f'''
                <div style="background: white; border-radius: 16px; padding: 5px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-top: 20px;">
                    <h3 style="text-align: center; color: #1E3A5F; margin-bottom: 0px; font-size: 22px; font-weight: 500;">{t["reset_title"]}</h3>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown(f'<p style="text-align: center; color: #64748B; margin-bottom: 15px;">{t["reset_instruction"]}</p>', unsafe_allow_html=True)
                
                if hasattr(st.session_state, 'recovery_code'):
                    recovery_code = st.session_state.recovery_code
                    st.markdown(f'''
                    <div style="background: #FEF3C7; border-radius: 8px; padding: 15px; margin-bottom: 15px; text-align: center;">
                        <p style="margin: 0; color: #92400E; font-weight: bold;">{t["success_recovery"]}</p>
                        <p style="margin: 10px 0 0 0; font-size: 24px; font-weight: bold; letter-spacing: 2px; color: #059669;">{recovery_code}</p>
                    </div>
                    ''', unsafe_allow_html=True)
                
                reset_code = st.text_input(t["code"], key="reset_code")
                new_pass = st.text_input(t["new_password_repeat"], type="password", key="new_password_reset")
                confirm_pass = st.text_input(t["confirm_password"], type="password", key="confirm_password_reset")
                
                col_r1, col_r2 = st.columns([1, 1])
                with col_r1:
                    if st.button(t["reset_button"], type="primary", use_container_width=True):
                        if reset_code and new_pass and confirm_pass:
                            if new_pass != confirm_pass:
                                st.error(t["error_passwords_dont_match"])
                            elif len(new_pass) < 6:
                                st.error(t["error_password_short"])
                            else:
                                result = reset_password(
                                    st.session_state.recovery_email,
                                    reset_code,
                                    new_pass
                                )
                                if result.get("success"):
                                    st.session_state.show_reset = False
                                    if hasattr(st.session_state, 'recovery_code'):
                                        del st.session_state.recovery_code
                                    if hasattr(st.session_state, 'recovery_email'):
                                        del st.session_state.recovery_email
                                    st.success(t["success_reset"])
                                    st.rerun()
                                else:
                                    st.error(result.get("error", t["error_connection"]))
                        else:
                            st.error(t["error_empty_fields"])
                with col_r2:
                    if st.button(t["back_to_login"], use_container_width=True):
                        st.session_state.show_reset = False
                        if hasattr(st.session_state, 'recovery_code'):
                            del st.session_state.recovery_code
                        if hasattr(st.session_state, 'recovery_email'):
                            del st.session_state.recovery_email
                        st.rerun()
        
        # Sign up form - all inside one white box
        with st.container():
            st.markdown(f'''
            <div style="background: white; border-radius: 16px; padding: 5px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-top: 20px;">
                <p style="text-align: center; color: #1E3A5F; margin-bottom: 0px; font-size: 22px; font-weight: 500;">{t["no_account"]}</p>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
            
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
