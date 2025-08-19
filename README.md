# 🛒 Kirana Tap - AI Grocery Assistant

**Kirana Tap** is an AI-powered grocery ordering assistant that helps people (especially older adults) order groceries simply by chatting with a bot. The bot parses grocery lists and automates the ordering process on Blinkit with cash on delivery.

## 🎯 Problem We're Solving

Most people, especially our parents, struggle with quick commerce apps because the interface is confusing. Kirana Tap makes grocery ordering as simple as typing a message in natural language.

## 🏗️ Architecture

```
User Chat → AI Processing → Blinkit Automation → Order Placement
    ↓              ↓              ↓              ↓
Web Interface → Parse Items → Headless Browser → Cash on Delivery
```

## 🚀 Features

- **Natural Language Processing**: Just type your grocery list in plain English
- **AI-Powered Parsing**: Automatically extracts items, quantities, and units
- **Automated Ordering**: Places orders on Blinkit using headless browser automation
- **Cash on Delivery**: No payment integration complexity
- **Real-time Updates**: Live order status and progress tracking
- **Beautiful UI**: Modern, responsive chat interface

## 🛠️ Tech Stack

- **Backend**: Flask + Socket.IO (Python)
- **Frontend**: HTML5 + CSS3 + JavaScript (Vanilla)
- **AI**: OpenAI GPT-3.5 Turbo
- **Automation**: Selenium WebDriver (Chrome)
- **Real-time**: WebSocket communication

## 📋 Prerequisites

- Python 3.8+
- Chrome browser installed
- OpenAI API key
- Windows 10/11 (tested on Windows)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd "Kirana Tap 2"

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
copy env_template.txt .env

# Edit .env file and add your OpenAI API key
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Run the Application

```bash
# Start the server
python app.py
```

### 4. Access the Application

- **Main Interface**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

## 💬 How to Use

### 1. Start a Conversation
Open the web app and start chatting with the AI assistant.

### 2. Order Groceries
Simply type your grocery list in natural language:
```
"I need 2 kg potatoes, 1 dozen eggs, and 3 packets of bread"
"milk 1 liter, bananas 5 pieces, rice 2 kg"
"2 kg onions, 1 kg tomatoes, 500g ginger"
```

### 3. Confirm Order
The AI will parse your list and show a summary. Click "✅ Confirm Order" to proceed.

### 4. Automated Ordering
The system will automatically:
- Navigate to Blinkit
- Search for each item
- Add items to cart
- Select cash on delivery
- Place the order

### 5. Track Progress
Monitor real-time updates on your order status.

## 🔧 Configuration

### OpenAI API
- Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- Add it to your `.env` file

### Chrome Driver
- The app automatically downloads ChromeDriver using `webdriver-manager`
- Ensure Chrome browser is installed on your system

### Customization
- Modify `blinkit_automation.py` for different e-commerce sites
- Adjust AI prompts in `app.py` for different parsing requirements
- Customize UI in `templates/index.html`

## 📁 Project Structure

```
Kirana Tap 2/
├── app.py                 # Main Flask application
├── blinkit_automation.py  # Blinkit automation layer
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Chat interface
├── env_template.txt       # Environment variables template
└── README.md             # This file
```

## 🧪 Testing

### Test the Chat Interface
1. Start the application
2. Open http://localhost:5000
3. Type a grocery list
4. Verify AI parsing works
5. Test order confirmation flow

### Test Automation (Optional)
- The automation runs in headless mode
- Monitor console logs for automation progress
- Check for any Selenium errors

## 🚨 Important Notes

### Production Considerations
- **Security**: Add proper user authentication
- **Database**: Replace in-memory storage with a proper database
- **Error Handling**: Add comprehensive error handling and retry logic
- **Rate Limiting**: Implement API rate limiting for OpenAI calls
- **Logging**: Add proper logging and monitoring

### Limitations
- **Demo Purpose**: This is a white-label coding project
- **Blinkit Specific**: Currently only works with Blinkit
- **Location**: Uses default location (Delhi, India)
- **Payment**: Only supports cash on delivery

## 🐛 Troubleshooting

### Common Issues

1. **Chrome Driver Error**
   - Ensure Chrome browser is installed
   - Check if antivirus is blocking ChromeDriver

2. **OpenAI API Error**
   - Verify your API key is correct
   - Check if you have sufficient API credits

3. **Blinkit Automation Fails**
   - Website structure may have changed
   - Check console logs for specific errors
   - Verify internet connection

4. **Port Already in Use**
   - Change port in `app.py` or kill existing process
   - Use `netstat -ano | findstr :5000` to find process

## 🔮 Future Enhancements

- [ ] Support for multiple e-commerce platforms
- [ ] User accounts and order history
- [ ] Payment gateway integration
- [ ] Mobile app
- [ ] Voice input support
- [ ] Multi-language support
- [ ] Advanced AI features (recommendations, substitutions)

## 📞 Support

This is a demonstration project. For production use, consider:
- Adding proper error handling
- Implementing user management
- Adding monitoring and analytics
- Security hardening

## 📄 License

This project is for educational and demonstration purposes.

---

**Made with ❤️ for simplifying grocery shopping**
