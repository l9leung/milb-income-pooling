import pandas as pd
import json


def scrape_drafts(stop=1740):
    drafts = {}
    for pick in range(1, stop + 1):
        print(f"Getting number {pick} picks overall")
        url = "https://www.baseball-reference.com/draft/?draft_type=junreg"
        url += f"&overall_pick={pick}&query_type=overall_pick"
        picks = pd.read_html(url)[0]
        picks = picks.drop(columns="FrRnd")
        picks["Name"] = picks["Name"].str.replace("(minors)", "", regex=False)
        picks["Name"] = picks["Name"].str.replace("*", "")
        picks["Name"] = picks["Name"].str.replace("#", "")
        picks["Name"] = picks["Name"].str.replace("+", "")
        picks["Name"] = picks["Name"].str.strip()
        picks.index = picks["Year"]
        picks = picks.groupby(picks.index).first()
        picks = picks.to_dict(orient="index")
        drafts[pick] = picks
    return drafts


if __name__ == "__main__":
    drafts = scrape_drafts()
    with open("MLB_draft_history", "w") as outfile:
        json.dump(drafts, outfile, indent=2)
