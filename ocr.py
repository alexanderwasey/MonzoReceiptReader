import http.client, urllib.request, urllib.parse, urllib.error, base64, json, time

# request headers
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'fbcc02faa1f04500b4275e49fba6bd62',
}

# request parameters
params = urllib.parse.urlencode({
    'mode': 'Printed',
})

body = {"url":"https://s3-eu-west-1.amazonaws.com/mondo-production-image-uploads/user_00009Vk182u7NXFlNmoBSz/ldPUTwxW7h6I4SKR5bHj-6f595092-3605-4937-88cc-e3c56e1cd5ed"}

try:
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v2.0/recognizeText?%s" % params, json.dumps(body) , headers)
    response = conn.getresponse()
    
    x = response.getheader('Operation-Location')
    time.sleep(5)
    
    try:
        # request parameters
        params2 = urllib.parse.urlencode({
            'operationId': x.split("/")[-1],
        })
        conn2 = http.client.HTTPSConnection("westcentralus.api.cognitive.microsoft.com")
        conn2.request("GET", "/vision/v2.0/textOperations/{operationId}?%s" % params2, "{body}", headers)
        response2 = conn2.getresponse()

        data2 = response2.read()
        z = json.loads(data2)
        
        #open the output file for writing
        dataFile = open('scanned-chars.txt', 'w')
        
        # loop through each item in the list
        # and write it to the output file
        for item in z["recognitionResult"]["lines"]:
            #item = json.loads(item)
            print(item["text"])
            dataFile.write(str(item["text"])+'\n')
            
        # close the output file
        dataFile.close()
        
        conn2.close()
    except Exception as e:    
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    
    conn.close()
except Exception as e:
   print("[Errno {0}] {1}".format(e.errno, e.strerror))


   

    
    
