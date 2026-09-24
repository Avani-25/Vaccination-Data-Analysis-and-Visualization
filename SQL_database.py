from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:postgres@localhost:5432/vaccination_db')

with engine.connect() as conn:
    for table in ["countries", "vaccines", "diseases", "coverage", "incidence", "reported_cases", "vaccine_introduction", "vaccine_schedule"]:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
        print(table, ":", result.scalar())