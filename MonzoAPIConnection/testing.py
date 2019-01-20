import ocr
import receipt_parser

parsedimage = ocr.image_to_text("https://i.imgur.com/h8yyhst.jpg")
print(parsedimage)
parsedtext = receipt_parser.parsereceipt(parsedimage)
print(parsedtext)
print (receipt_parser.findVAT(parsedimage))

