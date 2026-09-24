import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:postgres@localhost:5432/vaccination_db')

who_regions = pd.read_csv("data/cleaned/who_regions.csv")

with engine.connect() as conn:
    for _, row in who_regions.iterrows():
        conn.execute(
            text("UPDATE countries SET who_region = :region WHERE iso_3_code = :code"),
            {"region": row["WHO_REGION"], "code": row["ISO_3_CODE"]}
        )
    conn.commit()

print(f"Updated who_region for {len(who_regions)} countries.")