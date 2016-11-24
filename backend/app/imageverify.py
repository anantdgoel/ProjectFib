import http.client
import json
import urllib

#TODO Move all these secret keys to a single file. Maybe use a ConfigParser for this?
MICROSOFT_CV_SUBSCRIPTION_KEY = '92e7b0d9a88a4a6495c5b40481cbe81e'

TWITTER_API_KEY = 'WwA5L9U5PCqbnlfblKwKF0LEo'
TWITTER_API_SECRET = 'ezUnYWFGyoOzeW68Au7MWLbYvX8ashIYWMEPtOnMqmxQgzXlRu'
OAUTH_TOKEN = '136941431-Fwtibpyy072k8bqnoJyvLyrid69ZnUIYqbgPGiFr'
OAUTH_TOKEN_SECRET = 'mtkQ6H6XFElMmp6YV3fLlwx6tPBsZLxt39VWvAJ5H3EJY'

WOT_API_KEY = "e38619a0411ceaa1021f883730ffeeae3a386fa0"
MIN_TRUST_SCORE = 70

AYLIEN_APP_ID = "357c1a5a"
AYLIEN_APP_KEY = "458f8b52cec9fdbfd260a52d728c9d80"

IBM_WATSON_API_KEY = '899037d290dbf55145ab97ebccaae88d68b84210'

MICROSOFT_SEARCH_SUBSCRIPTION_KEY = '71b952e8431b4059b3eef47c50eead89'

def no_adult_content(body):
    """
    Use Microsoft's Project Oxford Computer Vision API to detect Adult/NSFW content in images.
    Returns True if content is Safe For Work (SFW), and False otherwise.
    """
    is_adult = False
    is_racy = False
    headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': MICROSOFT_CV_SUBSCRIPTION_KEY,}
    params = urllib.parse.urlencode({'visualFeatures': 'Adult', 'language': 'en',})
    #body = "{\"url\":\"http://www.gettyimages.ca/gi-resources/images/Homepage/Hero/UK/CMS_Creative_164657191_Kingfisher.jpg\"}"
    microsoft_project_oxford_endpoint = 'api.projectoxford.ai'
    try:
        conn = http.client.HTTPSConnection(microsoft_project_oxford_endpoint)
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        data = json.loads(data.decode("utf-8"))
        is_adult = data['adult']['isAdultContent']
        is_racy =  data['adult']['isRacyContent']
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return not is_adult and not is_racy

#no_adult_content("{\"url\":\"http://www.gettyimages.ca/gi-resources/images/Homepage/Hero/UK/CMS_Creative_164657191_Kingfisher.jpg\"}")

# TODO this function's variable names are pretty confusing, and there's not enough informative
#      commenting for a 80 line function. The function is likely still too long.
def twitter_present(link):
    import re
    from twython import Twython # pip install twython
    u = 0
    twitterorno = 0 # TODO Use booleans here
    thetwittertext = ""
    twitterusers = []

    twitter = Twython(TWITTER_API_KEY,
                      TWITTER_API_SECRET,
                      OAUTH_TOKEN,
                      OAUTH_TOKEN_SECRET)

    headers = {'Content-Type': 'application/json','Ocp-Apim-Subscription-Key': MICROSOFT_CV_SUBSCRIPTION_KEY,}
    params = urllib.parse.urlencode({'language': 'unk','detectOrientation ': 'true',})
    body = "{\"url\":\"" + link + "\"}"
    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/vision/v1.0/ocr?%s" % params, body, headers)
        response = conn.getresponse()
        json_data = response.read()
        data = json.loads(json_data.decode("utf-8"))

        if len(data) == 3:
            if data['orientation'] == 'NotDetected':
                u = 1
        else:
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
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    twpresentornot = 0
    if twitterorno == 0:
        u = 1
    elif twitterorno == 1:
        #print(thetwittertext)
        for p in twitterusers:
            p = p.replace("@","")
            try:
                user_timeline = twitter.get_user_timeline(screen_name=p, count=1000)
            except TwythonError as e:
                #print(e)
                pass # TODO shouldn't be ignoring exceptions.
            for tweets in user_timeline:
                formattedtweets = str(tweets['text'].encode('utf-8')).replace("b\'","").replace("\'","")
                formattedtweets = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', formattedtweets)
                if formattedtweets in thetwittertext:
                    twpresentornot = 1
                    break

    return1 = 1 if twpresentornot == 1 else  0

    return u == 1 or return1 != 0

