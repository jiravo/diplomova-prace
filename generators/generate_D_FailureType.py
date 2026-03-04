import pandas as pd


def generate_D_FailureType():

    data = [
        (1, "Mechanická", "Mechanické opotřebení nebo selhání pohyblivých částí"),
        (
            2,
            "Přehřátí",
            "Nadměrná teplota způsobená zatížením nebo nedostatečným chlazením",
        ),
        (3, "Tlaková", "Nestabilita nebo výrazná změna tlaku v systému"),
        (4, "Elektrická", "Porucha elektrických komponent nebo řídicího systému"),
    ]

    df = pd.DataFrame(data, columns=["failure_type_id", "failure_type", "description"])

    df.to_csv("data/BI/D_FailureType.csv", index=False)

    return df
