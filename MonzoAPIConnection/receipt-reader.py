import ReceiptsClient
import monzotools
import ocr
import receipt_parser
import sys


client = ReceiptsClient.ReceiptsClient()
client.do_auth()
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
        url = monzotools.getImageURL(transaction)
        parsed_image = ocr.image_to_text(url)
        items = receipt_parser.parsereceipt(parsed_image)
        receipt = monzotools.genReceipt(transaction, items)
        client.add_receipt_data(transaction, receipt)