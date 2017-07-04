# -*- coding: utf-8 -*-
import requests
import httplib, urllib, base64, json
import os,sys
import re


def imgtest1(body):

    # Replace the subscription_key string value with your valid subscription key.
    subscription_key = '1aeaf4a5de9c4d828c0ff823b5899074'

    params = urllib.urlencode({
        'returnFaceId': 'false',
        'returnFaceLandmarks': 'true',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    })

        #specify image from file

        #For a local image, Content-Type should be application/octet-stream or multipart/form-data AND JSON SHOULD BE EMPTY

    headers = {

        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }



    try: 
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')

        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)

        response = conn.getresponse()

        data = response.read()
    
        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        print ("Response:")
        print (json.dumps(parsed, sort_keys=True, indent=2))
        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

'''

def imgtest1(picurl):
    s = requests.session()

    # Replace the subscription_key string value with your valid subscription key.
    subscription_key = '1aeaf4a5de9c4d828c0ff823b5899074'

    # Replace or verify the region.
    #
    # You must use the same region in your REST API call as you used to obtain your subscription keys.
    # For example, if you obtained your subscription keys from the westus region, replace 
    # "westcentralus" in the URI below with "westus".
    #
    # NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
    # a free trial subscription key, you should not need to change this region.
    uri_base = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'

    # Request headers.
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    # Request parameters.
    params = urllib.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    })

    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        print ("Response:")
        print (json.dumps(parsed, sort_keys=True, indent=2))
        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
'''