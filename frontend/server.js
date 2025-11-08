const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:5000/api';

console.log('🚀 Server Configuration:');
console.log('📍 Port:', PORT);
console.log('🔗 API URL:', API_BASE_URL);
console.log('🌍 Environment:', process.env.NODE_ENV || 'development');

// Middleware
app.use(express.static('public'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Set EJS as template engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Routes

// Home page - show all tasks
app.get('/', async (req, res) => {
    try {
        const [tasksResponse, usersResponse] = await Promise.all([
            axios.get(`${API_BASE_URL}/tasks`),
            axios.get(`${API_BASE_URL}/users`)
        ]);
        
        res.render('index', {
            tasks: tasksResponse.data,
            users: usersResponse.data,
            selectedUser: null,
            selectedStatus: null
        });
    } catch (error) {
        console.error('Error fetching data:', error.message);
        res.render('index', {
            tasks: [],
            users: [],
            selectedUser: null,
            selectedStatus: null,
            error: 'Unable to connect to API'
        });
    }
});

// Filter tasks by user
app.get('/user/:userId', async (req, res) => {
    try {
        const userId = req.params.userId;
        const status = req.query.status;
        
        let url = `${API_BASE_URL}/users/${userId}/tasks`;
        if (status) {
            url += `?status=${status}`;
        }
        
        const [tasksResponse, usersResponse] = await Promise.all([
            axios.get(url),
            axios.get(`${API_BASE_URL}/users`)
        ]);
        
        res.render('index', {
            tasks: tasksResponse.data,
            users: usersResponse.data,
            selectedUser: parseInt(userId),
            selectedStatus: status || null
        });
    } catch (error) {
        console.error('Error fetching user tasks:', error.message);
        res.redirect('/');
    }
});

// Add new task page
app.get('/add-task', async (req, res) => {
    try {
        const usersResponse = await axios.get(`${API_BASE_URL}/users`);
        res.render('add-task', { users: usersResponse.data });
    } catch (error) {
        console.error('Error fetching users:', error.message);
        res.render('add-task', { users: [] });
    }
});

// Handle new task creation
app.post('/add-task', async (req, res) => {
    try {
        await axios.post(`${API_BASE_URL}/tasks`, {
            user_id: parseInt(req.body.user_id),
            title: req.body.title,
            description: req.body.description,
            priority: req.body.priority,
            status: 'pending'
        });
        res.redirect('/');
    } catch (error) {
        console.error('Error creating task:', error.message);
        res.redirect('/add-task');
    }
});

// Edit task page
app.get('/edit-task/:id', async (req, res) => {
    try {
        const taskId = req.params.id;
        const [taskResponse, usersResponse] = await Promise.all([
            axios.get(`${API_BASE_URL}/tasks/${taskId}`),
            axios.get(`${API_BASE_URL}/users`)
        ]);
        
        res.render('edit-task', {
            task: taskResponse.data,
            users: usersResponse.data
        });
    } catch (error) {
        console.error('Error fetching task:', error.message);
        res.redirect('/');
    }
});

// Handle task update
app.post('/edit-task/:id', async (req, res) => {
    try {
        const taskId = req.params.id;
        await axios.put(`${API_BASE_URL}/tasks/${taskId}`, {
            title: req.body.title,
            description: req.body.description,
            status: req.body.status,
            priority: req.body.priority
        });
        res.redirect('/');
    } catch (error) {
        console.error('Error updating task:', error.message);
        res.redirect(`/edit-task/${req.params.id}`);
    }
});

// Delete task
app.post('/delete-task/:id', async (req, res) => {
    try {
        const taskId = req.params.id;
        await axios.delete(`${API_BASE_URL}/tasks/${taskId}`);
        res.redirect('/');
    } catch (error) {
        console.error('Error deleting task:', error.message);
        res.redirect('/');
    }
});

// API proxy routes for AJAX calls
app.get('/api/users/:userId/tasks', async (req, res) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/users/${req.params.userId}/tasks`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch tasks' });
    }
});

// Start server (ONLY ONE app.listen!)
app.listen(PORT, '0.0.0.0', () => {
    console.log('');
    console.log('✅ Frontend server running successfully!');
    console.log('🌐 Port:', PORT);
    console.log('🔧 API:', API_BASE_URL);
    console.log('');
});