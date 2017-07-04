
# -*- coding: utf-8 -*-
import requests
import httplib, urllib, base64, json
import os,sys
import re


def imgtest2(picurl):


    # Replace the subscription_key string value with your valid subscription key.
    subscription_key = '1aeaf4a5de9c4d828c0ff823b5899074'

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

    # The URL of a JPEG image to analyze.
    print(picurl)
    body = "{'url':'"+picurl+"'}"




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
        
        ######### Get Happiness Index & identify mood ################

        emotion = ""
        for item in parsed:
            for key in item:
                for key1 in item[key]:
                    if key1 == "emotion":
                        for key2 in item[key][key1]:
                            if key2 == "happiness":
                                emotion = item[key][key1][key2]
                                #print(emotion)
        
        if emotion > 0.8:
            mood = "很高兴"
        elif emotion > 0.5:
            mood = "有点高兴"
        else:
            mood = "一般"

        return mood


        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
