# **🌍 Vaccination Data Analysis and Visualization**

Analysis of global vaccination coverage, disease incidence, and vaccine introduction trends using WHO/UNICEF datasets — cleaned in Python, stored in a normalized SQL database, and explored through an interactive dashboard.

Domain: Public Health & Epidemiology Skills: Python (Pandas, EDA), SQL (Database Design), Data Visualization (Streamlit/Plotly)

---
# ***📌 Project Overview***

This project analyzes global vaccination data to understand trends in vaccination coverage, disease incidence, and effectiveness. Raw WHO/UNICEF data was cleaned and normalized, stored in a relational SQL database, and visualized through an interactive dashboard to surface insights for public health strategy, disease prevention, and resource allocation.

---
# ***🛠️ Tech Stack***
Python — pandas, numpy, openpyxl (data cleaning & EDA)

SQL — PostgreSQL (relational database, normalized schema)

SQLAlchemy / psycopg2 — Python–database connectivity

Matplotlib / Seaborn — exploratory data analysis visualizations

Streamlit + Plotly — interactive dashboard (filters, KPI cards, trend lines, choropleth map, scatter plots)

---
# ***📂 Project Structure***

DS-Vaccination-Project/
├── data/
│   ├── raw/                  # Original source Excel files
│   └── cleaned/               # Cleaned CSVs (output of cleaning notebook)
├── notebooks/
│   ├── eda_analysis.ipynb     # Data profiling, cleaning, and EDA
│   ├── SQL_database.py        # Schema creation / one-off SQL fixes
│   └── load_data.py           # Loads cleaned data into the SQL database
├── dashboard.py                # Streamlit interactive dashboard
├── docs/
│   ├── Vaccination_Project_Documentation.docx   # Cleaning decisions, schema, challenges
│   └── Vaccination_Project_Question_Answers.pdf # Answers to all brief questions
├── requirements.txt
└── README.md

---
# ***📊 Dataset***

Five source tables (WHO/UNICEF vaccination data):

Table	                                       Records	                                                                      Description
Coverage data	                               ~400K	                                                         Vaccination coverage % by country, year, antigen
Incidence rate data	                          ~85K	                                                        Disease incidence rate by country, year, disease
Reported cases data	                          ~85K	                                                                   Raw disease case counts
Vaccine introduction data	                    ~138K	                                                             National vaccine introduction status/year
Vaccine schedule data	                         ~8K	                                                        National dosing schedules and target populations

---
# ***🧹 Data Cleaning Highlights***
Removed incomplete/junk records (missing country code or year)
Retained genuine missing coverage values as null rather than imputing false data
Standardized column names, whitespace, and date types across all tables
Documented and explained anomalies (e.g. coverage >100% due to WHO's known denominator-estimation quirk) rather than silently deleting them

See docs/Vaccination_Project_Documentation.docx for the full reasoning behind every cleaning decision.

---
# ***🗄️ Database Design***

Normalized PostgreSQL schema:

Lookup tables: countries, vaccines, diseases
Fact tables: coverage, incidence, reported_cases, vaccine_introduction, vaccine_schedule
Primary/foreign keys enforced for referential integrity

# ***📈 Dashboard Features***

Run locally via Streamlit:

1.Filters: WHO Region, Vaccine, Year Range

2.KPI cards: total records, average coverage %, % of records ≥95% coverage

3.Trend line: global vaccination coverage over time

4.Choropleth map: coverage by country

5.Scatter plot: coverage vs. disease incidence correlation

6.Bar charts: top/bottom 10 countries by average coverage

---
# ***🚀 Setup & Usage***
### 1. Clone the repo and install dependencies:
```bash
   pip install -r requirements.txt
```
### 2. Set up PostgreSQL and create a database named vaccination_db.
### 3. Run the cleaning notebook (notebooks/eda_analysis.ipynb) to generate cleaned CSVs in data/cleaned/.
### 4. Create the schema and load data:
```bash
   python notebooks/SQL_database.py
   python notebooks/load_data.py
```
#### (Update the database password in both files before running.)

### 4. Launch the dashboard:
```bash
   streamlit run dashboard.py
```
   ---
# ***🔍 Key Insights***
1.Global average vaccination coverage rose from ~45% (1980) to ~80% (mid-2000s), with dips around 2010 and 2020 (COVID-19 disruption).

2.Coverage and disease incidence show a negative correlation (-0.19), strongest for measles and pertussis.

3.Global measles coverage (87.6%) remains 7.4 points below WHO's 95%-by-2030 target.

4.Polio cases fell ~98.9% comparing 1980–90 vs. 2015–23 averages — the largest reduction of any disease tracked.

Full question-by-question analysis: (https://drive.google.com/file/d/1HOau1Qd3FL9LXwGntz2bILKScLKKgjgn/view?usp=drive_link)

---
# ***📑Project Report***

(https://drive.google.com/file/d/1PPGMF7AaCc7XuHyREzFa2JAcu10HOrQq/view?usp=drive_link)

# ***📽Project Demo***

(https://drive.google.com/file/d/1wlKPmj-hQvF2Kc6l8IZYgb3iWaGGl52l/view?usp=drive_link)

---
# ***⚠️ Known Limitations***
1.No gender, education level, urban/rural, or population density fields exist in the source data — related brief questions are documented as not answerable with this dataset.
2.vaccine_introduction / vaccine_schedule vaccine names are stored as free text rather than a foreign key, due to inconsistent naming conventions vs. the coverage table's antigen codes.

