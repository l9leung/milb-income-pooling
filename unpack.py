import pandas as pd


def unpack_active_roster(payrolls):
    activeplayers = pd.DataFrame()
    for team in payrolls.keys():
        team_activeplayers = payrolls[team]["2021 Active Players"]
        team_activeplayers.rename(columns={team_activeplayers.columns[0]: "Active Players"},
                                  inplace=True)
        for j in range(5, 9):
            try:
                team_activeplayers.iloc[:, j] = team_activeplayers.iloc[:, j].str.replace("$", "")
                team_activeplayers.iloc[:, j] = team_activeplayers.iloc[:, j].str.replace(",", "")
                team_activeplayers.iloc[:, j] = team_activeplayers.iloc[:, j].astype(float)
            except AttributeError:
                pass
        team_activeplayers["Team"] = team
        activeplayers = pd.concat([activeplayers, team_activeplayers])
    return activeplayers.reset_index(drop=True)
