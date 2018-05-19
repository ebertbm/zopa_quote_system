#!/usr/bin/env python
import csv
import numpy as np
import sys
from operator import itemgetter


def get_best_rate(input, loan_amount):
    """
    This borrow all the money available for each lender that have the best rates available.
    :param input: The location of the market file
    :param loan_amount: the requested loan amount
    :return:
    """
    market = []
    rates = []
    sum_lend = 0
    total_money_available = 0
    f = open(input)
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        lender = {'name': row[0],
                  'rate': float(row[1]),
                  'available': float(row[2]),
                  'original_available': float(row[2]),
                  'lent': 0
                  }
        total_money_available += lender['available']
        market.append(lender)

    # sort by the lowest rate
    market = sorted(market, key=itemgetter('rate'))

    # Make sure that the market has enough money to provide the requested loan
    if total_money_available > loan_amount:
        # loop through all the lenders until the lend has achieved
        while sum_lend != loan_amount:
            for lender in market:
                # A lender that has less than the amount left to lend
                # will give everything, otherwise another lender with more money
                # will give the rest.
                if sum_lend < loan_amount:
                    if lender['available'] < (loan_amount - sum_lend):
                        sum_lend += lender['available']
                        lender['lent'] = lender['lent'] + lender['available']
                        lender['available'] = 0
                    else:
                        # substract the lent amount
                        lender['available'] = lender['available'] - (loan_amount - sum_lend)
                        lender['lent'] = lender['lent'] + (loan_amount - sum_lend)
                        sum_lend += (loan_amount - sum_lend)
                    # this is the rate based on the % that was lent
                    rate_per_lent = (lender['lent'] / loan_amount) * lender['rate']
                    rates.append(rate_per_lent)
        return sum(rates)
    else:
        return None


def get_distributed_rate(input, loan_amount):
    """
    This is another approach that although gives a higher rates, it gives the opportunity to all
    the lenders to have a share in the loand. The function calculates the rate taking 2% of
    all available money of each lender, if does not reach the requested loan amount by
    the borrower on the first iteration, it keeps iterating until gets the desired amount.
    This gives priority to the lenders with the best rates
    :param input: The location of the market file
    :param loan_amount: the requested loan amount
    :return:
    """
    market = []
    rates = []
    sum_lend = 0
    total_money_available = 0
    f = open(input)
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        lender = {'name': row[0],
                  'rate': float(row[1]),
                  'available': float(row[2]),
                  'original_available': float(row[2]),
                  'lent': 0
                  }
        total_money_available += lender['available']
        market.append(lender)

    # sort by the lowest rate
    market = sorted(market, key=itemgetter('rate'))

    # Make sure that the market has enough money to provide a loan
    if total_money_available > loan_amount:
        # loop through all the lenders until the lend has achieved
        while sum_lend != loan_amount:
            for lender in market:
                # check if the next 10% increase of the amount lent is still lower
                # to loan amount requested
                if sum_lend + sum_lend * 0.1 < loan_amount:
                    if lender['available'] > 0:
                        amount_to_lend = lender['original_available'] * 0.02
                        lender['available'] = lender['available'] - amount_to_lend
                        lender['lent'] = lender['lent'] + amount_to_lend
                        rates.append(lender['rate'])
                        sum_lend += amount_to_lend
                    else:
                        print("{} - does not have more money!!".format(lender['name']))
                else:
                    # A lender that has less than the amount left to lend
                    # will give everything, otherwise another lender with more money
                    # could give the rest.
                    if lender['available'] < (loan_amount - sum_lend):
                        sum_lend += lender['available']
                        lender['available'] = 0
                        lender['lent'] = lender['lent'] + lender['available']
                    else:
                        lender['available'] = lender['available'] - (loan_amount - sum_lend)
                        lender['lent'] = lender['lent'] + (loan_amount - sum_lend)
                        sum_lend += (loan_amount - sum_lend)
                    rates.append(lender['rate'])

        return sum(rates) / len(rates)
    else:
        return None


def calculate_monthly_repayments(rate, loan_amount, number_of_payments):
    """
    Calculate the monthly repayments with numpy function
    :param rate: rate calculated
    :param loan_amount: request loan amount
    :param number_of_payments: number of all payments
    :return:
    """
    return round(np.pmt(rate / 12, number_of_payments, -loan_amount), 2)

def calculate_total_repayment(monthly_repayments, number_of_payments):
    """
    Calculate the total repayment
    :param monthly_repayments: amount of monthly repayments
    :param number_of_payments: number of payments
    :return:
    """

    return round(monthly_repayments * number_of_payments, 2)

if __name__ == '__main__':
    input = sys.argv[1]
    loan_amount = float(sys.argv[2])
    number_of_payments = 36

    rate = get_best_rate(input, loan_amount)

    if rate is None:
        print("Sorry, it is not possible to provide a quote this time.")
    else:
        monthly_repayments = calculate_monthly_repayments(rate, loan_amount, number_of_payments)
        total_repayment = calculate_total_repayment(monthly_repayments, number_of_payments)
        print("Requested amount: £{} \n"
              "Rate: {}% \n"
              "Monthly repayment: £{} \n"
              "Total repayment: £{}".format(loan_amount,
                                           round(rate * 100, 1),
                                           monthly_repayments,
                                           total_repayment))
