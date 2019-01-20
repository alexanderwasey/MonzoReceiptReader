import ReceiptsClient
import monzotools
import ocr
import receipt_parser
import sys
import receipt_types
import time

client = ReceiptsClient.ReceiptsClient()
client.do_auth()


while(True):
    usedImages = []
    
    client.list_transactions()
    transactions = monzotools.transactionsWithImages(client.transactions)

    #If command line arguments given then in reset mode
    reset = False
    if len(sys.argv) > 1:
        reset = True


    for transaction in transactions:
        
        if (reset):
            client.add_junk_data_receipt(transaction)
        else: 
            id = monzotools.getImageID(transaction)
            
            if (id not in usedImages):
            
                url = monzotools.getImageURL(transaction)
                parsed_image = ocr.image_to_text(url)
                items = receipt_parser.parsereceipt(parsed_image)
                receipt = monzotools.genReceipt(transaction,[], items)

                #get VAT
                vatNo = receipt_parser.findVAT(parsed_image)
                
                if vatNo != None:
                    vatamount = int(transaction["amount"] * -0.2)
                    vat = [receipt_types.Tax("VAT", vatamount, "GBP", vatNo)]
                    receipt = monzotools.genReceipt(transaction, vat, items)

                client.add_receipt_data(transaction, receipt)
                usedImages.append(id)
    if (reset == True):
        break

time.sleep(10)