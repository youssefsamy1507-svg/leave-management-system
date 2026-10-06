from flask import Flask, render_template, request

from database import (
    save_request,
    get_requests,
    deduct_leave_balance,
    get_all_employees
)

from rules import check_leave

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    employee_id = request.form["employee_id"]
    leave_date = request.form["leave_date"]
    leave_type = request.form["leave_type"]

    # Check leave rules
    status, reason = check_leave(
        employee_id,
        leave_date
    )

    # Deduct leave only if approved
    if status == "Approved":
        deduct_leave_balance(employee_id)

    # Save the request
    save_request(
        employee_id,
        leave_date,
        leave_type,
        status
    )

    return f"""
    <h2>Request Processed</h2>

    <p><strong>Employee ID:</strong> {employee_id}</p>

    <p><strong>Leave Date:</strong> {leave_date}</p>

    <p><strong>Leave Type:</strong> {leave_type}</p>

    <p><strong>Status:</strong> {status}</p>

    <p><strong>Reason:</strong> {reason}</p>

    <a href="/">Submit Another Request</a>
    """


@app.route("/admin")
def admin():

    requests = get_requests()

    html = """
    <h1>Leave Requests Dashboard</h1>

    <table border="1" cellpadding="10">
        <tr>
            <th>ID</th>
            <th>Employee ID</th>
            <th>Leave Date</th>
            <th>Leave Type</th>
            <th>Status</th>
        </tr>
    """

    for row in requests:

        html += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>{row[3]}</td>
            <td>{row[4]}</td>
        </tr>
        """

    html += "</table>"

    return html


@app.route("/employees")
def employees():

    employees = get_all_employees()

    html = """
    <h1>Employee Leave Balances</h1>

    <table border="1" cellpadding="10">
        <tr>
            <th>Employee ID</th>
            <th>Leave Balance</th>
        </tr>
    """

    for row in employees:

        html += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
        </tr>
        """

    html += "</table>"

    return html


if __name__ == "__main__":
    app.run(debug=True)
