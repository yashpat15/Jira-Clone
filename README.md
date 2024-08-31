# Jira Clone

This repository hosts a simplified version of Jira, designed as a SCRUM board application built with Django. It features user authentication, project management, and issue tracking with a draggable interface for task management.

## Features

- **User Authentication**: Includes both standard and OAuth integrations.
- **Project Management**: Capability to create and edit projects.
- **Issue Tracking**: Add and manage issues with status updates across SCRUM board stages.
- **Draggable Tasks**: Move issues between stages directly on the SCRUM board.

## Installation

Follow these steps to set up the project locally:

```bash
# Clone the repository
git clone https://github.com/yourusername/jira-clone.git

# Navigate to the project directory
cd jira-clone

# Install required dependencies
pip install -r requirements.txt

# Apply migrations to create the database schema
python manage.py migrate

# Start the development server
python manage.py runserver

Usage:
Once the server is running, access the application at http://localhost:8000 in your web browser.
