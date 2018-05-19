# Zopa calculation quote system
This is a small script that allows prospective borrowers to
obtain a quote from a pool of lenders for 36 month loans.
The script strives to provide as low a rate to the borrower as is possible.


## Installation requirements
2. Install Python 3.6 on your local machine.
3. Install Python requirements using: `pip3 install -r requirements.txt`

## Steps to Run the script
The script needs the following form to be able to run: `python3 quote.py [market_file] [loan_amount]`

For example:
```
$ python3 quote.py market.csv 1000
Requested amount: £1000
Rate: 7.0%
Monthly repayment: £30.78
Total repayment: £1108.10
```