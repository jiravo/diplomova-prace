import pandas as pd


def generate_D_Technician():

    technicians = [
        (1, "Jan Novák", "manažer údržby", "senior", 550, "Central"),
        (2, "Petr Svoboda", "údržba", "senior", 370, "Team A"),
        (3, "Martin Dvořák", "údržba", "pokročilý", 350, "Team A"),
        (4, "Tomáš Král", "údržba", "junior", 320, "Team C"),
        (5, "Lukáš Procházka", "údržba", "pokročilý", 350, "Team B"),
        (6, "David Beneš", "údržba", "junior", 320, "Team B"),
        (7, "Ondřej Veselý", "údržba", "pokročilý", 350, "Team C"),
        (8, "Michal Černý", "elektro-údržba", "senior", 420, "Team A"),
        (9, "Jiří Kučera", "elektro-údržba", "pokročilý", 390, "Team B"),
        (10, "Pavel Horák", "elektro-údržba", "pokročilý", 390, "Team C"),
        (11, "Externí technik", "externí specialista", "expert", 850, "External"),
    ]

    df = pd.DataFrame(
        technicians,
        columns=[
            "technician_id",
            "technician_name",
            "specialization",
            "seniority_level",
            "hourly_rate",
            "team",
        ],
    )

    df.to_csv("data/BI/D_Technician.csv", index=False)

    return df
