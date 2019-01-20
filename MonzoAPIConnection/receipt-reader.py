import ReceiptsClient
import monzotools
import ocr
import receipt_parser


client = ReceiptsClient.ReceiptsClient()
client.do_auth()
client.list_transactions()

transactions = monzotools.transactionsWithImages(client.transactions)

for transaction in transactions:
    url = monzotools.getImageURL(transaction)
    parsed_image = ocr.image_to_text(url)
    items = receipt_parser.parsereceipt(parsed_image)
    receipt = monzotools.genReceipt(transaction, items)
    client.add_receipt_data(transaction, receipt)