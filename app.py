from flask import Flask, render_template, request, session, jsonify
from datetime import datetime
import os
import json

app = Flask(__name__)
app.secret_key = 'dev-secret-key-for-testing'

# Mock data storage (in-memory for testing)
users_db = []
activity_logs = []
unauthorized_logs = []

# Configuration
ALLOWED_USERS = [
    'gcptrail0@gmail.com',
    'pravinrajagcp@gmail.com', 
    'parthibank72@gmail.com'
]

# Initialize mock data
def initialize_mock_data():
    """Initialize mock user data"""
    global users_db
    users_db = ALLOWED_USERS.copy()
    print("✅ Mock data initialized with allowed users:")
    for user in users_db:
        print(f"   - {user}")

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main application page"""
    if request.method == 'POST':
        email = request.form.get('email')
        session['user_email'] = email
        session['user_name'] = email.split('@')[0]
    
    # Check if user is logged in
    if 'user_email' not in session:
        return render_template('email_form.html')
    
    user_email = session.get('user_email')
    user_name = session.get('user_name', user_email.split('@')[0])
    
    # Check if user is authorized
    if user_email not in ALLOWED_USERS:
        # Log unauthorized access
        unauthorized_logs.append({
            'email': user_email,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'reason': 'User not in allowed list'
        })
        return render_template('unauthorized.html', 
                             user_email=user_email, 
                             user_name=user_name)
    
    # Log page load activity
    activity_logs.append({
        'id': len(activity_logs) + 1,
        'user_email': user_email,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'activity_type': 'Page Load'
    })
    
    # Get recent logs for this user (last 10)
    user_logs = [log for log in activity_logs if log['user_email'] == user_email][-10:]
    
    return render_template('dashboard.html', 
                         user_email=user_email,
                         user_name=user_name,
                         logs=user_logs)

@app.route('/api/logs')
def get_logs_api():
    """API endpoint to get user logs"""
    user_email = session.get('user_email')
    if not user_email or user_email not in ALLOWED_USERS:
        return jsonify({'error': 'Access denied'}), 403
    
    user_logs = [log for log in activity_logs if log['user_email'] == user_email][-10:]
    return jsonify({'logs': user_logs})

@app.route('/api/send-notification', methods=['POST'])
def send_notification():
    """API endpoint to send notification (mock Pub/Sub)"""
    user_email = session.get('user_email')
    if not user_email or user_email not in ALLOWED_USERS:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        # Mock Pub/Sub message
        message_data = {
            'user_email': user_email,
            'timestamp': datetime.now().isoformat(),
            'type': 'user_notification',
            'message': f'Mock notification triggered by {user_email}',
            'mock_message_id': f"mock-msg-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }
        
        # Log notification activity
        activity_logs.append({
            'id': len(activity_logs) + 1,
            'user_email': user_email,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'activity_type': 'Notification Sent'
        })
        
        print(f"📧 Mock Pub/Sub Message Sent: {json.dumps(message_data, indent=2)}")
        
        return jsonify({
            'status': 'Mock notification sent successfully',
            'message_id': message_data['mock_message_id'],
            'note': 'This is a mock implementation - no actual Pub/Sub used'
        })
    
    except Exception as e:
        print(f"❌ Error sending mock notification: {e}")
        return jsonify({'error': 'Failed to send notification'}), 500

@app.route('/debug')
def debug():
    """Debug page to see all data"""
    return jsonify({
        'allowed_users': ALLOWED_USERS,
        'activity_logs': activity_logs,
        'unauthorized_logs': unauthorized_logs,
        'session': dict(session)
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'mode': 'local-test'})

@app.route('/clear')
def clear_data():
    """Clear all mock data (for testing)"""
    global activity_logs, unauthorized_logs
    activity_logs.clear()
    unauthorized_logs.clear()
    session.clear()
    return jsonify({'status': 'all data cleared'})

if __name__ == '__main__':
    initialize_mock_data()
    print("🚀 Starting Flask development server...")
    print("📍 Access the application at: http://localhost:5000")
    print("👤 Allowed test users:")
    for user in ALLOWED_USERS:
        print(f"   • {user}")
    print("\n🔧 Debug endpoints:")
    print("   • /debug - View all data")
    print("   • /clear - Clear all data")
    print("   • /health - Health check")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
