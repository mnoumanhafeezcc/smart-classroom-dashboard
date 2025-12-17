import streamlit as st
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Path fix to import risk calculator
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from analysis.risk_calculator import calculate_risk

# -------------------- UI Title --------------------
st.title("📊 Smart Classroom Analytics System")
st.subheader("📁 Upload your class data (CSV)")

# -------------------- CSV Upload --------------------
uploaded_file = st.file_uploader("Upload CSV file", type="csv")

if uploaded_file is not None:
    # Load uploaded CSV
    df_upload = pd.read_csv(uploaded_file)
    df = df_upload.copy()
else:
    # If no upload, fallback to default CSVs
    attendance = pd.read_csv("data/attendance.csv")
    marks = pd.read_csv("data/marks.csv")
    quizzes = pd.read_csv("data/quizzes.csv")
    df = attendance.merge(marks, on="student_id").merge(quizzes, on="student_id")

# -------------------- Risk Calculation --------------------
# Calculate average marks
df["marks_avg"] = (df["mid"] + df["final"]) / 2

# Calculate risk status
df["risk_status"] = df.apply(
    lambda x: calculate_risk(
        x["attendance_percentage"],
        x["marks_avg"],
        x["quiz_avg"]
    ),
    axis=1
)

# Advice column
def advice(row):
    if row['risk_status'] == "HIGH RISK":
        return "Immediate attention required"
    elif row['risk_status'] == "MEDIUM RISK":
        return "Monitor closely"
    else:
        return "On track"

df['advice'] = df.apply(advice, axis=1)

# Color function for risk
def color_risk(val):
    if val == "HIGH RISK":
        return 'background-color: #ff4d4d'  # red
    elif val == "MEDIUM RISK":
        return 'background-color: #ffec99'  # yellow
    else:
        return 'background-color: #b3ffb3'  # green

# -------------------- Display DataFrame --------------------
st.subheader("📊 Student Risk Report")
st.dataframe(df.style.applymap(color_risk, subset=['risk_status']))

# -------------------- Graph --------------------
st.subheader("📈 Attendance vs Average Marks")
plt.figure(figsize=(8,4))
sns.scatterplot(
    data=df,
    x="attendance_percentage",
    y="marks_avg",
    hue="risk_status",
    palette=["green","yellow","red"],
    s=100
)
plt.xlabel("Attendance (%)")
plt.ylabel("Average Marks")
plt.title("Attendance vs Average Marks by Risk")
st.pyplot(plt)

# -------------------- Filter + Download --------------------
risk_filter = st.selectbox("Filter by Risk Status", ["ALL", "HIGH RISK", "MEDIUM RISK", "LOW RISK"])
if risk_filter != "ALL":
    df_filtered = df[df["risk_status"] == risk_filter]
else:
    df_filtered = df

st.subheader("Filtered Student Report")
st.dataframe(df_filtered.style.applymap(color_risk, subset=['risk_status']))

# Download processed report
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Report as CSV",
    data=csv,
    file_name='student_risk_report.csv',
    mime='text/csv'
)
