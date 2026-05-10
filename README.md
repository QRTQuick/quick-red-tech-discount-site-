# Quick Red Tech - Premium Web Development Services Platform

A modern, premium, responsive website for Quick Red Tech - a web development agency offering discounted services. Built with Flask backend and featuring a dark luxury UI with red, black, and white color palette.

## 🚀 Features

### Frontend
- **Modern Hero Section** - Animated with floating particles and glassmorphism effects
- **Services Section** - 8 service cards with hover animations
- **Pricing Plans** - Starter (₦23,000), Professional (₦80,000), Premium (₦250,000)
- **Features Grid** - 8 premium features with icons
- **Promotional Banner** - Countdown timer with discount badge
- **Testimonials Slider** - Auto-rotating client reviews
- **FAQ Accordion** - Interactive question/answer section
- **Contact Form** - Brevo API integration for email automation
- **Admin Dashboard** - Full CRUD operations for submissions

### Backend
- Flask REST API
- SQLite database (upgradeable to PostgreSQL)
- Admin authentication system
- Form submission handling
- Brevo email integration
- CSV export functionality
- Session management

### Design Features
- Dark luxury theme with red accents
- Responsive design (mobile, tablet, desktop)
- Smooth scroll animations
- Loading animation
- Particle effects
- WhatsApp floating button
- Back-to-top button
- Sticky navigation

## 📁 Project Structure

```
quick-red-tech/
├── backend/
│   └── app.py                 # Main Flask application
├── templates/
│   ├── index.html             # Main landing page
│   └── admin/
│       ├── login.html         # Admin login page
│       ├── dashboard.html     # Admin dashboard
│       └── submissions.html   # All submissions view
├── static/
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   ├── js/
│   │   └── main.js            # JavaScript interactions
│   └── images/                # Image assets
├── config/
├── models/
├── api/
├── .env.example               # Environment variables template
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager
- Brevo API key (for email functionality)
- InSForge backend account (optional)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd quick-red-tech
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env`:
```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Brevo API Configuration
BREVO_API_KEY=your-brevo-api-key
BREVO_SENDER_EMAIL=noreply@quickredtech.com
BREVO_SENDER_NAME=Quick Red Tech

# Admin Configuration
ADMIN_EMAIL=chisomlifeeke@gmail.com
ADMIN_PASSWORD=your-secure-password

# Database
DATABASE_URL=sqlite:///quickredtech.db

# WhatsApp Number
WHATSAPP_NUMBER=+2341234567890
```

### 5. Run the Application

```bash
python backend/app.py
```

Visit `http://localhost:5000` in your browser.

## 🔐 Admin Access

- **Login URL**: `http://localhost:5000/admin/login`
- **Default Email**: chisomlifeeke@gmail.com
- **Default Password**: Set in `.env` file

### Admin Features
- View all form submissions
- Update submission status (pending/completed)
- Delete submissions
- Export data as CSV
- Dashboard statistics

## 📧 Brevo Email Integration

1. Sign up at [Brevo.com](https://www.brevo.com)
2. Get your API key from Settings > SMTP & API
3. Add the API key to your `.env` file
4. The system will automatically send confirmation emails when forms are submitted

## 🚀 Deployment

### Deploying to Vercel (Frontend)

1. Build static files:
```bash
# Generate static files if needed
```

2. Connect your repository to Vercel
3. Configure build settings
4. Deploy

### Deploying Flask Backend

#### Option 1: Heroku
```bash
# Create Procfile
echo "web: gunicorn backend.app:app" > Procfile

# Deploy
heroku create quickredtech-backend
git push heroku main
```

#### Option 2: Railway
1. Connect GitHub repository
2. Select the backend folder
3. Add environment variables
4. Deploy

#### Option 3: DigitalOcean App Platform
1. Create new app
2. Connect GitHub
3. Configure Python environment
4. Add environment variables
5. Deploy

### Environment Variables for Production

Set these in your hosting platform:
- `SECRET_KEY` - Generate a strong random key
- `BREVO_API_KEY` - Your Brevo API key
- `ADMIN_EMAIL` - Admin email address
- `ADMIN_PASSWORD` - Strong admin password
- `DATABASE_URL` - Production database URL
- `FLASK_ENV` - production

## 🎨 Customization

### Colors
Edit CSS variables in `static/css/style.css`:
```css
:root {
    --primary-red: #ff0000;
    --bg-dark: #0a0a0a;
    --bg-card: #121212;
    /* ... more variables */
}
```

### Content
Update text content in `templates/index.html`

### WhatsApp Number
Update the WhatsApp link in `templates/index.html`:
```html
<a href="https://wa.me/2341234567890" class="whatsapp-float">
```

## 📱 Mobile Responsiveness

The website is fully responsive with breakpoints at:
- Desktop: 992px+
- Tablet: 768px - 991px
- Mobile: < 768px
- Small Mobile: < 480px

## 🔒 Security Features

- Password hashing for admin authentication
- CSRF protection (Flask built-in)
- Input validation on forms
- SQL injection prevention (parameterized queries)
- Session management

## 📊 Database Schema

### Submissions Table
```sql
CREATE TABLE submissions (
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
);
```

### Admins Table
```sql
CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🧪 Testing

Run the application and test:
1. Homepage loads correctly
2. Form submission works
3. Email confirmation is sent
4. Admin login works
5. Dashboard displays data
6. CRUD operations function properly
7. Mobile responsiveness

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Homepage |
| POST | `/submit-request` | Submit form |
| GET | `/admin/login` | Admin login page |
| POST | `/admin/login` | Process login |
| GET | `/admin/dashboard` | Dashboard view |
| GET | `/admin/submissions` | All submissions |
| POST | `/admin/update-status/<id>` | Update status |
| POST | `/admin/delete/<id>` | Delete submission |
| GET | `/admin/export` | Export CSV |
| GET | `/admin/logout` | Logout |

## 🤝 Support

For issues or questions:
- Email: chisomlifeeke@gmail.com
- Website: www.quickredtech.websitediscount.vercel.app

## 📄 License

This project is proprietary software. All rights reserved.

---

**Quick Red Tech** - Building powerful modern websites at affordable prices.
