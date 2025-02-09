from flask import Flask, render_template_string, request, session

# Initialize Flask application
app = Flask(__name__)
app.secret_key = "secret_key"  # Required for session management

# Define the PDA class for brute-force detection
class PDA:
    def __init__(self, threshold):
        self.state = 'q0'  # Initial state
        self.stack = []  # Stack to track failed attempts
        self.threshold = threshold  # Number of failed attempts to trigger alert
        self.alert_triggered = False  # Flag to indicate if alert has been triggered

    def transition(self, input_symbol):
        """
        Perform state transitions based on the input symbol.
        """
        if self.state == 'q0':  # Initial state
            if input_symbol == 'F':
                self.stack.append('X')
                self.state = 'q1'
            elif input_symbol == 'S':
                self.state = 'q3'

        elif self.state == 'q1':  # Tracking state
            if input_symbol == 'F':
                self.stack.append('X')
                if len(self.stack) >= self.threshold:  # Threshold reached
                    self.state = 'q2'
                    self.alert_triggered = True  # Set alert flag to True
            elif input_symbol == 'S':
                self.stack.clear()
                self.state = 'q3'

        elif self.state == 'q2':  # Alert state
            if input_symbol == 'S':  # Reset after successful login
                self.state = 'q3'
                self.stack.clear()
                self.alert_triggered = False  # Reset the alert flag

        elif self.state == 'q3':  # Success state
            self.stack.clear()
            self.state = 'q0'  # Reset after success

    def reset(self):
        """
        Reset the PDA to its initial state.
        """
        self.state = 'q0'
        self.stack.clear()
        self.alert_triggered = False  # Reset the alert flag


# Flask Routes
@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize or retrieve PDA from the session
    if "pda" not in session:
        session["pda"] = PDA(threshold=3).__dict__
    pda = PDA(threshold=3)
    pda.__dict__ = session["pda"]

    alert_message = None
    result_message = None

    if request.method == "POST":
        # Get user credentials and login attempt
        username = request.form["username"]
        password = request.form["password"]

        # Define the correct username and password (for this example)
        correct_username = "admin"
        correct_password = "password123"

        # Simulate login attempts
        if username == correct_username and password == correct_password:
            pda.transition('S')  # Successful login
            result_message = "Login Successful!"
        else:
            pda.transition('F')  # Failed login
            result_message = "Invalid credentials. Please try again."

            # Check if alert was triggered
            if pda.alert_triggered:
                alert_message = "Alert: Brute-force attack detected!"

        # Save PDA state back to session
        session["pda"] = pda.__dict__

        # Record state transitions after each login attempt
        state_transitions = [(username, pda.state, list(pda.stack))]

        # Pass results to the results page
        return render_template_string(
            RESULTS_HTML,
            alert_message=alert_message,
            result_message=result_message,
            transitions=state_transitions,
        )

    # Render the login page (HTML form)
    return render_template_string(LOGIN_HTML)


# HTML for the Login Page (Form Input)
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #74ebd5, #acb6e5);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .login-container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            width: 100%;
            max-width: 400px;
            text-align: center;
        }
        .login-container h1 {
            margin-bottom: 20px;
            color: #333;
        }
        .login-container label {
            display: block;
            margin: 10px 0 5px;
            font-weight: bold;
            color: #555;
        }
        .login-container input {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }
        .login-container button {
            background-color: #007BFF;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
        }
        .login-container button:hover {
            background-color: #0056b3;
        }
        .login-container p {
            margin-top: 10px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>Login</h1>
        <form action="/" method="POST">
            <label for="username">Username</label>
            <input type="text" id="username" name="username" required>
            <label for="password">Password</label>
            <input type="password" id="password" name="password" required>
            <button type="submit">Login</button>
        </form>
        <p>Welcome! Please log in to continue.</p>
    </div>
</body>
</html>
"""

# HTML for the Results Page (Alert and Messages)
RESULTS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Results</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #f093fb, #f5576c);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .results-container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            width: 100%;
            max-width: 500px;
            text-align: center;
        }
        .results-container h1 {
            color: #333;
            margin-bottom: 20px;
        }
        .results-container p {
            font-size: 16px;
            margin: 10px 0;
        }
        .alert {
            color: #d9534f;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .success {
            color: #5cb85c;
            font-weight: bold;
        }
        .table-container {
            margin-top: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: center;
        }
        th {
            background-color: #f7f7f7;
            color: #555;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        a {
            display: inline-block;
            margin-top: 20px;
            text-decoration: none;
            background-color: #007BFF;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
        }
        a:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="results-container">
        <h1>Login Results</h1>

        {% if alert_message %}
            <p class="alert">{{ alert_message }}</p>
        {% endif %}

        <p class="success">{{ result_message }}</p>

        <div class="table-container">
            <h3>State Transitions</h3>
            <table>
                <tr>
                    <th>Input</th>
                    <th>State</th>
                    <th>Stack</th>
                </tr>
                {% for transition in transitions %}
                <tr>
                    <td>{{ transition[0] }}</td>
                    <td>{{ transition[1] }}</td>
                    <td>{{ transition[2] }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>

        <a href="/">Go Back to Login Page</a>
    </div>
</body>
</html>

"""

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
