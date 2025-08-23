from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import os
from dotenv import load_dotenv
import openai
import json
import re
from blinkit_automation_clean import BlinkitAutomation
import threading

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kirana-tap-secret-key-2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

# Store pending orders (in production, use a proper database)
pending_orders = {}

def parse_grocery_list(user_message):
    """
    Parse user's grocery list using AI to extract structured items
    """
    try:
        # Create a system prompt for grocery parsing
        system_prompt = """You are a grocery assistant. Parse the user's grocery list into structured items.
        Return ONLY a JSON array with objects containing: name, quantity, unit, category.
        
        IMPORTANT: The 'name' field should be the search term for the grocery store, without quantity/unit.
        
        Examples:
        - "I need 2 kg potatoes, 1 dozen eggs, and 3 packets of bread"
        - Output: [{"name": "potatoes", "quantity": 2, "unit": "kg", "category": "vegetables"}, {"name": "eggs", "quantity": 1, "unit": "dozen", "category": "dairy"}, {"name": "bread", "quantity": 3, "unit": "packets", "category": "bakery"}]
        
        - "milk 1 liter, bananas 5 pieces, rice 2 kg"
        - Output: [{"name": "milk", "quantity": 1, "unit": "liter", "category": "dairy"}, {"name": "bananas", "quantity": 5, "unit": "pieces", "category": "fruits"}, {"name": "rice", "quantity": 2, "unit": "kg", "category": "grains"}]
        
        - "one packet amul toned milk"
        - Output: [{"name": "amul toned milk", "quantity": 1, "unit": "packet", "category": "dairy"}]
        
        - "2 kg onions, 1 kg tomatoes"
        - Output: [{"name": "onions", "quantity": 2, "unit": "kg", "category": "vegetables"}, {"name": "tomatoes", "quantity": 1, "unit": "kg", "category": "vegetables"}]
        
        - "three packets heritage milk"
        - Output: [{"name": "heritage milk", "quantity": 3, "unit": "packets", "category": "dairy"}]
        
        Keep categories simple: vegetables, fruits, dairy, grains, bakery, snacks, beverages, household, personal_care
        
        Handle simple formats like "one packet milk" or "2 kg potatoes" correctly.
        
        The 'name' field should be clean and searchable (e.g., "amul toned milk" not "one packet amul toned milk")."""
        
        # Get AI response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.1
        )
        
        # Extract and parse JSON response
        ai_response = response.choices[0].message.content.strip()
        
        # Clean the response to extract just the JSON
        json_match = re.search(r'\[.*\]', ai_response, re.DOTALL)
        if json_match:
            grocery_items = json.loads(json_match.group())
            return grocery_items
        else:
            # Fallback parsing for simple cases
            return fallback_parsing(user_message)
            
    except Exception as e:
        print(f"AI parsing error: {e}")
        return fallback_parsing(user_message)

def fallback_parsing(user_message):
    """
    Simple fallback parsing when AI fails
    """
    items = []
    # Basic pattern matching for common formats
    patterns = [
        # "one packet amul toned milk" or "1 packet milk"
        r'(one|two|three|four|five|six|seven|eight|nine|ten)\s+(packet|packets|kg|g|liter|liters|piece|pieces|dozen)\s+([a-zA-Z\s]+)',
        r'(\d+)\s*(packet|packets|kg|g|liters?|pieces?|dozen)\s+of?\s+([a-zA-Z\s]+)',
        r'(\d+)\s+([a-zA-Z\s]+)\s+(\d+)\s*(packet|packets|kg|g|liters?|pieces?|dozen)',
        r'(\d+)\s+([a-zA-Z\s]+)',
        # Handle "one milk" format
        r'(one|two|three|four|five|six|seven|eight|nine|ten)\s+([a-zA-Z\s]+)'
    ]
    
    # Convert word numbers to digits
    word_to_num = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
    }
    
    for pattern in patterns:
        matches = re.findall(pattern, user_message, re.IGNORECASE)
        for match in matches:
            if len(match) == 3:
                if match[0].lower() in word_to_num:
                    # Handle "one packet milk" format
                    quantity = word_to_num[match[0].lower()]
                    unit = match[1].lower()
                    name = match[2].strip().lower()
                else:
                    # Handle "1 packet milk" format
                    quantity = int(match[0])
                    unit = match[1].lower()
                    name = match[2].strip().lower()
                
                items.append({
                    "name": name,
                    "quantity": quantity,
                    "unit": unit,
                    "category": "general"
                })
            elif len(match) == 2:
                if match[0].lower() in word_to_num:
                    # Handle "one milk" format
                    quantity = word_to_num[match[0].lower()]
                    name = match[1].strip().lower()
                else:
                    # Handle "1 milk" format
                    quantity = int(match[0])
                    name = match[1].strip().lower()
                
                items.append({
                    "name": name,
                    "quantity": quantity,
                    "unit": "pieces",
                    "category": "general"
                })
    
    return items

def generate_order_summary(grocery_items):
    """
    Generate a human-readable summary of the order
    """
    if not grocery_items:
        return "I couldn't understand your grocery list. Please try again with a clearer format."
    
    summary = "I've understood your order! Here's what I'll get for you:\n\n"
    
    # Use a set to track unique items to avoid duplicates
    seen_items = set()
    unique_items = []
    
    for item in grocery_items:
        # Create a unique key based on just the item name (normalized) to avoid duplicates
        # Remove common prefixes like "packet", "pieces", etc. from the name
        clean_name = item['name'].lower().strip()
        
        # Remove common quantity/unit words that might be part of the name
        clean_name = re.sub(r'\b(packet|packets|piece|pieces|kg|g|liter|liters|dozen|bottle|bottles|can|cans)\b', '', clean_name).strip()
        clean_name = re.sub(r'\s+', ' ', clean_name)  # Normalize multiple spaces
        
        if clean_name not in seen_items:
            seen_items.add(clean_name)
            unique_items.append(item)
    
    # Generate summary from unique items only
    for item in unique_items:
        summary += f"• {item['quantity']} {item['unit']} of {item['name'].title()} ({item['category']})\n"
    
    summary += "\nReady to place your order? Click the Confirm Order button below or Cancel if you'd like to make changes."
    return summary

