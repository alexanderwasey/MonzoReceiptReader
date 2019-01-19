import json
import uuid

import sys

import requests

import config
import oauth2
import receipt_types
import monzotools 
from utils import error

class ReceiptsClient:
    ''' An example single-account client of the Monzo Transaction Receipts API. 
        For the underlying OAuth2 implementation, see oauth2.OAuth2Client.
    '''

    def __init__(self):
        self._api_client = oauth2.OAuth2Client()
        self._api_client_ready = False
        self._account_id = None
        self.transactions = []


    def do_auth(self):
        ''' Perform OAuth2 flow mostly on command-line and retrieve information of the
            authorised user's current account information, rather than from joint account, 
            if present.
        '''

        print("Starting OAuth2 flow...")
        self._api_client.start_auth()

        print("OAuth2 flow completed, testing API call...")
        response = self._api_client.test_api_call()
        if "authenticated" in response:
            print("API call test successful!")
        else:
            error("OAuth2 flow seems to have failed.")
        self._api_client_ready = True

        print("Retrieving account information...")
        success, response = self._api_client.api_get("accounts", {})
        if not success or "accounts" not in response or len(response["accounts"]) < 1:
            error("Could not retrieve accounts information")
        
        # We will be operating on personal account only.
        for account in response["accounts"]:
            if "type" in account and account["type"] == "uk_retail":
                self._account_id = account["id"]
                print("Retrieved account information.")
                return

        if self._account_id is None:
            error("Could not find a personal account")
    

    def list_transactions(self):
        ''' An example call to the end point documented in
            https://docs.monzo.com/#list-transactions, other requests 
            can be implemented in a similar fashion. 
        '''
        if self._api_client is None or not self._api_client_ready:
            error("API client not initialised.")

        # Our call is not paginated here with e.g. "limit": 10, which will be slow for
        # accounts with a lot of transactions.
        success, response = self._api_client.api_get("transactions", {
            "account_id": self._account_id,
        })

        if not success or "transactions" not in response:
            error("Could not list past transactions ({})".format(response))
        
        self.transactions = response["transactions"]
        print("All transactions loaded.")
        

    def read_receipt(self, receipt_id):
        ''' Retrieve receipt for a transaction with an external ID of our choosing.
        '''
        success, response = self._api_client.api_get("transaction-receipts", {
            "external_id": receipt_id,
        })
        if not success:
            error("Failed to load receipt: {}".format(response))
        
        print("Receipt read: {}".format(response))

    
    def add_receipt_data(self, transaction, receipt):
        receipt_marshaled = receipt.marshal()
        receipt_id = transaction["id"] + "ID"

        success, response = self._api_client.api_put("transaction-receipts/", receipt_marshaled)
        if not success:
            error("Failed to upload receipt: {}".format(response))
        print("Successfully uploaded receipt {}: {}".format(receipt_id, response))

    #Need to update with proper data source, but once we can do that should be good
    def add_data_image_receipts(self, transactions):
        imgtransactions = monzotools.transactionsWithImages(transactions)

        for transaction in imgtransactions:
            receipt_id = transaction["id"] + "ID"

            #TESTTESTTEST
            example_items = [monzotools.genItem("Testing testing", 1, 200)]
            payments = [monzotools.genPayment(transaction)]
            receipt = receipt_types.Receipt("", receipt_id, transaction["id"], 
            abs(transaction["amount"]), "GBP", payments, [], example_items)
            client.add_receipt_data(transaction, receipt)
            




if __name__ == "__main__":
    client = ReceiptsClient()
    client.do_auth()
    client.list_transactions()    
    client.add_data_image_receipts(client.transactions)

    
    
            
        
    