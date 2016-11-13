import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
from pprint import pprint
import urllib

def detectAdultContent(body):
    dp1 = ""
    dp2 = ""
    headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': '92e7b0d9a88a4a6495c5b40481cbe81e',}
    params = urllib.parse.urlencode({'visualFeatures': 'Adult', 'language': 'en',})
    #body = "{\"url\":\"http://www.gettyimages.ca/gi-resources/images/Homepage/Hero/UK/CMS_Creative_164657191_Kingfisher.jpg\"}"
    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        data = json.loads(data.decode("utf-8"))
        #print("isAdultContent")
        #print(data)
        dp1 = data['adult']['isAdultContent']
        #print("isRacyContent")
        dp2 = (data['adult']['isRacyContent'])
        
        #print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    #print(dp1)
    #print(dp2)
    if dp1 == False & dp2 == False:
        #print('True')
        return(True)
    else:
        #print('False')
        return(False)
    



#detectAdultContent("{\"url\":\"http://www.gettyimages.ca/gi-resources/images/Homepage/Hero/UK/CMS_Creative_164657191_Kingfisher.jpg\"}")
#link = 'dkakasdkjdjakdjadjfalskdjfalk'

def twitterpresentorno(link):
    import http.client, urllib.request, urllib.parse, urllib.error, base64
    import re
    u = 0
    return1 = 0
    thestring = "text1\ntext2\nhttp://url.com/bla1/blah1/\ntext3\ntext4\nhttp://url.com/bla2/blah2/\ntext5\ntext6"
    twitterorno = 0
    thetwittertext = ""
    twitterusers = []
    dk = "abc"
    #print('here')
    from twython import Twython # pip install twython
    import time # standard lib
    twitter = Twython('WwA5L9U5PCqbnlfblKwKF0LEo','ezUnYWFGyoOzeW68Au7MWLbYvX8ashIYWMEPtOnMqmxQgzXlRu','136941431-Fwtibpyy072k8bqnoJyvLyrid69ZnUIYqbgPGiFr','mtkQ6H6XFElMmp6YV3fLlwx6tPBsZLxt39VWvAJ5H3EJY')
    headers = {'Content-Type': 'application/json','Ocp-Apim-Subscription-Key': '92e7b0d9a88a4a6495c5b40481cbe81e',}
    params = urllib.parse.urlencode({'language': 'unk','detectOrientation ': 'true',})
    body = "{\"url\":\"" + link + "\"}"
    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/vision/v1.0/ocr?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        data = json.loads(data.decode("utf-8"))
        
        #print(data)
        #print(len(data))
        if len(data) == 3:
            if data['orientation'] == 'NotDetected':
                return1 = -1
                u = 1
                #print("yes")
        else:
            #print("yo")
            for p in data['regions'][0]['lines']:
                for x in p['words']:
                    thetwittertext = thetwittertext + " " + x['text'] 
                    if '@' in x['text']:
                        twitterusers.append(x['text'])
                        twitterorno = 1    
                    elif x['text'].lower() in ["tweet","retweets"]:
                        twitterorno = 1
                    else:
                        pass
        conn.close()
    except Exception as e:
        #print("[Errno {0}] {1}".format(e.errno, e.strerror))
        return1 = -1
    twpresentornot = 0
    if twitterorno == 0:
        u = 1
    if twitterorno == 1:
        #print(thetwittertext)
        for p in twitterusers:
            p = p.replace("@","")
            try:
                user_timeline = twitter.get_user_timeline(screen_name=p, count=1000)
            except TwythonError as e:
                #print(e)
                pass
            for tweets in user_timeline:
                formattedtweets = str(tweets['text'].encode('utf-8')).replace("b\'","").replace("\'","")
                formattedtweets = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', formattedtweets)
                if formattedtweets in thetwittertext:
                    twpresentornot = 1
                    break
    else:
        return1 = 1
    
    if twpresentornot == 1:
        return1 = 1
    else:
        return1 = 0
    #print(return1)
    if u == 1:
        #print('True')
        return(True)
    elif return1 == 0:
        #print('False')
        return(False)
    else:
        #print('False')
        return(True)

