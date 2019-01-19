import json
import uuid

import sys

import config
import oauth2
import receipt_types
from utils import error


def getImageURL(transaction):
    #Get attachments of file
    attachments = transaction["attachments"]
    if (len(attachments) == 0):
        return None
    else: 
        return attachments[0]["file_url"]

def transactionsWithImages(transactions):
    validTransactions = list()
    for transaction in transactions:
        if (len(transaction["attachments"]) > 0):
                validTransactions.append(transaction)
    return validTransactions

def printURLS(transactions):
    for transaction in transactions:
            print(getImageURL(transaction))

def genPayment(transaction):
    #Generates payment info based on a transaction
    payment = receipt_types.Payment("card", "", "", "", "", "", "", "", abs(transaction["amount"]), "GBP")
    return payment