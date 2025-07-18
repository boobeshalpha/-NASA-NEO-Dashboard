import streamlit as st
import pandas as pd
import pymysql
from datetime import date

# Database connection
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='7904',
    database='nasa'
)

# Predefined SQL queries
predefined_queries = {
    "1. Count how many times each asteroid has approached Earth": """
        SELECT neo_reference_id, COUNT(*) AS approach_count
        FROM close_approach
        GROUP BY neo_reference_id
        ORDER BY approach_count DESC
    """,

    "2. Average velocity of each asteroid over multiple approaches": """
        SELECT neo_reference_id, AVG(relative_velocity_kmph) AS avg_velocity
        FROM close_approach
        GROUP BY neo_reference_id
        ORDER BY avg_velocity DESC
    """,

    "3. List top 10 fastest asteroids": """
        SELECT neo_reference_id, MAX(relative_velocity_kmph) AS max_velocity
        FROM close_approach
        GROUP BY neo_reference_id
        ORDER BY max_velocity DESC
        LIMIT 10
    """,

    "4. Potentially hazardous asteroids that approached Earth more than 3 times": """
        SELECT ca.neo_reference_id, COUNT(*) AS total_approaches
        FROM close_approach ca
        JOIN asteroids a ON ca.neo_reference_id = a.id
        WHERE a.is_potentially_hazardous_asteroid = TRUE
        GROUP BY ca.neo_reference_id
        HAVING COUNT(*) > 3
    """,

    "5. Find the month with the most asteroid approaches": """
        SELECT MONTH(close_approach_date) AS month, COUNT(*) AS total_approaches
        FROM close_approach
        GROUP BY MONTH(close_approach_date)
        ORDER BY total_approaches DESC
    """,

    "6. Asteroid with the fastest ever approach speed": """
        SELECT neo_reference_id, relative_velocity_kmph
        FROM close_approach
        ORDER BY relative_velocity_kmph DESC
        LIMIT 1
    """,

    "7. Asteroids sorted by max estimated diameter (descending)": """
        SELECT id, name, estimated_diameter_max_km
        FROM asteroids
        ORDER BY estimated_diameter_max_km DESC
    """,

    "8. Closest approach getting nearer over time (ordered by date + distance)": """
        SELECT neo_reference_id, close_approach_date, miss_distance_km
        FROM close_approach
        ORDER BY neo_reference_id, close_approach_date, miss_distance_km
    """,

    "9. Closest approach (name, date, distance)": """
        SELECT a.name, ca.close_approach_date, ca.miss_distance_km
        FROM close_approach ca
        JOIN asteroids a ON ca.neo_reference_id = a.id
        ORDER BY ca.miss_distance_km ASC
        LIMIT 1
    """,

    "10. Asteroids with velocity > 50,000 km/h": """
        SELECT DISTINCT a.name, ca.relative_velocity_kmph
        FROM close_approach ca
        JOIN asteroids a ON ca.neo_reference_id = a.id
        WHERE ca.relative_velocity_kmph > 50000
    """,

    "11. Count of approaches per month": """
        SELECT MONTH(close_approach_date) AS month, COUNT(*) AS approach_count
        FROM close_approach
        GROUP BY MONTH(close_approach_date)
        ORDER BY month
    """,

    "12. Brightest asteroid (lowest magnitude)": """
        SELECT id, name, absolute_magnitude_h
        FROM asteroids
        ORDER BY absolute_magnitude_h ASC
        LIMIT 1
    """,

    "13. Hazardous vs Non-hazardous asteroid count": """
        SELECT is_potentially_hazardous_asteroid, COUNT(*) AS total
        FROM asteroids
        GROUP BY is_potentially_hazardous_asteroid
    """,

    "14. Asteroids that passed closer than the Moon (< 1 LD)": """
        SELECT a.name, ca.close_approach_date, ca.miss_distance_lunar
        FROM close_approach ca
        JOIN asteroids a ON ca.neo_reference_id = a.id
        WHERE ca.miss_distance_lunar < 1
    """,

    "15. Asteroids that came within 0.05 AU": """
        SELECT a.name, ca.close_approach_date, ca.astronomical
        FROM close_approach ca
        JOIN asteroids a ON ca.neo_reference_id = a.id
        WHERE ca.astronomical < 0.05
    """
}

# Streamlit Layout
st.set_page_config(page_title="NASA NEO Dashboard", layout="wide")
st.title("🚀 NASA Near-Earth Object (NEO) Dashboard")

# Query Selection
st.sidebar.header("📌 Predefined SQL Queries")
query_option = st.sidebar.selectbox("Select a query", list(predefined_queries.keys()))
if st.sidebar.button("Run Query"):
    try:
        df = pd.read_sql(predefined_queries[query_option], connection)
        st.subheader("Query Result")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Query Error: {e}")

# Filters Section
st.sidebar.header("🔍 Filter-based Query")
start_date = st.sidebar.date_input("Start Date", date(2024, 1, 1))
end_date = st.sidebar.date_input("End Date", date(2024, 12, 31))
min_velocity = st.sidebar.slider("Min Velocity (km/h)", 0, 100000, 0)
max_au = st.sidebar.slider("Max Astronomical Units (AU)", 0.00, 1.00, 1.00)
max_ld = st.sidebar.slider("Max Lunar Distance (LD)", 0.0, 100.0, 100.0)
max_diameter = st.sidebar.slider("Max Diameter (km)", 0.0, 10.0, 10.0)
hazard_state = st.sidebar.selectbox("Hazardous?", ["All", "Yes", "No"])

if st.sidebar.button("Apply Filter"):
    query = f"""
        SELECT a.name, ca.close_approach_date, ca.relative_velocity_kmph,
               ca.astronomical, ca.miss_distance_lunar, a.estimated_diameter_max_km,
               a.is_potentially_hazardous_asteroid
        FROM close_approach ca
        JOIN asteroids a ON ca.neo_reference_id = a.id
        WHERE ca.close_approach_date BETWEEN '{start_date}' AND '{end_date}'
          AND ca.relative_velocity_kmph >= {min_velocity}
          AND ca.astronomical <= {max_au}
          AND ca.miss_distance_lunar <= {max_ld}
          AND a.estimated_diameter_max_km <= {max_diameter}
    """
    if hazard_state == "Yes":
        query += " AND a.is_potentially_hazardous_asteroid = TRUE"
    elif hazard_state == "No":
        query += " AND a.is_potentially_hazardous_asteroid = FALSE"

    try:
        df = pd.read_sql(query, connection)
        st.subheader("📊 Filtered Asteroid Data")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Filter Query Error: {e}")
