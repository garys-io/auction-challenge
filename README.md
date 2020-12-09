# Auction Coding Challenge in Python3

## Steps to run the auction using the repo files

* Assuming you have cloned the repo in `~/projects`
* `docker build -t challenge .`
* `docker run -i -v ~/projects/auction-challenge/config.json:/auction/config.json challenge:latest < ./input.json`
* Runnig without docker `python -m auction.main`