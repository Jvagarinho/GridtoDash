"""
GridToDash - Excel to PDF Automated Reporter
A professional IterioTech application for small business owners to convert
Excel/CSV files into polished, branded PDF reports.
"""

import os
import tempfile
import base64
from datetime import datetime
from io import BytesIO

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Import login module
from login import show_login

# Get the redirect URL - can be set via environment variable for production
# For Streamlit Cloud, set this environment variable to your app's URL
REDIRECT_URL = os.getenv("REDIRECT_URL", "https://gridtodash.streamlit.app")


# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None


# Language Translations
TRANSLATIONS = {
    "pt": {
        "app_title": "GridToDash",
        "hero_title": "GridToDash",
        "hero_subtitle": "Transforme os seus ficheiros Excel/CSV em relatórios PDF profissionais",
        "hero_description": "Carregue os seus dados, visualize métricas e faça download de um relatório polido em segundos",
        "file_uploader": "Escolha um ficheiro Excel ou CSV",
        "file_uploader_help": "Arraste e solte ou clique para selecionar",
        "file_uploader_drag": "Arraste e solte o ficheiro aqui",
        "file_uploader_limit": "Limite 200MB por ficheiro",
        "file_uploader_browse": "Procurar ficheiros",
        "sidebar_about_title": "Sobre",
        "sidebar_about_text": "GridToDash transforma os seus ficheiros Excel e CSV em relatórios PDF profissionais instantaneamente. Perfeito para pequenos empresários que precisam de relatórios rápidos e polidos sem experiência em design.",
        "sidebar_built_with": "Feito com IterioTech",
        "key_metrics": "Métricas Principais",
        "total_records": "Total de Registos",
        "total_sum": "Soma Total",
        "average_value": "Valor Médio",
        "data_preview": "Pré-visualização dos Dados",
        "chart_title": "Gráfico",
        "generate_pdf": "Gerar Relatório PDF",
        "processing": "A processar o seu ficheiro...",
        "generating_pdf": "A gerar o relatório PDF...",
        "success_message": "PDF Ready! O seu relatório está pronto para download.",
        "download_pdf": "Download do Relatório PDF",
        "error_empty_file": "Erro: O ficheiro carregado está vazio.",
        "error_no_numeric": "Erro: Não foram encontradas colunas numéricas no ficheiro.",
        "error_loading": "Erro ao carregar ficheiro: ",
        "error_unexpected": "Ocorreu um erro inesperado: ",
        "select_column": "Selecionar coluna para métricas",
        "select_x_axis": "Selecionar coluna para eixo X",
        "select_y_axis": "Selecionar coluna para eixo Y",
        "select_columns_pdf": "Selecionar colunas para o relatório PDF",
        "about": "Sobre",
    },
    "en": {
        "app_title": "GridToDash",
        "hero_title": "GridToDash",
        "hero_subtitle": "Transform your Excel/CSV files into professional PDF reports",
        "hero_description": "Upload your data, visualize metrics, and download a polished report in seconds",
        "file_uploader": "Choose an Excel or CSV file",
        "file_uploader_help": "Drag and drop or click to select",
        "file_uploader_drag": "Drag and drop file here",
        "file_uploader_limit": "Limit 200MB per file",
        "file_uploader_browse": "Browse files",
        "sidebar_about_title": "About",
        "sidebar_about_text": "GridToDash transforms your Excel and CSV files into professional PDF reports instantly. Perfect for small business owners who need quick, polished reports without design expertise.",
        "sidebar_built_with": "Built with IterioTech",
        "key_metrics": "Key Metrics",
        "total_records": "Total Records",
        "total_sum": "Total Sum",
        "average_value": "Average Value",
        "data_preview": "Data Preview",
        "chart_title": "Chart",
        "generate_pdf": "Generate PDF Report",
        "processing": "Processing your file...",
        "generating_pdf": "Generating PDF report...",
        "success_message": "PDF Ready! Your report is ready for download.",
        "download_pdf": "Download PDF Report",
        "error_empty_file": "Error: The uploaded file is empty.",
        "error_no_numeric": "Error: No numeric columns found in the uploaded file.",
        "error_loading": "Error loading file: ",
        "error_unexpected": "An unexpected error occurred: ",
        "select_column": "Select column for metrics",
        "select_x_axis": "Select column for X-axis",
        "select_y_axis": "Select column for Y-axis",
        "select_columns_pdf": "Select columns for PDF report",
        "about": "About",
    }
}