@app.route('/')
def index():
    """Main chat interface page"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint for testing"""
    return jsonify({
        'status': 'healthy',
        'message': 'Kirana Tap backend is running!',
        'version': '1.0.0'
    })

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('status', {'message': 'Connected to Kirana Tap!'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

@socketio.on('confirm_order')
def handle_order_confirmation(data):
    """Handle order confirmation from user"""
    try:
        order_id = data.get('order_id')
        grocery_items = pending_orders.get(order_id, {}).get('items', [])
        
        if not grocery_items:
            emit('order_update', {
                'status': 'error',
                'message': 'Order not found or already processed'
            })
            return
        
        # Start order placement in background thread
        def place_order_background():
            try:
                blinkit = BlinkitAutomation()
                success, message = blinkit.place_order(grocery_items)
                
                if success:
                    # Update order status
                    pending_orders[order_id]['status'] = 'completed'
                    pending_orders[order_id]['message'] = message
                    
                    # Notify user
                    socketio.emit('order_update', {
                        'order_id': order_id,
                        'status': 'completed',
                        'message': message
                    })
                else:
                    # Check if it's a product availability issue
                    if "not available" in message.lower() or "not found" in message.lower():
                        # Try to suggest alternatives
                        try:
                            alternatives = blinkit.check_alternatives(grocery_items[0]['name'])
                            if alternatives:
                                alt_message = f"{message}\n\nAlternative options available:\n"
                                for alt in alternatives[:3]:  # Show top 3 alternatives
                                    alt_message += f"• {alt}\n"
                                alt_message += "\nWould you like me to try one of these alternatives?"
                            else:
                                alt_message = f"{message}\n\nNo alternatives found. Please try a different search term."
                        except:
                            alt_message = message
                        
                        # Update order status
                        pending_orders[order_id]['status'] = 'failed'
                        pending_orders[order_id]['message'] = alt_message
                        
                        # Notify user
                        socketio.emit('order_update', {
                            'order_id': order_id,
                            'status': 'failed',
                            'message': alt_message
                        })
                    else:
                        # Regular failure
                        pending_orders[order_id]['status'] = 'failed'
                        pending_orders[order_id]['message'] = message
                        
                        socketio.emit('order_update', {
                            'order_id': order_id,
                            'status': 'failed',
                            'message': message
                        })
                    
            except Exception as e:
                error_msg = f"Order placement failed: {str(e)}"
                pending_orders[order_id]['status'] = 'failed'
                pending_orders[order_id]['message'] = error_msg
                
                socketio.emit('order_update', {
                    'order_id': order_id,
                    'status': 'failed',
                    'message': error_msg
                })
        
        # Start background thread
        thread = threading.Thread(target=place_order_background)
        thread.daemon = True
        thread.start()
        
        # Update order status to processing
        pending_orders[order_id]['status'] = 'processing'
        
        emit('order_update', {
            'order_id': order_id,
            'status': 'processing',
            'message': 'Starting to place your order on Blinkit... This may take a few minutes.'
        })
        
    except Exception as e:
        emit('order_update', {
            'status': 'error',
            'message': f'Failed to process order confirmation: {str(e)}'
        })

@socketio.on('chat_message')
def handle_chat_message(data):
    """Handle incoming chat messages"""
    message = data.get('message', '').strip()
    print(f'Received message: {message}')
    
    if not message:
        return
    
    # Check if this is an order confirmation
    if message.lower() in ['yes', 'confirm', 'proceed', 'place order', 'order now']:
        # Find the latest pending order for this user
        # For simplicity, we'll use the first available order
        # In production, you'd track user sessions properly
        pending_order = None
        for order_id, order_data in pending_orders.items():
            if order_data.get('status') == 'pending':
                pending_order = order_id
                break
        
        if pending_order:
            # Trigger order confirmation
            handle_order_confirmation({'order_id': pending_order})
            return
        else:
            response = "I don't see any pending orders to confirm. Please start by telling me what groceries you need."
            emit('chat_response', {
                'message': response,
                'timestamp': 'now',
                'grocery_items': []
            })
            return
    
    # Parse the grocery list using AI
    grocery_items = parse_grocery_list(message)
    
    # Generate response
    if grocery_items:
        # Create a new order
        import uuid
        order_id = str(uuid.uuid4())[:8]
        
        pending_orders[order_id] = {
            'items': grocery_items,
            'status': 'pending',
            'timestamp': 'now'
        }
        
        response = generate_order_summary(grocery_items)
        
        # Remove order ID from initial message - it will be shown after confirmation
        # response += f"\n\nOrder ID: {order_id}\n\nReply with 'yes' to confirm and place this order!"
        
        print(f"Created order {order_id} with items: {grocery_items}")
    else:
        response = "I'm having trouble understanding your grocery list. Could you please rephrase it? For example: 'I need 2 kg potatoes, 1 dozen eggs, and 3 packets of bread'"
    
    emit('chat_response', {
        'message': response,
        'timestamp': 'now',
        'grocery_items': grocery_items if grocery_items else [],
        'order_id': order_id if grocery_items else None
    })

if __name__ == '__main__':
    print("🚀 Starting Kirana Tap Backend...")
    print("📍 Health check available at: http://localhost:5000/health")
    print("🌐 Chat interface at: http://localhost:5000/")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
