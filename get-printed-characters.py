import requests
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
from io import BytesIO

subscription_key = "fbcc02faa1f04500b4275e49fba6bd62"
assert subscription_key
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

ocr_url = vision_base_url + "ocr"

# url of image you want to analyse
image_url = "https://s3-eu-west-1.amazonaws.com/mondo-production-image-uploads/user_00009Vk182u7NXFlNmoBSz/ldPUTwxW7h6I4SKR5bHj-6f595092-3605-4937-88cc-e3c56e1cd5ed"

headers = {'Ocp-Apim-Subscription-Key': subscription_key}
params  = {'language': 'unk', 'detectOrientation': 'true'}
data    = {'url': image_url}
response = requests.post(ocr_url, headers=headers, params=params, json=data)
response.raise_for_status()

analysis = response.json()

print(analysis)

# Extract the word bounding boxes and text.
line_infos = [region["lines"] for region in analysis["regions"]]
word_infos = []


for line in line_infos:
    for word_metadata in line:
        for word_info in word_metadata["words"]:
            word_infos.append(word_info)
word_infos

# open the output file for writing
dataFile = open('scanned-chars.txt', 'w')

# loop through each item in the list
# and write it to the output file
for eachitem in word_infos:
    dataFile.write(str(eachitem["text"])+'\n')

# close the output file
dataFile.close()

# Display the image and overlay it with the extracted text.
plt.figure(figsize=(5, 5))
image = Image.open(BytesIO(requests.get(image_url).content))
ax = plt.imshow(image, alpha=0.5)
for word in word_infos:
    bbox = [int(num) for num in word["boundingBox"].split(",")]
    text = word["text"]
    origin = (bbox[0], bbox[1])
    patch  = Rectangle(origin, bbox[2], bbox[3], fill=False, linewidth=2, color='y')
    ax.axes.add_patch(patch)
    plt.text(origin[0], origin[1], text, fontsize=20, weight="bold", va="top")
plt.axis("off")
#plt.show()




########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'fbcc02faa1f04500b4275e49fba6bd62',
}

params = urllib.parse.urlencode({
    # Request parameters
    'mode': 'Printed',
})

try:
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v2.0/recognizeText?%s" % params, {"url":"https://s3-eu-west-1.amazonaws.com/mondo-production-image-uploads/user_00009Vk182u7NXFlNmoBSz/ldPUTwxW7h6I4SKR5bHj-6f595092-3605-4937-88cc-e3c56e1cd5ed"}, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################
