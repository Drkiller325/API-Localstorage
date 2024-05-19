document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.getElementById('task-input');
    const addTaskButton = document.getElementById('add-task');
    const taskList = document.getElementById('task-list');
    const categorySelect = document.getElementById('category-select');
    const themeToggleButton = document.getElementById('theme-toggle');
    const body = document.body;

    let token = '';

    const login = async () => {
        const response = await fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: 'admin', password: 'password' }),
        });
        const data = await response.json();
        token = data.access_token;
    };

    const fetchTasks = async () => {
        const response = await fetch('http://localhost:5000/api/tasks', {
            headers: { 'Authorization': `Bearer ${token}` },
        });
        const tasks = await response.json();
        renderTasks(tasks);
    };

    const renderTasks = (tasks) => {
        taskList.innerHTML = '';
        tasks.forEach((task, index) => {
            const li = document.createElement('li');
            li.innerHTML = `
                ${task.name} - <strong>${task.category}</strong>
                <div>
                    <button class="like-button ${task.completed ? 'liked' : ''}" data-index="${index}">
                        ${task.completed ? '✅' : '✅︎'}
                    </button>
                    <button class="delete-button" data-index="${index}">❌</button>
                </div>
            `;
            taskList.appendChild(li);
        });
    };

    addTaskButton.addEventListener('click', async () => {
        const taskName = taskInput.value.trim();
        const category = categorySelect.value;
        if (taskName) {
            await fetch('http://localhost:5000/api/tasks', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ name: taskName, category: category }),
            });
            taskInput.value = '';
            fetchTasks();
        }
    });

    taskList.addEventListener('click', async (event) => {
        const index = event.target.getAttribute('data-index');
        const response = await fetch('http://localhost:5000/api/tasks', {
            headers: { 'Authorization': `Bearer ${token}` },
        });
        const tasks = await response.json();

        if (event.target.classList.contains('like-button')) {
            const task = tasks[index];
            task.completed = !task.completed;
            await fetch(`http://localhost:5000/api/tasks/${task.id}`, {
                method: 'PUT',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ completed: task.completed }),
            });
            fetchTasks();
        } else if (event.target.classList.contains('delete-button')) {
            const task = tasks[index];
            await fetch(`http://localhost:5000/api/tasks/${task.id}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` },
            });
            fetchTasks();
        }
    });

    themeToggleButton.addEventListener('click', () => {
        body.classList.toggle('dark-theme');
        const theme = body.classList.contains('dark-theme') ? 'dark' : 'light';
        localStorage.setItem('theme', theme);
    });

    (async () => {
        await login();
        fetchTasks();
    })();
});
