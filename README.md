# 🚀 NASA Near-Earth Object (NEO) Dashboard

Hi, I’m Boobesh S. 👋  
This is my personal project where I built a dashboard using **Streamlit**, **SQL**, and **NASA’s NEO API**. It allows users to explore near-Earth asteroids using predefined SQL queries and dynamic filters.

## 📁 Project Structure

- `app.py` – Main Streamlit dashboard that connects to the MySQL database and displays asteroid data.
- `nasa.ipynb` – Notebook used to collect and process data from the NASA NEO API (before inserting into SQL).

## 💡 Features

- 15 Predefined SQL queries to analyze:
  - Fastest asteroids
  - Closest approaches
  - Hazardous object counts
  - Monthly patterns, brightness, etc.
- Sidebar filters to:
  - Select date range
  - Filter by velocity, diameter, hazard level, and more

## 🛠 Technologies Used

- Python
- Streamlit
- MySQL
- Pandas
- NASA Open API

## 📌 How to Run

```bash
pip install streamlit pymysql pandas
streamlit run app.py
