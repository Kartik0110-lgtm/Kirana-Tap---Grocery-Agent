#!/usr/bin/env python3
"""
Startup script for Kirana Tap - Production Ready
"""

import os
from app import app, socketio

if __name__ == '__main__':
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get('PORT', 5000))
    
    # Use production settings
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    
    print(f"🚀 Starting Kirana Tap Backend on port {port}...")
    print(f"📍 Health check available at: http://localhost:{port}/health")
    print(f"🌐 Chat interface at: http://localhost:{port}/")
    print(f"🔧 Debug mode: {debug_mode}")
    
    # Start the application
    socketio.run(app, debug=debug_mode, host='0.0.0.0', port=port)
