import requests
from bs4 import BeautifulSoup
import pandas as pd
from unpack import unpack_active_roster


def get_team_pages():
    url = "https://www.spotrac.com/mlb/payroll/"
    r = requests.get(url)
    page = BeautifulSoup(r.content, "html.parser")
    teams_table = page.find_all("td")
    links = []
    for cell in teams_table:
        if cell.find("a") is not None:
            teamname = cell.find("a").get_text().strip("\n")
            teamname = teamname.split("\n")
            teamlink = cell.find("a").get("href")
            links.append(teamname + [teamlink])
    return links


def get_team_payrolls(teams):
    payrolls = {}
    for fullname, team, teamlink in teams:
        print("Getting " + fullname + " roster")
        payroll = {}

        payroll["fullname"] = fullname
        payroll["url"] = teamlink

        r = requests.get(teamlink)
        page = BeautifulSoup(r.content, "html.parser")
        headings = page.find_all("h2")
        teamtables = pd.read_html(r.content, na_values=["-"])
        payroll["2021 Active Players"] = teamtables[0]
        for teamtable, heading in zip(teamtables[1:], headings[1:len(teamtables)]):
            payroll[heading.get_text()] = teamtable

        payrolls[team] = payroll

    return payrolls


if __name__ == "__main__":
    teams = get_team_pages()
    payrolls = get_team_payrolls(teams)
    activeplayers = unpack_active_roster(payrolls)
    activeplayers.to_csv("activeplayers.csv")
