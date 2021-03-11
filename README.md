## MiLB Income Pooling
Estimation of the expected value and standard deviation of professional baseball salaries with and without the income pooling scheme featured in [Episode 947](https://www.npr.org/2019/10/25/773493342/episode-947-some-of-the-money-ball) of Planet Money. Estimates are constructed using data scraped from [spotrac](https://www.spotrac.com/) and [Baseball-Reference](https://www.baseball-reference.com/). Data is used for academic purposes only.

## Organization
* `scrape_drafts.py`: scrapes all Major League Baseball Drafts since 1965 and each drafted player's career summary statistics
* `scrape_mlb_payrolls.py`: scrapes 2021 Major League Baseball payrolls
* `explore_drafts.py`: generates exploratory visualizations of the data
* `payoffs.py`: uses the scraped data to estimate the expected value and standard deviation of a drafted player's salary given their pool's constituents