def verified_links( url ):
    """
    Use's Web of Trust's API to detect untrustworthy web addresses.
    """
    #Check if web address
    import requests
    mywot_api_endpoint = "http://api.mywot.com/0.4/public_link_json2"
    #add_website_here = "https://www.ncbi.nlm.nih.gov/pubmed/26389314"
    querystring = {"hosts":"/"+ url + "/","callback":"process","key" : WOT_API_KEY}
    payload = ""
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'postman-token': "93ffde57-c70f-a775-d5ce-03f8e152e9da"
        }
    response = requests.request("GET", mywot_api_endpoint, data=payload, headers=headers, params=querystring)
    data = response.text.replace("process","")
    web_of_trust_score = int(data.split("[")[1].split(",")[0])
    if web_of_trust_score > MIN_TRUST_SCORE:
        return "verified"
    elif "blacklists" in data:
        return "Blacklisted"
    else:
        return "not verified" # TODO Why are we returning Strings and not booleans here?

def summarization(url):
    """
    Uses Aylien's Text Summarization API to summarize the text content of the
    page at the given URL.
    Returns the summarized text as a string.
    """
    from aylienapiclient import textapi
    client = textapi.Client(AYLIEN_APP_ID, AYLIEN_APP_KEY)

    summary = client.Summarize({'url': url, 'sentences_number': 3})
    if len(summary['sentences'])==0:
        return ""
    else:
        return " ".join(sentence for sentence in summary['sentences'] )

def url_title(link):
    """
    Uses IBM Watson AlchemyLanguage API to extract the title of the webpage at the
    address of the link passed as argument.
    Eg: link : "http://techcrunch.com/2016/01/29/ibm-watson-weather-company-sale/"
        returns ->
        title: "IBM Closes Weather Co. Purchase, Names David Kenny New Head Of Watson Platform"
    """
    from watson_developer_cloud import AlchemyLanguageV1
    alchemy_language = AlchemyLanguageV1(api_key = IBM_WATSON_API_KEY)
    alchemyres = json.dumps(alchemy_language.title(url=link),indent=2)
    data = json.loads(alchemyres)
    return data["title"] # TODO Check whether json response is empty or not

def other_links(url):
    """
    Uses Microsoft's Cognitive API to evaluate the quality of a webpage, and suggest
    better information if possible.
    """
    link_verified = verified_links(url)
    if link_verified == "not verified":

        st = url_title(url)
        import http.client, urllib.request, urllib.parse, urllib.error
        headers = {
            'Ocp-Apim-Subscription-Key': MICROSOFT_SEARCH_SUBSCRIPTION_KEY,}
        params = urllib.parse.urlencode({'q': st, 'count': '10', 'offset': '0', 'mkt': 'en-us','safesearch': 'Moderate',})
        try:
            conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
            conn.request("GET", "/bing/v5.0/search?%s" % params, "", headers)
            response = conn.getresponse()
            data = response.read()
            #print(data)
            data = json.loads(data.decode("utf-8"))

            for alt_url in data['webPages']['value']:
                if alt_url['displayUrl'] != url:
                    urlscores = verified_links(alt_url['displayUrl'])
                    if urlscores == "verified":
                        alternative_summary = "Non verified. Better Verified Info is : "+summarization(alt_url['displayUrl'])
                        return alternative_summary
            conn.close()
            return "no verified links"

        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
    else:
        return link_verified

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
                count += 1
        else:
            if ".jpg" in link or ".png" in link:
                if no_adult_content("{\"url\":\"" + link+"\"}") and twitter_present(link):
                    return "Verified"
                else:
                    return "Not Verified"
            else:
                return other_links(link)

if __name__ == "__main__":
    print(main('https://scontent-lga3-1.xx.fbcdn.net/v/t1.0-0/p480x480/15094286_1461068273945394_240413192541301870_n.jpg?oh=2213d25515dac7200efbc93ec5abe94d&oe=58C33895'))
