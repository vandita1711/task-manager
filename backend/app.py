from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

# ... existing imports ...

app = Flask(__name__)

# Production CORS configuration
if os.environ.get('FLASK_ENV') == 'production':
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "https://*.onrender.com",
                "http://localhost:3000"
            ]
        }
    })
else:
    CORS(app)  # Allow all in development
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
DATABASE = 'tasks.db'

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

def init_database():
    """Initialize the database with schema"""
    conn = get_db_connection()
    
    # Create users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create tasks table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            status VARCHAR(20) DEFAULT 'pending',
            priority VARCHAR(10) DEFAULT 'medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Insert sample users if they don't exist
    conn.execute('''
        INSERT OR IGNORE INTO users (id, username, email) VALUES 
        (1, 'john_doe', 'john@example.com'),
        (2, 'jane_smith', 'jane@example.com')
    ''')
    
    # Insert sample tasks if they don't exist
    conn.execute('''
        INSERT OR IGNORE INTO tasks (user_id, title, description, status, priority) VALUES 
        (1, 'Complete Python project', 'Finish the task manager API', 'pending', 'high'),
        (1, 'Buy groceries', 'Get milk, bread, and eggs', 'pending', 'medium'),
        (2, 'Review code', 'Review the new feature implementation', 'in-progress', 'high'),
        (2, 'Team meeting', 'Weekly standup meeting', 'completed', 'low')
    ''')
    
    conn.commit()
    conn.close()

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'OK', 'message': 'Task Manager API is running'})

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    
    return jsonify([dict(user) for user in users])

@app.route('/api/users/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    """Get all tasks for a specific user"""
    conn = get_db_connection()
    
    # Optional status filter
    status = request.args.get('status')
    
    if status:
        tasks = conn.execute(
            'SELECT * FROM tasks WHERE user_id = ? AND status = ? ORDER BY created_at DESC',
            (user_id, status)
        ).fetchall()
    else:
        tasks = conn.execute(
            'SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC',
            (user_id,)
        ).fetchall()
    
    conn.close()
    
    return jsonify([dict(task) for task in tasks])

@app.route('/api/tasks', methods=['GET'])
def get_all_tasks():
    """Get all tasks with user information"""
    conn = get_db_connection()
    tasks = conn.execute('''
        SELECT t.*, u.username 
        FROM tasks t 
        JOIN users u ON t.user_id = u.id 
        ORDER BY t.created_at DESC
    ''').fetchall()
    conn.close()
    
    return jsonify([dict(task) for task in tasks])

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('title') or not data.get('user_id'):
        return jsonify({'error': 'Title and user_id are required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO tasks (user_id, title, description, status, priority)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data['user_id'],
        data['title'],
        data.get('description', ''),
        data.get('status', 'pending'),
        data.get('priority', 'medium')
    ))
    
    task_id = cursor.lastrowid
    conn.commit()
    
    # Get the created task
    new_task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    
    return jsonify(dict(new_task)), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    conn = get_db_connection()
    
    # Check if task exists
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if not task:
        conn.close()
        return jsonify({'error': 'Task not found'}), 404
    
    # Update task
    conn.execute('''
        UPDATE tasks 
        SET title = ?, description = ?, status = ?, priority = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (
        data.get('title', task['title']),
        data.get('description', task['description']),
        data.get('status', task['status']),
        data.get('priority', task['priority']),
        task_id
    ))
    
    conn.commit()
    
    # Get updated task
    updated_task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    
    return jsonify(dict(updated_task))

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    conn = get_db_connection()
    
    # Check if task exists
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if not task:
        conn.close()
        return jsonify({'error': 'Task not found'}), 404
    
    # Delete task
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Task deleted successfully'})

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task"""
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(dict(task))

@app.route('/')
def home():
    return jsonify({
        'message': '✅ Task Manager API is running successfully on Render!',
        'available_endpoints': [
            '/api/health',
            '/api/users',
            '/api/users/<user_id>/tasks',
            '/api/tasks'
        ]
    })


if __name__ == '__main__':
    # Initialize database
    init_database()
    print("Database initialized successfully!")
    print("Starting Flask API server...")
    print("API endpoints available at http://localhost:5000/api/")
    app.run(debug=True, port=5000)