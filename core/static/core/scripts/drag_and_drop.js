document.addEventListener('DOMContentLoaded', function () {
    const createIssueButton = document.getElementById('create-issue-btn');
    const createIssuePanel = document.getElementById('issueCreationPanel');

    // Toggle visibility of the issue creation panel
    if (createIssueButton && createIssuePanel) {
        createIssueButton.addEventListener('click', function() {
            createIssuePanel.style.right = '0';
        });

        const closeButton = createIssuePanel.querySelector('.close');
        closeButton.addEventListener('click', function() {
            createIssuePanel.style.right = '-100%';
        });
    }

    const createIssueForm = document.getElementById('create-issue-form');
    createIssueForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);

        fetch(`/api/project/${project_id}/create_issue/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                addTaskToColumn(data, 'todo');
                createIssuePanel.style.right = '-100%'; // Close the panel after submission
            } else {
                console.error('Failed to create issue:', data.errors);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Drag and drop functionality for tasks
    enableDragAndDrop();
});

function addTaskToColumn(data, columnId) {
    const column = document.getElementById(columnId);
    const newTask = document.createElement('div');
    newTask.classList.add('task', 'draggable');
    newTask.setAttribute('data-issue-id', data.issue_id);
    newTask.innerHTML = `<h3>${data.title}</h3><p>${data.description}</p>`;
    column.appendChild(newTask);
    makeDraggable(newTask);
}

function enableDragAndDrop() {
    const tasks = document.querySelectorAll('.draggable');
    const columns = document.querySelectorAll('.task-list');

    tasks.forEach(task => {
        task.addEventListener('dragstart', dragStart);
    });

    columns.forEach(column => {
        column.addEventListener('dragover', dragOver);
        column.addEventListener('drop', drop);
    });
}

function dragStart(event) {
    event.dataTransfer.setData("text/plain", event.target.getAttribute('data-issue-id'));
}

function dragOver(event) {
    event.preventDefault(); // Necessary to allow dropping
}

function drop(event) {
    event.preventDefault();
    const issueId = event.dataTransfer.getData("text");
    const task = document.querySelector(`[data-issue-id="${issueId}"]`);
    if (event.target.className.includes('task-list')) {
        event.target.appendChild(task);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            let [key, value] = cookie.split('=');
            if (key.trim() === name) {
                return decodeURIComponent(value);
            }
        }
    }
    return cookieValue;
}

function makeDraggable(element) {
    element.draggable = true;
    element.addEventListener('dragstart', dragStart);
}
