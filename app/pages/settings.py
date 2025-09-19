from dash import html
from database.db_methods import Users
import dash_ag_grid as dag
import pandas as pd

class SettingsPage:
    def __init__(self, users: Users):
        self.Users = users

    def layout(self) -> html.Div:
        users_res = self.Users.get_all_users()
        print(r for r in users_res)
        df = pd.DataFrame(users_res, columns=[users_res.columns])
        print(df)

        table = dag.AgGrid(
            rowData=df.to_dict("records"),
            columnDefs=[{"field": i} for i in df.columns]
        )

        return table