"""
Quick Red Tech - Flask Backend Application
Premium Web Development Services Platform
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
import os
import sqlite3
from datetime import datetime
import hashlib
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database configuration
DATABASE = os.environ.get('DATABASE_URL', 'quickredtech.db').replace('sqlite:///', '')

# Brevo SMTP Configuration
SMTP_SERVER = os.environ.get('BREVO_SMTP_SERVER', 'smtp-relay.brevo.com')
SMTP_PORT = int(os.environ.get('BREVO_SMTP_PORT', 587))
SMTP_LOGIN = os.environ.get('BREVO_SMTP_LOGIN', 'aa47d9001@smtp-brevo.com')
SMTP_KEY = os.environ.get('BREVO_SMTP_KEY', '')

def get_db():
    """Get database connection"""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize database tables"""
    db = get_db()
    cursor = db.cursor()
    
    # Create submissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            business_name TEXT NOT NULL,
            website_type TEXT NOT NULL,
            budget TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create admin table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert default admin if not exists
    admin_email = os.environ.get('ADMIN_EMAIL', 'chisomlifeeke@gmail.com')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    password_hash = hashlib.sha256(admin_password.encode()).hexdigest()
    
    try:
        cursor.execute('INSERT INTO admins (email, password_hash) VALUES (?, ?)', 
                      (admin_email, password_hash))
    except sqlite3.IntegrityError:
        pass  # Admin already exists
    
    db.commit()
    db.close()

# Initialize database on startup
init_db()

def login_required(f):
    """Decorator to require login for admin routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please log in to access the admin panel.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/submit-request', methods=['POST'])
def submit_request():
    """Handle form submission"""
    try:
        data = request.form
        
        # Validate required fields
        required_fields = ['full_name', 'email', 'phone', 'business_name', 'website_type', 'budget', 'description']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} is required'}), 400
        
        # Store in database
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO submissions (full_name, email, phone, business_name, website_type, budget, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['full_name'],
            data['email'],
            data['phone'],
            data['business_name'],
            data['website_type'],
            data['budget'],
            data['description']
        ))
        db.commit()
        submission_id = cursor.lastrowid
        db.close()
        
        # Send email via Brevo (placeholder - implement with actual Brevo API)
        send_confirmation_email(data)
        
        return jsonify({
            'success': True, 
            'message': 'Your request has been submitted successfully! We will contact you soon.'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

def send_confirmation_email(data):
    """Send confirmation email using Brevo SMTP"""
    try:
        if not SMTP_KEY:
            print("Brevo SMTP key not configured")
            return
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Website Request Confirmation - Quick Red Tech"
        msg['From'] = f"{os.environ.get('BREVO_SENDER_NAME', 'Quick Red Tech')} <{os.environ.get('BREVO_SENDER_EMAIL', 'noreply@quickredtech.com')}>"
        msg['To'] = data['email']
        
        # Plain text version
        text = f"""
        Thank You for Your Interest!
        
        Dear {data['full_name']},
        
        We have received your website request for {data['business_name']}.
        Our team will review your requirements and contact you within 24-48 hours.
        
        Request Details:
        - Website Type: {data['website_type']}
        - Budget: {data['budget']}
        - Email: {data['email']}
        - Phone: {data['phone']}
        
        We're excited to build your dream website!
        
        Best regards,
        Quick Red Tech Team
        """
        
        # HTML version
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background: #0a0a0a; color: #ffffff;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h1 style="color: #ff0000;">Thank You for Your Interest!</h1>
                    <p>Dear {data['full_name']},</p>
                    <p>We have received your website request for <strong>{data['business_name']}</strong>.</p>
                    <p>Our team will review your requirements and contact you within 24-48 hours.</p>
                    
                    <h3>Request Details:</h3>
                    <ul>
                        <li><strong>Website Type:</strong> {data['website_type']}</li>
                        <li><strong>Budget:</strong> {data['budget']}</li>
                        <li><strong>Email:</strong> {data['email']}</li>
                        <li><strong>Phone:</strong> {data['phone']}</li>
                    </ul>
                    
                    <p style="color: #ff0000; font-weight: bold;">We're excited to build your dream website!</p>
                    
                    <p>Best regards,<br>Quick Red Tech Team</p>
                </div>
            </body>
        </html>
        """
        
        # Attach both versions
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send via SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_LOGIN, SMTP_KEY)
            server.sendmail(msg['From'], data['email'], msg.as_string())
        
        print(f"Email sent successfully to {data['email']}")
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM admins WHERE email = ? AND password_hash = ?', (email, password_hash))
        admin = cursor.fetchone()
        db.close()
        
        if admin:
            session['admin_logged_in'] = True
            session['admin_email'] = email
            flash('Welcome back!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    db = get_db()
    cursor = db.cursor()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) as total FROM submissions')
    total_submissions = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as pending FROM submissions WHERE status = 'pending'")
    pending_submissions = cursor.fetchone()['pending']
    
    cursor.execute("SELECT COUNT(*) as completed FROM submissions WHERE status = 'completed'")
    completed_submissions = cursor.fetchone()['completed']
    
    # Get recent submissions
    cursor.execute('SELECT * FROM submissions ORDER BY created_at DESC LIMIT 10')
    recent_submissions = cursor.fetchall()
    
    db.close()
    
    stats = {
        'total': total_submissions,
        'pending': pending_submissions,
        'completed': completed_submissions
    }
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         submissions=recent_submissions,
                         admin_email=session.get('admin_email'))

@app.route('/admin/submissions')
@login_required
def admin_submissions():
    """View all submissions"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM submissions ORDER BY created_at DESC')
    submissions = cursor.fetchall()
    db.close()
    
    return render_template('admin/submissions.html', submissions=submissions)

@app.route('/admin/update-status/<int:id>', methods=['POST'])
@login_required
def update_submission_status(id):
    """Update submission status"""
    status = request.form.get('status', 'pending')
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE submissions SET status = ? WHERE id = ?', (status, id))
    db.commit()
    db.close()
    
    flash('Status updated successfully', 'success')
    return redirect(url_for('admin_submissions'))

@app.route('/admin/delete/<int:id>', methods=['POST'])
@login_required
def delete_submission(id):
    """Delete a submission"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM submissions WHERE id = ?', (id,))
    db.commit()
    db.close()
    
    flash('Submission deleted successfully', 'success')
    return redirect(url_for('admin_submissions'))

@app.route('/admin/export')
@login_required
def export_submissions():
    """Export submissions as CSV"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM submissions ORDER BY created_at DESC')
    submissions = cursor.fetchall()
    db.close()
    
    import csv
    from io import StringIO
    from flask import make_response
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Full Name', 'Email', 'Phone', 'Business Name', 'Website Type', 'Budget', 'Description', 'Status', 'Created At'])
    
    for sub in submissions:
        writer.writerow([
            sub['id'], sub['full_name'], sub['email'], sub['phone'],
            sub['business_name'], sub['website_type'], sub['budget'],
            sub['description'], sub['status'], sub['created_at']
        ])
    
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=submissions.csv'
    response.headers['Content-type'] = 'text/csv'
    
    return response

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
