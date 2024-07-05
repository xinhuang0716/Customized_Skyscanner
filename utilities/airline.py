## import packages
import json, requests, pandas as pd, datetime as dt


## function tiger airline
def TigerQuery(
    destination: str,
    start_date: str,
    end_date: str,
    go: bool = True,
    payload_path: str = "./config/payload.json",
    airport_path: str = "./config/airport.json",
    API_url: str = "https://api-book.tigerairtw.com/graphql",
) -> pd.DataFrame:
    """
    use api to fetch tiger airline information,
    the maximum of query perriod(start 2 end) is six months
    """

    # load configs
    airport_dict = json.load(open(airport_path, encoding="utf-8-sig"))
    payload = json.load(open(payload_path, encoding="utf-8-sig"))
    payload_var = payload["variables"]
    if go:
        payload_var["input"]["destination"] = destination
    else:
        payload_var["input"]["destination"] = "TPE"
        payload_var["input"]["origin"] = destination
    payload_var["input"]["since"] = start_date
    payload_var["input"]["until"] = end_date
    payload["variables"] = json.dumps(payload_var)

    # query
    res = requests.post(API_url, json=payload, verify=False)
    result = pd.DataFrame.from_dict(res.json()["data"]["appLiveDailyPrices"])

    # data preprocessing
    result["destination"] = result["destination"].apply(
        lambda x: "台北" if x == "TPE" else airport_dict[x]
    )
    result["origin"] = result["origin"].apply(
        lambda x: "台北" if x == "TPE" else airport_dict[x]
    )

    result['星期'] = result['date'].apply(lambda x : dt.datetime.strptime(x, '%Y-%m-%d').strftime("%A")[:3].upper())
    result["往返"] = "去程" if go else "回程"
    
    result = result.rename(
        columns={
            "origin": "出發地" if go else "目的地",
            "destination": "目的地" if go else "出發地",
            "date": "日期",
            "amount": "金額",
        }
    )

    return result.drop(["fareLabels", "currency"], axis=1)


def PeachQuery():
    return 0
