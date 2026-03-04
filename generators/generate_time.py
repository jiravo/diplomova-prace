import pandas as pd
from config import *

# SCRIPT GENERUJE ČASOVOU ŘADU SPOLEČNOU PRO VŠECHNY TABULKY A BĚH FIRMY: time, D_Time

CZECH_DAYS = {
    "Monday": "Pondělí",
    "Tuesday": "Úterý",
    "Wednesday": "Středa",
    "Thursday": "Čtvrtek",
    "Friday": "Pátek",
    "Saturday": "Sobota",
    "Sunday": "Neděle",
}

CZECH_MONTHS = {
    "January": "Leden",
    "February": "Únor",
    "March": "Březen",
    "April": "Duben",
    "May": "Květen",
    "June": "Červen",
    "July": "Červenec",
    "August": "Srpen",
    "September": "Září",
    "October": "Říjen",
    "November": "Listopad",
    "December": "Prosinec",
}


def get_shift(hour):

    if 6 <= hour < 14:
        return 1, "Ranní", 6, 14
    elif 14 <= hour < 22:
        return 2, "Odpolední", 14, 22
    else:
        return 3, "Noční", 22, 6


def generate_time():

    time_index = pd.date_range(start=START_DATE, end=END_DATE, freq=FREQ)

    df_time = pd.DataFrame({"timestamp": time_index})

    df_time["date_key"] = df_time["timestamp"].dt.strftime("%Y%m%d").astype(int)
    df_time["date"] = df_time["timestamp"].dt.normalize()
    df_time["year"] = df_time["timestamp"].dt.year
    df_time["quarter"] = df_time["timestamp"].dt.quarter
    df_time["month"] = df_time["timestamp"].dt.month
    df_time["month_name"] = df_time["timestamp"].dt.month_name().map(CZECH_MONTHS)
    df_time["week"] = df_time["timestamp"].dt.isocalendar().week
    df_time["day"] = df_time["timestamp"].dt.day
    df_time["day_of_week"] = df_time["timestamp"].dt.day_name().map(CZECH_DAYS)
    df_time["day_of_week_number"] = df_time["timestamp"].dt.weekday + 1
    df_time["hour"] = df_time["timestamp"].dt.hour
    df_time["is_weekend"] = (df_time["timestamp"].dt.weekday >= 5).astype(int)

    # SHIFT LOGIC
    shifts = df_time["hour"].apply(get_shift)

    df_time["shift_id"] = shifts.apply(lambda x: x[0])
    df_time["shift_name"] = shifts.apply(lambda x: x[1])
    df_time["shift_start_hour"] = shifts.apply(lambda x: x[2])
    df_time["shift_end_hour"] = shifts.apply(lambda x: x[3])

    df_time.to_csv("data/Source/time.csv", index=False)
    df_time.to_csv("data/BI/D_Time.csv", index=False)

    return df_time
