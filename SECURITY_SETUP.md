# Quick Security Setup Guide

## 🚨 IMPORTANT: Read This First!

Your Kirana Tap application has been updated with security improvements. Follow these steps to configure it properly.

---

## Step 1: Update Your .env File

Your current `.env` file needs new security variables. Here's what to do:

### Option A: Start Fresh (Recommended)

1. **Backup your current API key**:
   - Open your existing `.env` file
   - Copy the `OPENAI_API_KEY` value somewhere safe

2. **Delete old .env**:
   ```bash
   del .env
   ```

3. **Copy the new template**:
   ```bash
   copy env_template.txt .env
   ```

4. **Edit .env** and set at minimum:
   ```bash
   OPENAI_API_KEY=<your_openai_api_key_from_step_1>
   FLASK_SECRET_KEY=<generate_using_command_below>
   ```

5. **Generate a secure secret key**:
   ```bash
   python -c "import os; print(os.urandom(32).hex())"
   ```
   Copy the output and paste it as `FLASK_SECRET_KEY` value

### Option B: Update Existing .env

Add these new lines to your existing `.env` file:

```bash
# Add these new security variables:
FLASK_SECRET_KEY=<run: python -c "import os; print(os.urandom(32).hex())">
CORS_ALLOWED_ORIGINS=http://localhost:5000,http://127.0.0.1:5000
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60
MAX_MESSAGE_LENGTH=500
AUTH_ENABLED=false
AUTH_TOKEN=
```

---

## Step 2: Install New Dependencies

The security updates require a new package:

```bash
pip install cryptography==41.0.7
```

Or reinstall all dependencies:

```bash
pip install -r requirements.txt
```

---

## Step 3: Test the Application

1. **Start the server**:
   ```bash
   python app.py
   ```

2. **Look for security warnings**:
   - You should see: "🛠️ Development mode enabled"
   - You should see: "⚠️ Not for production use - enable security features in .env"
   - You should see rate limiting and other security features listed

3. **Test basic functionality**:
   - Open: http://localhost:5000
   - Try placing a test order
   - Verify everything works

---

## Step 4: Verify Security Settings

### Check 1: .gitignore Protection

Run this command to ensure `.env` won't be committed:

```bash
git status
```

**✅ Good**: `.env` should NOT appear in the list of changes
**❌ Bad**: If you see `.env` in red, run: `git reset .env`

### Check 2: Secret Key

Run this to verify your secret key is set:

```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Secret key set!' if os.getenv('FLASK_SECRET_KEY') else 'WARNING: No secret key!')"
```

### Check 3: CORS Configuration

Your app should only allow connections from localhost in development.

---

## Step 5: Understand What Changed

### What's New:

✅ **Secure Secret Keys**: No more hardcoded secrets in code
✅ **CORS Protection**: Only allowed origins can connect
✅ **Input Validation**: Prevents malicious input
✅ **Rate Limiting**: Prevents API abuse (10 requests per minute)
✅ **Better Logging**: No sensitive data in logs
✅ **Session Management**: Tracks connections securely
✅ **Optional Authentication**: Can enable token-based auth

### What's Different for You:

**Before**: Just worked with default settings
**Now**: Requires `.env` configuration (more secure!)

**Before**: Any website could connect
**Now**: Only your specified origins allowed

**Before**: No protection against spam
**Now**: Rate limiting prevents abuse

---

## For Production Deployment

If you want to deploy this publicly:

1. **Read SECURITY.md** - Complete security guide
2. **Enable authentication**:
   ```bash
   AUTH_ENABLED=true
   AUTH_TOKEN=<run: python -c "import secrets; print(secrets.token_urlsafe(32))">
   ```
3. **Set production environment**:
   ```bash
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```
4. **Update CORS to your domain**:
   ```bash
   CORS_ALLOWED_ORIGINS=https://yourdomain.com
   ```
5. **Deploy on platform with HTTPS** (Render, Heroku, etc.)

---

## Troubleshooting

### Error: "FLASK_SECRET_KEY not set"

**Solution**: Generate and set it in `.env`:
```bash
python -c "import os; print(os.urandom(32).hex())"
```
Add to `.env`: `FLASK_SECRET_KEY=<output_from_above>`

### Error: "ModuleNotFoundError: No module named 'cryptography'"

**Solution**: Install new dependency:
```bash
pip install cryptography==41.0.7
```

### Warning: "Using randomly generated SECRET_KEY"

**Solution**: This is OK for development, but set a permanent one in `.env` for production.

### Error: "Rate limit exceeded"

**Solution**: Wait 60 seconds, or increase limits in `.env`:
```bash
RATE_LIMIT_REQUESTS=20
RATE_LIMIT_WINDOW=60
```

---

## Quick Reference

### Essential .env Variables:
```bash
OPENAI_API_KEY=sk-...                    # REQUIRED
FLASK_SECRET_KEY=<64-char-hex-string>    # REQUIRED
CORS_ALLOWED_ORIGINS=http://localhost:5000  # REQUIRED
```

### Generate Secrets:
```bash
# Secret Key
python -c "import os; print(os.urandom(32).hex())"

# Auth Token (if enabling AUTH_ENABLED=true)
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Default Security Settings:
- Rate Limit: 10 requests per 60 seconds
- Max Message: 500 characters
- Authentication: Disabled (for development)
- CORS: Localhost only

---

## Need Help?

1. **Check SECURITY.md** for detailed documentation
2. **Review env_template.txt** for all available options
3. **Check app.log** for error messages
4. **Ensure all environment variables are set correctly**

---

**Your application is now more secure! 🔒**

For development use, you're all set. For production, read SECURITY.md for the full checklist.
