import json
from itertools import combinations
from math import factorial
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def payoff_nopool(p=0.06,
                  MLB_contract=4158333, minor_contract=6600, thresh=1500000):
    """Expected value and variance of the salary a player will get without
    pooling."""
    E_nopool = MLB_contract*p + minor_contract * (1-p)
    E_nopool_var = (MLB_contract - E_nopool)**2 * p + (minor_contract - E_nopool)**2 * (1-p)
    return E_nopool, E_nopool_var**0.5


def payoff_n(n=3, p=0.06,
             MLB_contract=4158333, minor_contract=6600, thresh=1500000):
    """Expected value and variance of the salary a player will get from
    pooling with n players. Assume each player has the same probability p of
    reaching the major leagues."""
    distribution = []
    for n_makers in range(n + 1):  # For every number of possible players who make it
        if n_makers == 0:
            distribution.append((minor_contract, (1-p)**n))
        elif n_makers == n:
            distribution.append((MLB_contract, p**n))
        else:
            # number of combinations of players who make it
            n_combinations = factorial(n)
            n_combinations /= (factorial(n-n_makers)*factorial(n_makers))
            n_combinations = int(n_combinations)

            # number of combinations where player 1 makes it
            n_indv_inmajors = factorial(n-1)
            n_indv_inmajors /= (factorial((n-1)-(n_makers-1))*factorial(n_makers-1))
            n_indv_inmajors = int(n_indv_inmajors)

            # probability that n_makers of players make it
            payoff_prob = p**n_makers * (1-p)**(n-n_makers)

            # payoff when player 1 is one of the players who makes it
            payoff = MLB_contract - 0.1*(MLB_contract-thresh)
            payoff += (n_makers-1)*0.1*(MLB_contract-thresh)/(n-1)
            distribution.append((payoff, payoff_prob*n_indv_inmajors))

            # payoff when player 1 is not one of the players who makes it
            payoff = minor_contract
            payoff += n_makers*0.1*(MLB_contract-thresh)/(n-1)
            distribution.append((payoff, payoff_prob*(n_combinations-n_indv_inmajors)))
    E_payoff = [a*b for (a, b) in distribution]
    E_payoff = sum(E_payoff)
    var_payoff = [((a-E_payoff)**2)*b for (a, b) in distribution]
    var_payoff = sum(var_payoff)
    return E_payoff, var_payoff**0.5


# Plot change in std dev as pool size increases
max_pool = 20
E_payoffs = []
var_payoffs = []
for n in range(1, max_pool + 1):
    E_payoff, var_payoff = payoff_n(n=n, p=0.06)
    E_payoffs.append(E_payoff)
    var_payoffs.append(var_payoff)
plt.figure(dpi=720)
# plt.scatter(range(1, max_pool + 1), var_payoffs)
plt.plot(range(2, max_pool + 1), [x/10**3 for x in var_payoffs[1:]],
         linewidth=2, alpha=0.5)
plt.xlabel("size of pool")
plt.xticks(range(0, max_pool + 1, 2))
plt.ylabel("standard deviation (thousands)")
plt.title("Standard Deviation In Salary vs. Pool Size (all $p_i=6\%$)")
plt.savefig("std.png", bbox_inches="tight")
plt.show()


def payoff_n_p(p, n=3,
               MLB_contract=4158333, minor_contract=6600, thresh=1500000):
    """Expected value and variance of the salary a player will get from
    pooling with n players. Each player has their own unique probability p
    of reaching the major leagues."""
    distribution = []
    for n_makers in range(n + 1):
        if n_makers == 0:
            payoff_prob = [1 - prob for prob in p.values()]
            payoff_prob = np.prod(payoff_prob)
            distribution.append((minor_contract, payoff_prob))
        elif n_makers == n:
            payoff_prob = [prob for prob in p.values()]
            payoff_prob = np.prod(payoff_prob)
            distribution.append((MLB_contract, payoff_prob))
        else:
            makers = list(combinations(range(1, n + 1), n_makers))
            for maker_set in makers:
                if 1 in maker_set:
                    payoff = MLB_contract - 0.1*(MLB_contract-thresh)
                    payoff += (n_makers-1)*0.1*(MLB_contract-thresh)/(n-1)
                    payoff_prob = [p[player] for player in maker_set]
                    payoff_prob += [1-p[player] for player in p.keys() if player not in maker_set]
                    payoff_prob = np.prod(payoff_prob)
                    distribution.append((payoff, payoff_prob))
                else:
                    payoff = minor_contract
                    payoff += n_makers*0.1*(MLB_contract-thresh)/(n-1)
                    payoff_prob = [p[player] for player in maker_set]
                    payoff_prob += [1-p[player] for player in p.keys() if player not in maker_set]
                    payoff_prob = np.prod(payoff_prob)
                    distribution.append((payoff, payoff_prob))
    E_payoff = [a*b for (a, b) in distribution]
    E_payoff = sum(E_payoff)
    var_payoff = [((a-E_payoff)**2)*b for (a, b) in distribution]
    var_payoff = sum(var_payoff)
    return E_payoff, var_payoff**0.5


def calc_pool(players):
    """
    Calculate the expected value and variance of salary all players in the
    input pool.
    Parameters
    ----------
    players : List containing the draft position of each player.

    Returns
    -------
    None.

    """
    players = [str(x) for x in players]
    n = len(players)
    for player in players:
        nopool = payoff_nopool(p=percentages[player])
        print(nopool)
        p = {i: percentages[key] for i, key in zip([x for x in range(2, n+1)],
                                                   [x for x in players if x != player])}
        p[1] = percentages[player]
        pool = payoff_n_p(p=p, n=n)
        print(pool)


if __name__ == "__main__":
    # Load historical draft data
    with open("MLB_draft_history.json") as file:
        hitters = json.load(file)
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
    # Import historical percent of players who play in MLB at each draft pick
    percentages = percentages["Majors"].to_dict()

    calc_pool([1, 50, 100, 200, 400])
