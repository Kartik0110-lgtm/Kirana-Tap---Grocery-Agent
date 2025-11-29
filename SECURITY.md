# Security Guide for Kirana Tap

## Overview

This document outlines the security measures implemented in Kirana Tap and provides guidance for secure deployment and usage.

---

## Table of Contents

1. [Security Features Implemented](#security-features-implemented)
2. [Configuration Guide](#configuration-guide)
3. [Production Deployment Checklist](#production-deployment-checklist)
4. [Known Risks & Mitigations](#known-risks--mitigations)
5. [Security Best Practices](#security-best-practices)
6. [Incident Response](#incident-response)

---

## Security Features Implemented

### ✅ 1. Secure Secret Key Management
- **What**: Flask session encryption key
- **Implementation**: Uses `FLASK_SECRET_KEY` from environment variables
- **Fallback**: Generates random key with warning in development
- **Risk if compromised**: Session hijacking, unauthorized access

### ✅ 2. CORS (Cross-Origin Resource Sharing) Restrictions
- **What**: Controls which websites can access your API
- **Implementation**: Configurable via `CORS_ALLOWED_ORIGINS` environment variable
- **Default**: Only localhost in development
- **Production**: Must set to your actual domain(s)

### ✅ 3. Input Validation & Sanitization
- **What**: Prevents malicious input from crashing or exploiting the system
- **Implementation**:
  - Maximum message length (500 chars default)
  - Character whitelist (letters, numbers, basic punctuation)
  - Type checking (ensures strings are strings)
- **Protects against**: Code injection, buffer overflow, DoS attacks

### ✅ 4. Rate Limiting
- **What**: Prevents API abuse and spam
- **Implementation**: Per-session request limiting
- **Default**: 10 requests per 60 seconds
- **Configurable**: `RATE_LIMIT_REQUESTS` and `RATE_LIMIT_WINDOW`
- **Protects against**: DoS attacks, API cost exploitation

### ✅ 5. Session Management
- **What**: Tracks authenticated users
- **Implementation**:
  - Secure random session IDs (32-byte tokens)
  - IP address tracking
  - Automatic cleanup on disconnect
- **Protects against**: Session fixation, unauthorized access

### ✅ 6. Authentication System (Optional)
- **What**: Token-based authentication
- **Implementation**: Simple token validation via `AUTH_TOKEN`
- **When to enable**: Production environments
- **Future**: Should be replaced with OAuth2/JWT for multi-user systems

### ✅ 7. Secure Logging
- **What**: Logs events without exposing sensitive data
- **Implementation**:
  - No full user input in logs (only length/metadata)
  - No API keys or tokens in logs
  - Separate log levels for development vs production
- **Protects against**: Information leakage, privacy violations

### ✅ 8. HTTPS/SSL Support
- **What**: Encrypted communication
- **Implementation**: Optional SSL certificate loading
- **Production**: Usually handled by reverse proxy (Nginx, Render)
- **Protects against**: Man-in-the-middle attacks, data interception

---

## Configuration Guide

### Development Setup

1. **Copy environment template**:
   ```bash
   copy env_template.txt .env
   ```

2. **Set minimum required variables**:
   ```bash
   OPENAI_API_KEY=your_actual_api_key
   FLASK_SECRET_KEY=any_random_string_for_dev
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

### Production Setup

1. **Generate secure secret key**:
   ```bash
   python -c "import os; print(os.urandom(32).hex())"
   ```

2. **Generate auth token** (if enabling authentication):
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **Configure .env for production**:
   ```bash
   OPENAI_API_KEY=your_actual_api_key
   FLASK_SECRET_KEY=<generated_secret_from_step_1>
   FLASK_ENV=production
   FLASK_DEBUG=False
   CORS_ALLOWED_ORIGINS=https://yourdomain.com
   AUTH_ENABLED=true
   AUTH_TOKEN=<generated_token_from_step_2>
   RATE_LIMIT_REQUESTS=10
   RATE_LIMIT_WINDOW=60
   ```

4. **Deploy with HTTPS**:
   - **Option A**: Use platform with automatic HTTPS (Render, Heroku, Vercel)
   - **Option B**: Set up Nginx reverse proxy with Let's Encrypt SSL
   - **Option C**: Provide SSL certificate paths:
     ```bash
     SSL_CERT_PATH=/path/to/cert.pem
     SSL_KEY_PATH=/path/to/key.pem
     ```

---

## Production Deployment Checklist

### Critical (Must Do)

- [ ] Set unique `FLASK_SECRET_KEY` (never use default or commit to Git)
- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Configure `CORS_ALLOWED_ORIGINS` to your domain only
- [ ] Enable HTTPS/SSL (via reverse proxy or SSL certificates)
- [ ] Verify `.env` is in `.gitignore` (should already be there)
- [ ] Never commit `.env` or `chrome-profile/` to version control

### Recommended

- [ ] Enable authentication: `AUTH_ENABLED=true` and set `AUTH_TOKEN`
- [ ] Set appropriate rate limits for your use case
- [ ] Set up monitoring/alerting for errors
- [ ] Configure log rotation (logs can grow large)
- [ ] Set up backup system for chrome-profile directory
- [ ] Use a database for order persistence (instead of in-memory)
- [ ] Set OpenAI API spending limits in your OpenAI account
- [ ] Review and understand Blinkit's Terms of Service

### Optional (Nice to Have)

- [ ] Set up Redis for distributed rate limiting
- [ ] Implement proper user authentication (OAuth2/JWT)
- [ ] Add database for order history
- [ ] Set up CI/CD pipeline with security scanning
- [ ] Enable Content Security Policy (CSP) headers
- [ ] Implement request signing/verification
- [ ] Add IP whitelisting for admin functions

---

## Known Risks & Mitigations

### 🔴 HIGH RISK

#### 1. Chrome Profile Contains Login Credentials
- **Risk**: `chrome-profile/` directory contains Blinkit login cookies
- **Impact**: If stolen, attacker can access your Blinkit account
- **Mitigations**:
  - ✅ Excluded from Git via `.gitignore`
  - ⚠️ Set file permissions: `chmod 700 chrome-profile/` (Linux/Mac)
  - ⚠️ Consider encrypting the directory
  - ⚠️ Don't share server access with untrusted parties
  - ⚠️ Regular session rotation (log out and back in periodically)

#### 2. Automation Violates Blinkit Terms of Service
- **Risk**: Account ban or legal action
- **Impact**: Loss of access to Blinkit account
- **Mitigations**:
  - ⚠️ Use only for personal orders (not commercial)
  - ⚠️ Don't abuse with excessive orders
  - ⚠️ Contact Blinkit for official API access if doing commercial use
  - ℹ️ Consider this a proof-of-concept / learning project

#### 3. OpenAI API Key Exposure
- **Risk**: Unauthorized use, unexpected charges
- **Impact**: Financial loss
- **Mitigations**:
  - ✅ Stored in `.env` (not in code)
  - ✅ `.env` excluded from Git
  - ✅ Rate limiting reduces abuse potential
  - ⚠️ Set spending limits in OpenAI dashboard
  - ⚠️ Rotate keys periodically
  - ⚠️ Monitor API usage regularly

### 🟡 MEDIUM RISK

#### 4. In-Memory Order Storage
- **Risk**: Orders lost on server restart
- **Impact**: User confusion, lost orders
- **Mitigations**:
  - ⚠️ Implement database persistence (PostgreSQL/MongoDB)
  - ⚠️ For now: Warn users that orders may be lost on restart
  - ℹ️ Current implementation suitable for single-user dev use only

#### 5. No Multi-User Support
- **Risk**: Concurrent users interfere with each other
- **Impact**: Wrong orders, cart conflicts
- **Mitigations**:
  - ⚠️ Current design is single-user only
  - ⚠️ Use separate chrome-profile per user (requires significant refactoring)
  - ℹ️ Don't deploy for public use without proper multi-user architecture

#### 6. Simple Authentication System
- **Risk**: Token-based auth is basic, no user management
- **Impact**: Limited access control
- **Mitigations**:
  - ✅ Better than nothing for personal use
  - ⚠️ Implement proper OAuth2/JWT for production
  - ⚠️ Add user registration/login system
  - ℹ️ Current auth sufficient for single-user or trusted group use

### 🟢 LOW RISK

#### 7. Rate Limiting is In-Memory
- **Risk**: Limits reset on server restart
- **Impact**: Temporary bypass of rate limits
- **Mitigations**:
  - ⚠️ Use Redis for persistent rate limiting in production
  - ℹ️ Current implementation fine for development

---

## Security Best Practices

### For Developers

1. **Never commit secrets**:
   - Always check `.gitignore` includes `.env` and `chrome-profile/`
   - Before pushing: `git status` to verify no sensitive files staged

2. **Keep dependencies updated**:
   ```bash
   pip install --upgrade pip
   pip list --outdated
   pip install safety
   safety check
   ```

3. **Review logs regularly**:
   - Check `app.log` for suspicious activity
   - Monitor for rate limit violations
   - Watch for authentication failures

4. **Use environment-specific configs**:
   - Separate `.env.development` and `.env.production`
   - Never use production secrets in development

### For Deployers

1. **Use HTTPS everywhere**:
   - Free SSL certificates: Let's Encrypt
   - Platforms with auto-SSL: Render, Vercel, Netlify

2. **Restrict access**:
   - Use firewall rules to limit which IPs can access admin endpoints
   - Consider VPN for sensitive operations

3. **Monitor and alert**:
   - Set up uptime monitoring (UptimeRobot, Pingdom)
   - Configure alerts for errors
   - Track API usage and costs

4. **Regular backups**:
   - Backup `chrome-profile/` directory
   - Export `.env` securely (encrypted)
   - Test restore procedures

### For Users

1. **Protect your API keys**:
   - Never share your `.env` file
   - Don't screenshot or email API keys
   - Rotate keys if exposed

2. **Use strong authentication**:
   - Generate long, random `AUTH_TOKEN` (32+ characters)
   - Don't reuse passwords from other services

3. **Review orders before confirming**:
   - Always check the AI-parsed order summary
   - Verify quantities and items are correct

---

## Incident Response

### If API Key is Compromised

1. **Immediately**:
   - Revoke the key in OpenAI dashboard
   - Generate a new key
   - Update `.env` with new key
   - Restart the application

2. **Review**:
   - Check OpenAI usage logs for unauthorized requests
   - Review charges for unexpected costs
   - Contact OpenAI support if fraudulent charges

### If Server is Compromised

1. **Immediately**:
   - Shut down the server
   - Change all passwords and tokens
   - Revoke all API keys

2. **Investigate**:
   - Review server logs for unauthorized access
   - Check for modified files
   - Scan for malware

3. **Recover**:
   - Restore from clean backup
   - Update all dependencies
   - Apply security patches
   - Restart with new credentials

### If Blinkit Account is Compromised

1. **Immediately**:
   - Log out from all devices via Blinkit app
   - Change Blinkit password
   - Delete `chrome-profile/` directory
   - Re-login manually on next automation run

2. **Review**:
   - Check Blinkit order history for unauthorized orders
   - Contact Blinkit support if fraudulent orders
   - Review payment methods linked to account

---

## Security Roadmap (Future Improvements)

### Short Term
- [ ] Implement database for persistent storage
- [ ] Add request signing/verification
- [ ] Implement proper user authentication (OAuth2)
- [ ] Add Content Security Policy headers
- [ ] Set up automated security scanning in CI/CD

### Medium Term
- [ ] Multi-user support with isolated chrome profiles
- [ ] Encrypted chrome-profile storage
- [ ] Two-factor authentication
- [ ] Audit logging for all actions
- [ ] Role-based access control (RBAC)

### Long Term
- [ ] Official Blinkit API integration (if available)
- [ ] End-to-end encryption for sensitive data
- [ ] Compliance with data protection regulations (GDPR, etc.)
- [ ] Third-party security audit
- [ ] Bug bounty program

---

## Resources

### Security Tools
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Common web vulnerabilities
- [Let's Encrypt](https://letsencrypt.org/) - Free SSL certificates
- [Safety](https://github.com/pyupio/safety) - Python dependency checker
- [Bandit](https://github.com/PyCQA/bandit) - Python security linter

### Learning Resources
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

### Reporting Security Issues
If you discover a security vulnerability in Kirana Tap:
1. **DO NOT** create a public GitHub issue
2. Email the maintainer directly (if this was a public project)
3. Provide detailed description and steps to reproduce
4. Allow time for fix before public disclosure

---

## Conclusion

Security is an ongoing process, not a one-time setup. Regularly review this document, update dependencies, and stay informed about new vulnerabilities.

**Remember**: This application is designed for personal use and learning. For commercial use, consult security professionals and ensure compliance with all applicable laws and terms of service.

---

**Last Updated**: 2024-01-15
**Version**: 1.0
**Maintained By**: Kirana Tap Security Team
