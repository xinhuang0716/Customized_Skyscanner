## import packages
import pandas as pd


## function tiger airline
def OptimalTrip(nday: int, file_path: str = "./data/result_tiger.csv") -> pd.DataFrame:
    """
    transform raw data into more readable data for Tableau
    """
    # import data
    df = pd.read_csv(file_path).drop("出發地", axis=1)
    df = pd.merge(
        df[df["往返"] == "去程"].drop("往返", axis=1),
        df[df["往返"] == "回程"].drop("往返", axis=1),
        on=["目的地", "日期"],
        how="inner",
    ).rename({"金額_x": "去程金額", "金額_y": "回程金額"}, axis=1)

    # data preprocessing and some calculations
    df["回程金額 lead"] = df["回程金額"].shift(-(nday - 1))
    df = pd.concat([df[df["目的地"] == i].iloc[: -(nday - 1)] for i in df["目的地"].unique()])
    df["總金額"] = df["去程金額"] + df["回程金額 lead"]
    df = df[(df["去程金額"] != 0) & (df["回程金額 lead"] != 0)]
    df["yyyymm"] = df["日期"].apply(lambda x: x[:7])
    df = pd.concat(
        [
            df[df["yyyymm"] == i]
            .sort_values("總金額")
            .drop_duplicates(subset="目的地", keep="first")
            .head(3)
            for i in df["yyyymm"].unique()
        ]
    )
    df["旅程日期"], df["總金額"], df["Rank"] = (
        nday,
        df["總金額"].apply(lambda x: int(x)),
        sum([["Top1", "Top2", "Top3"][:i] for i in df['yyyymm'].value_counts()], []),
    )

    return df[["目的地", "日期", "總金額", "旅程日期", "Rank"]]
