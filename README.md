# Kirana Tap - AI Grocery Assistant

An intelligent grocery ordering assistant that automates the process of ordering groceries from Blinkit using AI-powered natural language processing and Selenium automation.

## 🚨 **SECURITY WARNING - READ FIRST!**

**⚠️ CRITICAL: This project contains sensitive data that must be secured:**

1. **API Keys**: Never commit your `.env` file containing API keys
2. **Chrome Profile**: Contains personal browser data, login credentials, and cookies
3. **Personal Data**: May contain browsing history and autofill information

**🔒 Security Measures Implemented:**
- `.env` file is excluded from git tracking
- `chrome-profile/` directory is excluded from git tracking
- Environment template provided for safe setup

## 🛡️ **Setup & Security Instructions**

### 1. **Environment Setup (REQUIRED)**
```bash
# Copy the environment template
cp env_template.txt .env

# Edit .env with your actual API keys
# NEVER commit this file!
```

### 2. **Chrome Profile Security**
- The `chrome-profile/` directory contains your personal browser data
- This directory is automatically excluded from git
- **DO NOT** manually add it to version control
- Keep this directory local only

### 3. **API Key Security**
- Your OpenAI API key is stored in `.env`
- This file is automatically excluded from git
- **NEVER** share or commit your `.env` file
- Use `env_template.txt` as a reference

## 🚀 Features

- **AI-Powered Parsing**: Natural language grocery list processing via OpenAI API
- **Automated Ordering**: Selenium-based automation for Blinkit orders
- **Persistent Login**: Chrome profile management for seamless authentication
- **Real-time Updates**: Socket.IO-powered live order status updates
- **Smart Deduplication**: Intelligent duplicate item detection
- **Professional UI**: Modern, responsive chat interface

## 📋 Prerequisites

- Python 3.8+
- Chrome browser
- OpenAI API key
- Blinkit account

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/Kartik0110-lgtm/Kirana-Tap---AI-Grocery-Assistant.git
cd Kirana-Tap---AI-Grocery-Assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Copy and edit the environment template
cp env_template.txt .env
# Edit .env with your actual API keys
```

4. **Run the application**
```bash
python app.py
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `FLASK_ENV`: Flask environment (development/production)
- `FLASK_DEBUG`: Enable/disable debug mode
- `PORT`: Custom port number (optional)

### Chrome Profile
- Located in `chrome-profile/` directory
- Contains persistent login sessions
- Automatically excluded from version control
- **Keep this directory secure and local**

## 📁 Project Structure

```
Kirana Tap 2/
├── app.py                          # Flask web application
├── blinkit_automation_clean.py    # Primary automation script
├── blinkit_automation.py          # Alternative automation script
├── templates/                     # HTML templates
│   └── index.html               # Main chat interface
├── requirements.txt               # Python dependencies
├── env_template.txt              # Environment variables template
├── README.md                     # This file
├── .gitignore                    # Git exclusions (includes security rules)
└── chrome-profile/               # Chrome profile (EXCLUDED from git)
```

## 🚀 Usage

1. **Start the application**: `python app.py`
2. **Open your browser**: Navigate to `http://localhost:5000`
3. **Type your grocery list**: Use natural language (e.g., "I need 2 packets of milk and 1 kg rice")
4. **Confirm order**: Review the parsed items and confirm
5. **Watch automation**: The system automatically orders from Blinkit

## 🔒 Security Best Practices

1. **Never commit sensitive files**:
   - `.env` (contains API keys)
   - `chrome-profile/` (contains personal data)

2. **Use environment templates**:
   - Copy `env_template.txt` to `.env`
   - Fill in your actual values
   - Keep `.env` local only

3. **Regular security checks**:
   - Verify `.gitignore` excludes sensitive files
   - Check git status before commits
   - Review what's being tracked

## 🐛 Troubleshooting

### Common Issues
1. **API Key Errors**: Ensure `.env` file exists and contains valid API key
2. **Chrome Profile Issues**: Verify `chrome-profile/` directory exists locally
3. **Automation Failures**: Check internet connection and Blinkit availability

### Security Issues
1. **Sensitive Data in Git**: Use `git rm --cached <file>` to remove tracked sensitive files
2. **API Key Exposure**: Immediately rotate exposed API keys
3. **Profile Data Leak**: Check `.gitignore` and remove any tracked sensitive directories

## 📝 Contributing

1. **Security First**: Never commit sensitive data
2. **Use Templates**: Always use provided templates for configuration
3. **Test Locally**: Ensure changes work without exposing sensitive information

## 📄 License

This project is for educational and personal use. Please respect the security measures and never expose sensitive data.

## 🆘 Support

If you encounter security issues:
1. **Immediately** rotate any exposed API keys
2. **Check** what data has been committed
3. **Review** your `.gitignore` configuration
4. **Contact** the maintainer for assistance

---

**⚠️ Remember: Security is everyone's responsibility. Always verify what you're committing to version control!**
