from database import (
    get_leave_balance,
    count_approved_leaves
)


def check_leave(employee_id, leave_date):

    balance = get_leave_balance(employee_id)

    if balance <= 0:
        return "Rejected", "Insufficient Leave Balance"

    blocked_dates = [
        "2026-12-31",
        "2026-11-30"
    ]

    if leave_date in blocked_dates:
        return "Rejected", "Blackout Date"

    approved_count = count_approved_leaves(leave_date)

    if approved_count >= 3:
        return "Rejected", "Daily Leave Limit Reached"

    return "Approved", "Request Meets All Rules"