Event Management System

Introduction
This is a Python Django advanced project for managing events. The project uses pure Django and aims to provide a comprehensive event management platform.

Features
User registration and login functionality
Event creation, updating, and deletion
Category management for events
Viewing events by category
Event statistics and charts

Requirements
Python 3.8+
Django 3.2+
pip packages: django, djangorestframework

Installation
Clone the repository: git clone (https://github.com/Karthik-ihub/event_management_system.git)
Install the required packages: pip install -r requirements.txt


Usage
Open a web browser and navigate to http://localhost:8000
Register a new user or login with an existing account
Create, update, or delete events
Manage event categories
View events by category and check event statistics

Views
create_category
Handles the creation of new event categories.

delete_category
Handles the deletion of event categories. Prevents deletion if the category contains events.

category_list
Displays a list of all event categories.

category_events
Displays all events under a specific category.

event_chart
Displays a chart of pending events by category.

Contributing
Feel free to fork this repository and contribute by submitting a pull request.

License
This project is licensed under the MIT License.

