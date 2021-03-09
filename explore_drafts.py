import json
import pandas as pd
import matplotlib.pyplot as plt

# Load 2021 MLB salary data
mlb = pd.read_csv("MLB_activeplayers.csv")
mlb.columns
# Median 2021 MLB salary
mlb_contract = mlb["Adj. Salary"].median()
# Plot distribution of 2021 MLB salaries
plt.figure()
plt.hist(mlb["Adj. Salary"]/10**6, alpha=0.5, edgecolor="k")
plt.xlabel("Salary (millions)")
plt.ylabel("Count")
plt.title("Distribution of MLB Salaries (2021)")
plt.savefig("mlb_salary_2021.png", bbox_inches="tight", dpi=720)
plt.show()

# Load historical draft data
with open("MLB_draft_history.json") as file:
    hitters = json.load(file)
# Calculate historical percent of players who play in MLB at each draft pick
percentages = pd.DataFrame(index=hitters.keys(), columns=["Majors"],
                           dtype="float64")
percentages["Pick"] = pd.to_numeric(percentages.index)
pick_thresh = 100
year_thresh = 2015
for position in hitters.keys():
    picks = pd.DataFrame(hitters[position]).transpose()
    picks = picks[picks["Year"] <= year_thresh]
    majors_pct = len(picks[(picks["G"] >= pick_thresh) |
                           (picks["G.1"] >= pick_thresh)])
    percentages.loc[position, "Majors"] = majors_pct/len(picks)
# Plot MLB appearances by draft pick
maxpick = 400
plt.figure(figsize=(15, 4), dpi=480)
plt.bar(percentages[percentages["Pick"] <= maxpick]["Pick"],
        percentages[percentages["Pick"] <= maxpick]["Majors"]*100,
        align="edge",
        alpha=0.6)
plt.xticks([1] + [x for x in range(50, maxpick+1, 50)])
plt.xlabel("Overall Pick Number")
plt.ylabel("Percent")
plt.title(f"Percentage of Players With >{pick_thresh} Games Played in MLB At Each Pick Number")
plt.savefig("majors_by_draft_position.png", bbox_inches="tight")
plt.show()

# All items in U.S. city average, all urban consumers, not seasonally adjusted
cpi = pd.read_csv("CUUR0000SA0.csv", index_col=0)
# Calculate average CPI adjusted bonus by draft pick
bonuses = pd.DataFrame(index=hitters.keys(), columns=["Bonus"],
                       dtype="int64")
bonuses["Pick"] = pd.to_numeric(bonuses.index)
year_thresh = 2000
for position in hitters.keys():
    picks = pd.DataFrame(hitters[position]).transpose()
    picks = picks[picks["Year"] >= year_thresh]
    picks["Bonus"] = picks["Bonus"].str.replace("$", "")
    picks["Bonus"] = picks["Bonus"].str.replace(",", "")
    picks["Bonus"] = pd.to_numeric(picks["Bonus"])
    picks["Year"] = pd.to_numeric(picks["Year"])
    picks["Bonus"] = picks.apply(lambda x: x["Bonus"] * (cpi.loc[2020, "Annual"]/cpi.loc[x["Year"], "Annual"]),
                                 axis=1)
    bonuses.loc[position, "Bonus"] = picks["Bonus"].mean()
# Plot average bonus by draft pick
plt.figure(figsize=(15, 4), dpi=480)
plt.bar(bonuses[bonuses["Pick"] <= maxpick]["Pick"],
        bonuses[bonuses["Pick"] <= maxpick]["Bonus"]/10**6,
        align="center",
        alpha=0.6)
plt.xticks([1] + [x for x in range(50, maxpick+1, 50)])
plt.xlabel("Overall Pick Number")
plt.ylabel("Bonus (millions)")
plt.title("Average Inflation Adjusted Signing Bonus By Pick Number (in 2020 dollars)")
plt.savefig("bonus_by_draft_position.png", bbox_inches="tight")
plt.show()