def get_translation(key):
    """Get translation for the current language."""
    lang = st.session_state.get("language", "pt")
    return TRANSLATIONS[lang].get(key, key)

# Initialize language in session state
if "language" not in st.session_state:
    st.session_state.language = "pt"

# Page Configuration
st.set_page_config(
    page_title="GridToDash - Professional Reporter",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Boutique Look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 100%);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E3A5F 0%, #0F172A 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: rgba(255,255,255,0.9);
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }
    
    /* Main title */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1E3A5F 0%, #059669 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: fadeInDown 0.8s ease-out;
    }
    
    /* Hero section */
    .hero-section {
        background: white;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 40px rgba(30, 58, 95, 0.1);
        margin-bottom: 30px;
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid rgba(30, 58, 95, 0.1);
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(30, 58, 95, 0.15);
    }
    .metric-card h3 {
        font-size: 0.875rem;
        color: #64748B;
        font-weight: 500;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-card .value {
        font-size: 2rem;
        font-weight: 700;
    }
    .metric-card .value.navy { color: #1E3A5F; }
    .metric-card .value.green { color: #059669; }
    .metric-card .value.blue { color: #0EA5E9; }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 14px 32px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(5, 150, 105, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(5, 150, 105, 0.4);
    }
    
    /* Success message */
    .success-message {
        padding: 20px 24px;
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        border-left: 4px solid #059669;
        border-radius: 12px;
        margin: 20px 0;
        animation: slideInRight 0.5s ease-out;
    }
    .success-message strong {
        color: #047857;
        font-size: 1.1rem;
    }
    
    /* Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1E3A5F;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #E2E8F0;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* Spinner */
    [data-testid="stSpinner"] {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    /* Download button */
    .download-btn {
        background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%) !important;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3) !important;
    }
    .download-btn:hover {
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4) !important;
    }
    
    /* Hide Deploy button */
    [data-testid="stDeployButton"] {
        display: none !important;
    }
    
    /* Custom File Uploader */
    .custom-upload-btn {
        display: inline-block;
        padding: 12px 24px;
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white !important;
        border-radius: 12px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(5, 150, 105, 0.3);
    }
    .custom-upload-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(5, 150, 105, 0.4);
    }
    
    /* Logo smaller */
    [data-testid="stSidebar"] .stImage > img {
        max-width: 120px !important;
        height: auto !important;
    }
    
    /* Language buttons smaller */
    [data-testid="stSidebar"] .stButton > button {
        padding: 8px 16px !important;
        font-size: 0.9rem !important;
    }
    
    /* Hide custom file uploader section - use native instead */
    /* Keep native file uploader but translate via JS */
    
    /* Sidebar toggle button - always visible */
    [data-testid="stSidebarCollapseButton"] {
        background: #059669 !important;
        border: none !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    [data-testid="stSidebarCollapseButton"]:hover {
        background: #047857 !important;
    }
    [data-testid="stSidebarCollapseButton"] > button > svg,
    [data-testid="stSidebarCollapseButton"] > svg,
    [data-testid="stSidebarCollapseButton"] svg {
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
        color: #FFFFFF !important;
        opacity: 1 !important;
    }
    
    /* Better mobile sidebar behavior */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            min-width: 200px !important;
            max-width: 200px !important;
        }
    }
    </style>
    
    <script>
    function getCurrentLang() {{
        // Check which language button is styled as primary
        const buttons = document.querySelectorAll('[data-testid="stSidebar"] button');
        for (let btn of buttons) {{
            if (btn.innerText === 'PT' && btn.getAttribute('kind') === 'secondary') {{
                return 'pt';
            }}
            if (btn.innerText === 'EN' && btn.getAttribute('kind') === 'secondary') {{
                return 'en';
            }}
        }}
        return 'pt'; // default
    }}
    
    function translateUploader() {{
        const lang = window.currentLang || 'pt';
        const texts = {{
            'pt': {{ drag: 'Arraste e solte o ficheiro aqui', limit: 'Limite 200MB por ficheiro', browse: 'Procurar ficheiros' }},
            'en': {{ drag: 'Drag and drop file here', limit: 'Limit 200MB per file', browse: 'Browse files' }}
        }};
        
        // Translate span with class st-emotion-cache-ycmcfb
        const spans = document.querySelectorAll('.st-emotion-cache-ycmcfb span');
        for (let span of spans) {{
            if (span.innerText && span.innerText.trim() !== '') {{
                span.innerText = texts[lang].drag;
            }}
        }}
        
        // Translate p tag
        const ps = document.querySelectorAll('.st-emotion-cache-ycmcfb p');
        for (let p of ps) {{
            if (p.innerText && (p.innerText.includes('200MB') || p.innerText.includes('Limit'))) {{
                p.innerText = texts[lang].limit + ' • XLSX, CSV';
            }}
        }}
        
        // Translate button
        const buttons = document.querySelectorAll('.st-emotion-cache-ycmcfb button');
        for (let btn of buttons) {{
            if (btn.innerText && btn.innerText.includes('Browse')) {{
                btn.innerText = texts[lang].browse;
            }}
        }}
    }}
    
    // Set language from Python and run translation
    window.currentLang = "{st.session_state.get('language', 'pt')}";
    window.addEventListener('load', function() {{
        setTimeout(translateUploader, 500);
        setInterval(translateUploader, 2000);
    }});
    </script>
