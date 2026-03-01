# GridToDash - Excel to PDF Automated Reporter

<p align="center">
  <img src="logo.png" alt="GridToDash Logo" width="200"/>
</p>

<p align="center">
  <a href="https://gridtodash.streamlit.app">
    <img src="https://img.shields.io/badge/Live Demo-6-green" alt="Live Demo">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python 3.10+">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Streamlit-1.28%2B-red" alt="Streamlit 1.28+">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
  </a>
</p>

---

GridToDash is a professional Streamlit application that transforms Excel/CSV files into polished, branded PDF reports instantly. Perfect for small business owners who need quick, professional reports without any design experience.

## Features

- **Secure Authentication** - User login and registration system with MongoDB
- **File Upload** - Supports Excel (.xlsx) and CSV files
- **Smart Column Selection** - Choose which numeric column to use for metrics calculation
- **Interactive Charts** - Dynamic bar chart with multi-column support
- **PDF Generation** - Automatic professional PDF report creation
- **Bilingual Support** - Full Portuguese and English translations
- **Modern Design** - Beautiful interface with animations and boutique styling
- **Fully Responsive** - Works seamlessly on desktop and mobile devices

## Screenshots

### Main Interface
> The interface displays the logo, language selector, file uploader, column selectors for metrics and charts, PDF column selection, metrics display, chart visualization, and data table.

### Generated PDF Report
> The PDF includes key metrics, bar charts, and a formatted table with your selected data.

## Quick Start

### Prerequisites

- Python 3.10 or higher
- MongoDB database (local or Atlas)

### Installation

1. **Clone the Repository**

```bash
git clone https://github.com/Jvagarinho/GridToDash.git
cd GridToDash
```

2. **Create Virtual Environment (Recommended)**

```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure Database**

Create a `.streamlit/secrets.toml` file:

```toml
MONGODB_URI = "your connection details"
MONGODB_DB = "gridtodash"
```

5. **Run the Application**

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Select your repository and branch
4. Click "Deploy"
5. Add your secrets in the settings:
   - `MONGODB_URI` - Your MongoDB connection string
   - `MONGODB_DB` - Your database name

## Project Structure

```
GridToDash/
├── app.py              # Main application
├── login.py            # Authentication module
├── requirements.txt    # Python dependencies
├── logo.png           # Application logo
├── convex/            # Convex functions (optional)
├── .streamlit/        # Streamlit configuration
├── .gitignore         # Git ignore patterns
└── README.md          # Documentation
```

## Technology Stack

| Category | Technology |
|----------|------------|
| Frontend | Streamlit |
| Database | MongoDB |
| Data Processing | Pandas, OpenPyXL |
| Charts | Matplotlib |
| PDF Generation | FPDF |
| Styling | Custom CSS |

## How to Use

1. **Create an Account** - Use the registration form
2. **Sign In** - Enter your credentials
3. **Select Language** - Use PT/EN buttons in the sidebar
4. **Upload File** - Drag or select an Excel or CSV file
5. **Choose Metrics Column** - Select which numeric column for Total Sum and Average
6. **Choose X Axis** - Select which column for chart labels
7. **Choose Y Axis** - Select which column for chart values
8. **Select PDF Columns** - Choose columns to include in the report
9. **View Data** - See metrics, chart, and data table
10. **Generate PDF** - Click "Generate PDF Report"
11. **Download** - Get your professional report

## Input File Format

Your Excel/CSV file should contain:
- At least one numeric column for metrics calculation
- Text columns for table and chart display

Example:

| Product | Sales | Stock | Seller |
|---------|-------|-------|--------|
| Product A | 1000 | 50 | John |
| Product B | 2500 | 30 | Mary |

## Security Notes

- Passwords are hashed using SHA-256 before storage
- MongoDB connection uses secure URI
- Credentials are stored only in environment variables/secrets
- Never expose your credentials in source code
- Minimum 6 characters required for passwords

## Troubleshooting

### MongoDB Connection Error
- Verify `MONGODB_URI` environment variable is correctly configured
- Confirm your IP is whitelisted in MongoDB Atlas

### Application Won't Start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using Python 3.10 or higher

### PDF Generation Error
- Ensure your Excel/CSV file has at least one numeric column
- Verify the file is not corrupted

## Supported Languages

- 🇵🇹 Portuguese
- 🇬🇧 English

## License

MIT License - See [LICENSE](LICENSE) for details

## Author

Developed by **IterioTech**

---

<p align="center">
  Made with ❤️ by IterioTech
</p>
