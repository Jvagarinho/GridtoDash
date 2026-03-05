# GridToDash - Excel to PDF Automated Reporter

![GridToDash Logo](logo.png)

**GridToDash** is a professional Streamlit application that transforms Excel/CSV files into polished, branded PDF reports instantly. Perfect for small business owners who need quick, professional reports without any design experience.

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

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- MongoDB database (MongoDB Atlas recommended - free cloud)

### 📦 Installation

1. **Clone the Repository**

```bash
git clone https://github.com/Jvagarinho/GridToDash.git
cd GridToDash
```

1. **Create Virtual Environment (Recommended)**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 🗄️ Database Configuration

#### Option A: MongoDB Atlas (Cloud - FREE & Recommended)

1. **Create Account**: Go to <https://www.mongodb.com/cloud/atlas/register>
2. **Create Cluster**: Click "Build a Cluster", choose FREE (M0), name it `gridtodash`
3. **Create Database User**:
   - Go to "Database Access" → "Add New Database User"
   - Username: `gridtodash`
   - Password: Choose a strong password
   - Privileges: `Read and write to any database`
4. **Configure Network Access**:
   - Go to "Network Access" → "Add IP Address"
   - Click "Allow Access from Anywhere" (for testing)
   - Or add your specific IP address
5. **Get Connection String**:
   - Go to "Database" → Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<username>` with `gridtodash`
   - Replace `<password>` with your password

6. **Configure secrets.toml**:

```toml
MONGODB_URI = "mongodb+srv://gridtodash:YOUR_PASSWORD@gridtodash.xxxxx.mongodb.net/gridtodash?retryWrites=true&w=majority"
MONGODB_DB = "gridtodash"
```

#### Option B: Local MongoDB (if installed)

```toml
MONGODB_URI = "mongodb://localhost:27017"
MONGODB_DB = "gridtodash"
```

#### Option C: Development Mode (No MongoDB)

For testing without a database, leave `MONGODB_URI` empty:

```toml
MONGODB_URI = ""
MONGODB_DB = "gridtodash"
```

This uses local file storage (`.dev_users.json`) for development.

### 🎯 Run the Application

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`

### 🔄 Migrate Development Data to MongoDB

If you've been using development mode and want to migrate users to MongoDB:

1. Configure `MONGODB_URI` in `.streamlit/secrets.toml`
2. Run the migration script:

```bash
streamlit run migrate_users.py
```

This will transfer all users from `.dev_users.json` to your MongoDB database.

## Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Visit <https://share.streamlit.io>
3. Select your repository and branch
4. Click "Deploy"
5. Add your secrets in the settings:
   - `MONGODB_URI` - Your MongoDB connection string
   - `MONGODB_DB` - Your database name

## Project Structure

```text
GridToDash/
├── app.py              # Main application
├── login.py            # Authentication module
├── requirements.txt    # Python dependencies
├── logo.png            # Application logo
├── .streamlit/         # Streamlit configuration
├── .gitignore          # Git ignore patterns
├── migrate_users.py    # Migration script (optional)
└── README.md           # Documentation
```

## Technology Stack

| Category          | Technology                          |
|-------------------|-------------------------------------|
| Frontend          | Streamlit                           |
| Database          | MongoDB                             |
| Data Processing   | Pandas, OpenPyXL                    |
| Charts            | Matplotlib                          |
| PDF Generation    | FPDF                                |
| Styling           | Custom CSS                          |

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

| Product   | Sales | Stock | Seller |
|-----------|-------|-------|--------|
| Product A | 1000  | 50    | John   |
| Product B | 2500  | 30    | Mary   |

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

Made with ❤️ by IterioTech