""", unsafe_allow_html=True)


def load_data(uploaded_file):
    """
    Load Excel or CSV file into a Pandas DataFrame.
    Handles both .xlsx and .csv formats.
    """
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        if df.empty:
            raise ValueError("The uploaded file is empty.")
        
        return df
    except Exception as e:
        raise ValueError(f"Error loading file: {str(e)}")


def identify_numeric_columns(df):
    """Identify and return list of numeric columns in the DataFrame."""
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if not numeric_cols:
        raise ValueError("No numeric columns found in the uploaded file.")
    return numeric_cols


def calculate_key_metrics(df, selected_column):
    """
    Calculate key metrics from the DataFrame.
    Returns: Total Records, Total Sum, Average Value for selected column.
    """
    total_records = len(df)
    total_sum = df[selected_column].sum()
    average_value = df[selected_column].mean()
    
    return {
        'total_records': total_records,
        'total_sum': total_sum,
        'average_value': average_value,
        'primary_column': selected_column
    }


def generate_bar_chart(df, x_axis_col, y_axis_col, numeric_cols):
    """
    Generate a bar chart showing top entries by value.
    Uses selected column for X-axis labels and Y-axis values.
    """
    primary_col = y_axis_col
    
    # Limit to max 100 rows
    max_rows = min(100, len(df))
    top_data = df.nlargest(max_rows, primary_col)
    
    # Get labels from X-axis column
    labels = top_data[x_axis_col].astype(str).tolist()
    
    # Calculate dynamic figure size based on number of entries
    fig_height = min(6 + (max_rows / 20), 12)
    fig, ax = plt.subplots(figsize=(12, fig_height))
    
    # Use different colors for bars
    colors = ['#059669', '#0EA5E9', '#8B5CF6', '#F59E0B', '#EC4899']
    
    if len(numeric_cols) > 1:
        # Grouped bar chart for multiple columns
        x = range(len(top_data))
        width = 0.8 / len(numeric_cols)
        
        for i, col in enumerate(numeric_cols[:5]):  # Max 5 columns
            values = [float(top_data[col].iloc[j]) for j in range(len(top_data))]
            ax.bar([xi + i * width for xi in x], values, width, label=col, color=colors[i % len(colors)])
        
        ax.set_xticks([xi + width * (len(numeric_cols[:5]) - 1) / 2 for xi in x])
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
        ax.legend(loc='upper right', fontsize=8)
    else:
        # Single column bar chart
        values = top_data[primary_col].values
        ax.bar(range(len(top_data)), values, color='#059669', edgecolor='#047857')
        ax.set_xticks(range(len(top_data)))
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
    
    ax.set_xlabel(x_axis_col)
    ax.set_ylabel(y_axis_col)
    ax.set_title(f'{x_axis_col} by {y_axis_col} ({len(top_data)} entries)', color='#1E3A5F', fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3)
    
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf


class PDFReport(FPDF):
    """Custom PDF Report Generator using FPDF."""
    
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(30, 58, 95)
        self.cell(0, 10, 'GridToDash Professional Report', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-20)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'Generated by GridToDash - Professional Automation', 0, 0, 'C')


def create_pdf(df, metrics, chart_buf, filename):
    """
    Create a PDF report with header, metrics, chart, and data table.
    """
    total_rows = len(df)
    pdf = PDFReport()
    pdf.add_page()
    
    # Current Date
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, f'Report Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'R')
    pdf.ln(5)
    
    # Key Metrics Section
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(30, 58, 95)
    pdf.cell(0, 10, 'Key Metrics', 0, 1, 'L')
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(60, 8, f"Total Records: {metrics['total_records']}", 0, 0, 'L')
    pdf.cell(60, 8, f"Total Sum: {metrics['total_sum']:,.2f}", 0, 0, 'L')
    pdf.cell(60, 8, f"Average Value: {metrics['average_value']:,.2f}", 0, 1, 'L')
    pdf.ln(10)
    
    # All Columns Info
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(30, 58, 95)
    all_cols = df.columns.tolist()
    pdf.cell(0, 8, f"Columns in data: {', '.join(all_cols)}", 0, 1, 'L')
    pdf.ln(5)
    
    # Chart Section
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(30, 58, 95)
    pdf.cell(0, 10, f'Chart ({min(total_rows, 100)} Entries)', 0, 1, 'L')
    pdf.ln(5)
    
    chart_path = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    chart_path.write(chart_buf.getvalue())
    chart_path.close()
    pdf.image(chart_path.name, x=10, w=190)
    os.unlink(chart_path.name)
    pdf.ln(10)
    
    # Data Table Section
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(30, 58, 95)
    pdf.cell(0, 10, f'Data Preview (First {min(total_rows, 100)} Rows)', 0, 1, 'L')
    pdf.ln(5)
    
    # Table Header
    pdf.set_font('Arial', 'B', 7)
    pdf.set_fill_color(30, 58, 95)
    pdf.set_text_color(255, 255, 255)
    
    columns = df.columns.tolist()
    num_cols = len(columns)
    
    # Calculate column width - dynamic based on number of columns
    max_width = 195
    col_width = min(22, max_width / num_cols)
    
    # Print header
    for col in columns:
        pdf.cell(col_width, 7, str(col)[:10], 1, 0, 'C', True)
    pdf.ln()
    
    # Table Rows
    pdf.set_font('Arial', '', 7)
    pdf.set_text_color(0, 0, 0)
    
    # Show up to 20 rows for better data preview
    for idx, row in df.head(100).iterrows():
        for col in columns:
            cell_value = str(row[col])[:12]
            pdf.cell(col_width, 6, cell_value, 1, 0, 'C')
        pdf.ln()
    
    # Footer
    pdf.set_y(-25)
    pdf.set_font('Arial', 'I', 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, 'Generated by GridToDash - Professional Automation', 0, 0, 'C')
    
    return pdf.output(dest='S').encode('latin-1')


def main():
    """Main application entry point."""
    
    # Handle language from query params - read and process
    try:
        # Get query params as dict
        qp = st.query_params.to_dict()
        if "lang" in qp:
            lang = qp["lang"]
            if lang in ("pt", "en"):
                st.session_state.language = lang
    except Exception:
        pass
    
    # Check authentication - show login if not authenticated
    if not st.session_state.get("authenticated"):
        show_login()
        return
    
    # Show logout button in main area
    st.markdown(f"""
    <div style="position: fixed; top: 10px; right: 10px; z-index: 1000;">
        <span style="background: #1E3A5F; color: white; padding: 8px 16px; border-radius: 8px; font-size: 14px;">
            {st.session_state.user_email}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        col_logo1, col_logo2, col_logo3 = st.columns([1,2,1])
        with col_logo2:
            st.image("logo.png", width=150)
        st.markdown('<p style="text-align: center; font-size: 1.3rem; font-weight: bold; color: white; margin-top: 0px;">GridToDash</p>', unsafe_allow_html=True)
        
        # Language Toggle
        st.markdown("### Language / Idioma")
        col_lang1, col_lang2 = st.columns(2)
        with col_lang1:
            if st.button("PT", use_container_width=True, type="primary" if st.session_state.language == "pt" else "secondary"):
                st.session_state.language = "pt"
                st.rerun()
        with col_lang2:
            if st.button("EN", use_container_width=True, type="primary" if st.session_state.language == "en" else "secondary"):
                st.session_state.language = "en"
                st.rerun()
        
        st.markdown("---")
        st.markdown(f"### {get_translation('about')}")
        st.markdown(get_translation("sidebar_about_text"))
        st.markdown("---")
        
        # Logout button
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_email = None
            st.rerun()
        
        st.markdown(f"*{get_translation('sidebar_built_with')}*")
    
    # Main Content
    st.markdown(f"""
    <div class="hero-section">
        <h1 class="main-title">{get_translation('hero_title')}</h1>
        <p style="font-size: 1.2rem; color: #64748B; margin-top: 10px;">
            {get_translation('hero_subtitle')}
        </p>
        <p style="color: #94A3B8; margin-top: 8px;">
            {get_translation('hero_description')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # File Uploader - Native Streamlit with JS translation
    uploaded_file = st.file_uploader(
        get_translation("file_uploader"),
        type=['xlsx', 'csv'],
        help=get_translation("file_uploader_help")
    )
    
    if uploaded_file is not None:
        try:
            # Load and process data
            with st.spinner(get_translation('processing')):
                df = load_data(uploaded_file)
                numeric_cols = identify_numeric_columns(df)
            
            # Initialize selected column in session state if not set or if columns changed
            if 'selected_column' not in st.session_state or st.session_state.get('numeric_cols') != numeric_cols:
                st.session_state.selected_column = numeric_cols[0] if numeric_cols else None
                st.session_state.numeric_cols = numeric_cols
            
            # Column selector for metrics
            selected_col = st.selectbox(
                get_translation("select_column"),
                options=numeric_cols,
                index=numeric_cols.index(st.session_state.selected_column) if st.session_state.selected_column in numeric_cols else 0,
                key="column_selector"
            )
            st.session_state.selected_column = selected_col
            
            # X-axis and Y-axis selectors
            col_x, col_y = st.columns(2)
            with col_x:
                all_cols = df.columns.tolist()
                x_axis_col = st.selectbox(
                    get_translation("select_x_axis"),
                    options=all_cols,
                    index=0,
                    key="x_axis_selector"
                )
            with col_y:
                y_axis_col = st.selectbox(
                    get_translation("select_y_axis"),
                    options=numeric_cols,
                    index=numeric_cols.index(selected_col) if selected_col in numeric_cols else 0,
                    key="y_axis_selector"
                )
            
            # Columns selector for PDF
            pdf_columns = st.multiselect(
                get_translation("select_columns_pdf"),
                options=all_cols,
                default=all_cols,
                key="pdf_columns_selector"
            )
            
            # Calculate metrics for selected column
            metrics = calculate_key_metrics(df, selected_col)
            
            # Display Key Metrics
            st.markdown(f'<p class="section-header">{get_translation("key_metrics")}</p>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="metric-card" style="animation-delay: 0.1s;">
                    <h3>{get_translation("total_records")}</h3>
                    <p class="value navy">{metrics['total_records']:,}</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="metric-card" style="animation-delay: 0.2s;">
                    <h3>{get_translation("total_sum")} ({selected_col})</h3>
                    <p class="value green">{metrics['total_sum']:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="metric-card" style="animation-delay: 0.3s;">
                    <h3>{get_translation("average_value")} ({selected_col})</h3>
                    <p class="value blue">{metrics['average_value']:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Display Data Preview
            st.markdown(f'<p class="section-header" style="margin-top: 30px;">{get_translation("data_preview")}</p>', unsafe_allow_html=True)
            st.dataframe(df[pdf_columns].head(10), use_container_width=True)
            
            # Get numeric columns from selected PDF columns for chart
            chart_numeric_cols = [col for col in pdf_columns if col in numeric_cols] if pdf_columns else numeric_cols
            
            # Generate Chart
            st.markdown(f'<p class="section-header">{get_translation("chart_title")}</p>', unsafe_allow_html=True)
            chart_buf = generate_bar_chart(df, x_axis_col, y_axis_col, chart_numeric_cols if chart_numeric_cols else numeric_cols)
            st.image(chart_buf, use_container_width=True)
            
            # Generate PDF Button
            if st.button(get_translation("generate_pdf")):
                with st.spinner(get_translation('generating_pdf')):
                    # Create PDF with selected columns
                    df_pdf = df[pdf_columns] if pdf_columns else df
                    pdf_bytes = create_pdf(df_pdf, metrics, chart_buf, uploaded_file.name)
                    
                    # Success Message
                    st.markdown(f"""
                    <div class="success-message">
                        <strong>{get_translation("success_message")}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Download Button
                    pdf_filename = f"GridToDash_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    st.download_button(
                        label=get_translation("download_pdf"),
                        data=pdf_bytes,
                        file_name=pdf_filename,
                        mime="application/pdf",
                        type="primary"
                    )
        
        except ValueError as e:
            error_msg = get_translation("error_loading") + str(e)
            if "empty" in str(e).lower():
                error_msg = get_translation("error_empty_file")
            elif "numeric" in str(e).lower():
                error_msg = get_translation("error_no_numeric")
            st.error(error_msg)
        except Exception as e:
            st.error(get_translation("error_unexpected") + str(e))


if __name__ == "__main__":
    main()
