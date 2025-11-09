# 📋 Task Manager - Full Stack Web Application

![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![Node.js](https://img.shields.io/badge/node.js-v14+-green.svg)
![Flask](https://img.shields.io/badge/flask-v2.3+-red.svg)
![Express](https://img.shields.io/badge/express-v4.18+-yellow.svg)
![SQLite](https://img.shields.io/badge/sqlite-v3+-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-live-success.svg)

A modern, full-stack task management application built with **Python Flask REST API**, **Node.js Express frontend**, and **SQLite database**. This project demonstrates proficiency in full-stack web development, RESTful API design, database management, and cloud deployment.

---

## 🌐 Live Demo

**🚀 Try the Application:**

- **Frontend Application**: [https://task-manager-frontend-mqkv.onrender.com](https://task-manager-frontend-mqkv.onrender.com)
- **Backend API**: [https://task-manager-api-1p72.onrender.com](https://task-manager-api-1p72.onrender.com)
- **API Health Check**: [https://task-manager-api-1p72.onrender.com/api/health](https://task-manager-api-1p72.onrender.com/api/health)

> ⚠️ **Note**: Free tier services may take 30-50 seconds to wake up from sleep on first request. Subsequent requests are instant!

---

## ✨ Features

### 🎨 User Interface
-  **Modern Responsive Design** - Bootstrap 5 with mobile-first approach
-  **Real-time Dashboard** - Live task statistics and progress tracking
-  **Intuitive Navigation** - Clean, user-friendly interface
-  **Interactive Forms** - Dynamic task creation and editing
-  **Mobile Optimized** - Works seamlessly on all devices

### 🔧 Backend API
-  **RESTful Architecture** - Complete CRUD operations
-  **Data Validation** - Server-side validation and error handling
-  **Database Relationships** - Proper foreign key constraints
-  **CORS Support** - Cross-origin resource sharing enabled
-  **Health Monitoring** - API health check endpoint

### 📊 Task Management
-  **Multi-user Support** - Assign tasks to different users
-  **Priority Levels** - High, Medium, Low priority classification
-  **Status Tracking** - Pending → In Progress → Completed workflow
-  **Advanced Filtering** - Filter by user, status, and priority
-  **Task Statistics** - Real-time dashboard with task counts

---

## 🛠️ Technology Stack

| Layer | Technologies |
|-------|--------------|
| **Frontend** | Node.js, Express.js, EJS Templates, Bootstrap 5, Axios, Font Awesome |
| **Backend** | Python 3.9+, Flask 2.3, Flask-CORS, Gunicorn |
| **Database** | SQLite with relational schema and foreign keys |
| **Deployment** | Render.com (automated deployment via Blueprint) |
| **Version Control** | Git & GitHub |

### Architecture

```
┌─────────────────────┐
│   Client Browser    │
│   (Bootstrap UI)    │
└──────────┬──────────┘
           │ HTTPS
           ▼
┌─────────────────────┐
│  Node.js Express    │
│    Frontend         │
│  Port 10000         │
└──────────┬──────────┘
           │ HTTP/JSON
           ▼
┌─────────────────────┐
│  Python Flask API   │
│    REST Backend     │
│  Port 5000          │
└──────────┬──────────┘
           │ SQL
           ▼
┌─────────────────────┐
│  SQLite Database    │
│   Relational DB     │
└─────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- Git

### Local Development Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/vandita17/task-manager.git
cd task-manager
```

#### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask API
python app.py
```

Backend will start on `http://localhost:5000`

#### 3. Frontend Setup (New Terminal)
```bash
cd frontend

# Install dependencies
npm install

# Start the Express server
node server.js
```

Frontend will start on `http://localhost:3000`

#### 4. Access the Application
Open your browser and navigate to:
- **Application**: http://localhost:3000
- **API Documentation**: http://localhost:5000/api/

---

## 📊 API Documentation

### Base URL
```
Local: http://localhost:5000/api
Production: https://task-manager-api-1p72.onrender.com/api
```

### Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/health` | API health check | No |
| GET | `/users` | Get all users | No |
| GET | `/tasks` | Get all tasks | No |
| GET | `/users/:id/tasks` | Get user's tasks | No |
| GET | `/users/:id/tasks?status=pending` | Filter tasks by status | No |
| POST | `/tasks` | Create new task | No |
| GET | `/tasks/:id` | Get specific task | No |
| PUT | `/tasks/:id` | Update task | No |
| DELETE | `/tasks/:id` | Delete task | No |

### Example Requests

#### Get All Tasks
```bash
curl https://task-manager-api-1p72.onrender.com/api/tasks
```

#### Create New Task
```bash
curl -X POST https://task-manager-api-1p72.onrender.com/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "title": "Complete project documentation",
    "description": "Write comprehensive README",
    "priority": "high"
  }'
```

#### Update Task
```bash
curl -X PUT https://task-manager-api-1p72.onrender.com/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "priority": "high"
  }'
```


## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    priority VARCHAR(10) DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Sample Data Included:**
- 2 Users: john_doe, jane_smith
- 4 Tasks with various priorities and statuses

---

## 🚀 Deployment

This application is deployed on **Render.com** using automated Blueprint deployment.

### Deploy Your Own Instance

1. **Fork this repository**

2. **Sign up on Render.com** with your GitHub account

3. **Create New Blueprint**:
   - Click "New +" → "Blueprint"
   - Select your forked repository
   - Render will auto-detect `render.yaml`
   - Click "Apply"

4. **Wait for deployment** (5-10 minutes)

5. **Update environment variables** in the frontend service:
   - Set `API_BASE_URL` to your backend URL + `/api`

6. **Done!** Your app is live with automatic HTTPS

### Environment Variables

**Backend:**
```env
FLASK_ENV=production
PYTHON_VERSION=3.9.0
```

**Frontend:**
```env
NODE_ENV=production
API_BASE_URL=https://your-backend-url.onrender.com/api
```

---

## 🧪 Testing

### Manual Testing Checklist
- [ ] Dashboard loads with task statistics
- [ ] View all tasks
- [ ] Create new task
- [ ] Edit existing task
- [ ] Delete task with confirmation
- [ ] Filter by user
- [ ] Filter by status
- [ ] Mobile responsiveness
- [ ] Error handling

### API Testing
```bash
# Health check
curl https://task-manager-api-1p72.onrender.com/api/health

# Get all tasks
curl https://task-manager-api-1p72.onrender.com/api/tasks

# Get all users
curl https://task-manager-api-1p72.onrender.com/api/users
```

---

## 🌟 Key Features Demonstrated

### Full-Stack Development
- ✅ Separate frontend and backend architecture
- ✅ RESTful API design and implementation
- ✅ Database design with relationships
- ✅ Client-server communication via HTTP/JSON

### Modern Web Technologies
- ✅ Server-side rendering with EJS
- ✅ Responsive CSS with Bootstrap 5
- ✅ Asynchronous JavaScript (async/await)
- ✅ Environment-based configuration

### Best Practices
- ✅ Clean code structure and organization
- ✅ Error handling and validation
- ✅ CORS configuration for security
- ✅ Parameterized SQL queries (SQL injection prevention)
- ✅ Version control with meaningful commits

### DevOps & Deployment
- ✅ Cloud deployment on Render
- ✅ Automated deployment via Blueprint
- ✅ Environment variable management
- ✅ Production-ready configuration with Gunicorn

---

## 🔮 Future Enhancements

### Phase 1 - Authentication & Security
- [ ] User authentication with JWT
- [ ] Password hashing and security
- [ ] Protected API routes
- [ ] Session management

### Phase 2 - Enhanced Features
- [ ] Due dates and reminders
- [ ] Task categories/tags
- [ ] File attachments
- [ ] Task comments and notes
- [ ] Email notifications

### Phase 3 - Advanced Functionality
- [ ] Real-time updates with WebSockets
- [ ] Team collaboration features
- [ ] Task dependencies
- [ ] Advanced analytics dashboard
- [ ] Export tasks (CSV, PDF)

### Phase 4 - Scaling
- [ ] PostgreSQL migration for persistence
- [ ] Redis caching for performance
- [ ] API rate limiting
- [ ] Docker containerization
- [ ] CI/CD pipeline with GitHub Actions

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m '✨ Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Vandita**

- 🐙 GitHub: vandita1711
- 💼 LinkedIn: www.linkedin.com/in/vandita-gautam-209a192a0
- 📧 Email: vanditagautam79@gmail.com

---

## 🙏 Acknowledgments

- **Flask Community** - Excellent Python web framework
- **Express.js Team** - Fast, minimalist web framework
- **Bootstrap Team** - Responsive CSS framework
- **Render.com** - Easy cloud deployment platform
- **SQLite** - Lightweight, serverless database

---

## 📊 Project Stats

- **Lines of Code**: ~1,500+
- **Files**: 15+
- **Languages**: Python, JavaScript, HTML, CSS, SQL
- **Deployment**: Automated with Render Blueprint
- **Status**: ✅ Live and Running

---

## 📞 Support

If you have any questions or run into issues:

1. **Check the Issues tab** on GitHub
2. **Open a new issue** with details
3. **Contact me** via email or LinkedIn

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

**🍴 Fork it to create your own version!**

**🐛 Found a bug? Open an issue!**

---

Made with ❤️ by Vandita

*This project was built to demonstrate full-stack web development skills using modern technologies and best practices.*

</div>
