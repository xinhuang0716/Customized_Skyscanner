## import packages
from utilities.airline import TigerQuery
from utilities.optimal import OptimalTrip
import json, warnings, pandas as pd
warnings.filterwarnings("ignore")

## airport code
airport_dict = json.load(open("./config/airport.json", encoding="utf-8-sig"))

## query
df_tiger_go = pd.concat([TigerQuery(i, "2024-09-30", "2024-12-31") for i in list(airport_dict.keys())] + 
                        [TigerQuery(i, "2025-01-01", "2025-03-31") for i in list(airport_dict.keys())])
df_tiger_back = pd.concat([TigerQuery(i, "2024-09-30", "2024-12-31", False) for i in list(airport_dict.keys())] + 
                          [TigerQuery(i, "2025-01-01", "2025-03-31", False) for i in list(airport_dict.keys())])

## data preprocessing
print("/n**Completed**/n")
df = pd.concat([df_tiger_go, df_tiger_back])

## output
df.to_csv("./data/result_tiger.csv", index = False, encoding = "utf-8-sig")