def verifiedlinks(add_website_here):
    import requests
    url = "http://api.mywot.com/0.4/public_link_json2"
    #add_website_here = "https://www.ncbi.nlm.nih.gov/pubmed/26389314"
    querystring = {"hosts":"/"+add_website_here+"/","callback":"process","key":"e38619a0411ceaa1021f883730ffeeae3a386fa0"}
    payload = ""
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'postman-token': "93ffde57-c70f-a775-d5ce-03f8e152e9da"
        }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    data = response.text.replace("process","")
    #print(data)
    wot = int(data.split("[")[1].split(",")[0])
    if wot > 70:
        return("verified")
    elif "blacklists" in data:
        return("Blacklisted")
    else:
        return("not verified")

def summarization(url):
    from aylienapiclient import textapi
    summarizedtext = ""
    client = textapi.Client("357c1a5a", "458f8b52cec9fdbfd260a52d728c9d80")
    
    summary = client.Summarize({'url': url, 'sentences_number': 3})
    for sentence in summary['sentences']:
        summarizedtext = summarizedtext + " " + sentence;
    return(summarizedtext)

def urltitle(link):
    import json
    from watson_developer_cloud import AlchemyLanguageV1
    alchemy_language = AlchemyLanguageV1(api_key='899037d290dbf55145ab97ebccaae88d68b84210')
    alchemyres = json.dumps(alchemy_language.title(url=link),indent=2)
    data = json.loads(alchemyres)
    return(data["title"])

def otherlinks(urllink):
    #from bs4 import BeautifulSoup
    from urllib.request import urlopen
    vorno=0
    #urllink = "https://www.cancer.gov/about-cancer/treatment/cam/patient/cannabis-pdq"
    
    if(verifiedlinks(urllink) == "not verified"):

        st = urltitle(urllink)
        import http.client, urllib.request, urllib.parse, urllib.error, base64
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': '71b952e8431b4059b3eef47c50eead89',}
        params = urllib.parse.urlencode({'q': st, 'count': '10', 'offset': '0', 'mkt': 'en-us','safesearch': 'Moderate',})
        try:
            conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
            conn.request("GET", "/bing/v5.0/search?%s" % params, "", headers)
            response = conn.getresponse()
            data = response.read()
            #print(data)
            data = json.loads(data.decode("utf-8"))
            for h in data['webPages']['value']:
                if h['displayUrl'] == urllink:
                    pass
                else:
                    urlscores = verifiedlinks(h['displayUrl'])
                    if urlscores == "verified":
                        v = 1
                        kk = "Non verified. Better Verified Info is : " + " "+summarization(h['displayUrl'])
                        return(kk)
                        break;           
            if v == 0:
                return("no verified links")
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
    else:
        return verifiedlinks(urllink)    
   
def main(link):
    #link = "http://i.imgur.com/walokrp.png"
    tokens = [urllib.parse.urlparse(url) for url in ("",link)]
    count = 0
    min_attributes = ('scheme', 'netloc')  # add attrs to your liking
    for token in tokens:
        if not all([getattr(token, attr) for attr in min_attributes]):
            if count > 0:
                print("no link")
            else:
                count = count + 1
        else:
            if ".jpg" in link:
                p = detectAdultContent("{\"url\":\"" + link+"\"}")
                #print(p)
                p = p & twitterpresentorno(link)
                #print("p1=")
                #print(type(p))
                if p:
                    return("Verified")
                else:
                    return("Not Verified")
                
            elif ".png" in link:
                p = detectAdultContent("{\"url\":\"" + link+"\"}")
                #print(p)
                p = p & twitterpresentorno(link)
                #print("p2=")
                #print(type(p))
                if p:
                    return("Verified")
                else:
                    return("Not Verified")
            else:
                return(otherlinks(link))
            
if __name__ == "__main__":
    print(main('https://scontent-lga3-1.xx.fbcdn.net/v/t1.0-0/p480x480/15094286_1461068273945394_240413192541301870_n.jpg?oh=2213d25515dac7200efbc93ec5abe94d&oe=58C33895'))
    