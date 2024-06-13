# Timer and Task Management Application
## Video Demo:  <https://www.youtube.com/watch?v=OV5t65nP_Qg>
This is a Flask-based web application designed to help users manage their time and tasks. The application allows users to add, update, and track timers, tasks, and events. It also provides a progress tracking feature for tasks.

## Features

- User registration and login
- Timer management
- Task management
- Event management
- Progress tracking for tasks
- Calendar view for events

## Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. **Set up a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**
    ```bash
    flask db upgrade
    ```

5. **Run the application**
    ```bash
    flask run
    ```

## Configuration

The application uses SQLite as its database. The database file is `data.db`. If you want to change the database, you can modify the `SQL` configuration in the application.

## Usage

### User Authentication

- **Register**: Create a new account by providing a username and password.
- **Login**: Log in using your username and password.
- **Logout**: Log out of the application.

### Timer Management

- **Add Timer**: Add a new timer with a title, hours, and minutes.
- **Update Timer**: Update the hours and minutes of an existing timer.
- **View Timers**: View all timers associated with your account.

### Task Management

- **Add Task**: Add a new task with a title, description, start time, end time, hours, and minutes.
- **Update Task**: Update the details of an existing task.
- **Delete Task**: Delete an existing task.
- **View Tasks**: View all tasks associated with your account.

### Event Management

- **Add Event**: Add a new event with a title, description, start time, and end time.
- **Update Event**: Update the details of an existing event.
- **Delete Event**: Delete an existing event.
- **View Events**: View all events associated with your account.

### Progress Tracking

- **Track Progress**: The application calculates and displays the progress of each task based on the hours and minutes left.

## Routes

- `/`: Home page with options to add timer, event, or task.
- `/login`: Login page.
- `/logout`: Logout route.
- `/register`: Registration page.
- `/clock`: View all timers.
- `/add_timer`: Add a new timer.
- `/update_timer`: Update an existing timer (AJAX).
- `/add_task`: Add a new task.
- `/update_task/<int:task_id>`: Update an existing task.
- `/delete_task/<int:task_id>`: Delete an existing task.
- `/add_event`: Add a new event.
- `/update_event/<int:event_id>`: Update an existing event.
- `/delete_event/<int:event_id>`: Delete an existing event.
- `/progress_tracker`: View progress of all tasks.
- `/calendar`: View all events in a calendar format.

## Custom Filters

- **usd**: A custom Jinja filter to format numbers as USD currency.

## Helpers

- **apology**: Render an apology message.
- **login_required**: Decorator to require login for certain routes.
- **lookup**: Lookup function (placeholder).
- **usd**: Format numbers as USD currency.
- **days_to_date**: Convert days to date format.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

This project uses the following libraries:

- Flask
- Flask-Session
- CS50 Library
- Werkzeug
- Jinja2

Feel free to reach out if you have any questions or suggestions!

---

Happy coding! 😊
