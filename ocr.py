import http.client, urllib.request, urllib.parse, urllib.error, base64, json, time, pprint

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'fbcc02faa1f04500b4275e49fba6bd62',
}

params = urllib.parse.urlencode({
    # Request parameters
    'mode': 'Printed',
})

body = {"url":"https://s3-eu-west-1.amazonaws.com/mondo-production-image-uploads/user_00009Vk182u7NXFlNmoBSz/7DS5UJt0jB4bl4X9wnNf-c95c1ee7-ed3a-4757-80ab-d53b7f02c4fc"}

try:
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v2.0/recognizeText?%s" % params, json.dumps(body) , headers)
    response = conn.getresponse()
    
    x = response.getheader('Operation-Location')
    #print(json.dumps(response.getheaders()))
    #params = urllib.parse.urlencode({response["Operation-Location"]})
    time.sleep(5)
    
    #print(x)
    #print(x.split("/")[-1]) 
    
    try:
        params2 = urllib.parse.urlencode({
           # Request parameters
            'operationId': x.split("/")[-1],
        })
        conn2 = http.client.HTTPSConnection("westcentralus.api.cognitive.microsoft.com")
        conn2.request("GET", "/vision/v2.0/textOperations/{operationId}?%s" % params2, "{body}", headers)  
        response2 = conn2.getresponse()
    
        #z = analysis = response.json()
        
        #x = response.getheader('Operation-Location')
        #params = urllib.parse.urlencode({response["Operation-Location"]})
        data2 = response2.read()
        #print(data2)
        
        z = json.loads(data2)
       # z = json.loads(data2)
        
        pp = pprint.PrettyPrinter(width=41, compact=True)
        #pp.pprint(z)
        #pp.pprint(z["recognitionResult"]["lines"])
        
        
        
        
        for item in z["recognitionResult"]["lines"]:
            #item = json.loads(item)
            print(item["text"])

        #print(line_infos)
        
        
        
        conn2.close()
  #  print(type("ABC")


    except Exception as e:    
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    	
    	# Extract the word bounding boxes and text.
        #line_infos = data2["lines"]
        #word_infos = []
        #print(line_infos)


        #for line in line_infos:
   	     #   for word_metadata in line:
   	      #      for word_info in word_metadata["words"]:
   	       #         word_infos.append(word_info)
        #word_infos
	
        # open the output file for writing
        #dataFile = open('scanned-chars.txt', 'w')

        # loop through each item in the list
        # and write it to the output file
        #for eachitem in word_infos:
         #   dataFile.write(str(eachitem["text"])+'\n')

        # close the output file
        #dataFile.close()
    
    conn.close()
except Exception as e:
   print("[Errno {0}] {1}".format(e.errno, e.strerror))
    
    #parsed = urlparse.urlparse(url)
    #print urlparse.parse_qs(parsed.query)['def']


   

    
    
