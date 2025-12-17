def calculate_risk(attendance, marks_avg, quiz_avg):
    score = 0

    # Attendance impact
    if attendance < 75:
        score += 40

    # Marks impact
    if marks_avg < 50:
        score += 40

    # Quiz impact
    if quiz_avg < 50:
        score += 20

    if score >= 70:
        return "HIGH RISK"
    elif score >= 40:
        return "MEDIUM RISK"
    else:
        return "LOW RISK"
