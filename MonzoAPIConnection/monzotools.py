import json
import uuid

import sys

import config
import oauth2
import receipt_types
from utils import error

#Various util functions for dealing with Monzo

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
    #Generates payment info based on a transaction, presuming entire transaction done on card
    payment = receipt_types.Payment("card", "", "", "", "", "", "", "", abs(transaction["amount"]), "GBP")
    return payment

def genItem(description, quantity, price):
        item = receipt_types.Item(description, quantity, "", price, "GBP", 0, list() )
        return item

#This because to replace a receipt must use the same ID as previous
def genReceiptID(transaction):
        return transaction["id"] + "ID"

#Each item is a tuple of description, quantity, price
def genReceipt(transaction, items):
        receipt_id = genReceiptID(transaction)
        payments = [genPayment(transaction)]

        #Gen items in json format
        jsonitems = []
        for item in items:
                jsonitems.append(genItem(item[0], item[1], item[2]))
        
        receipt = receipt_types.Receipt("", receipt_id, transaction["id"], 
        abs(transaction["amount"]), "GBP", payments, [], jsonitems)

        return receipt
