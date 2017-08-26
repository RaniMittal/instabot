import requests
import urllib
token="1796098632.8aee24b.cc35bab9d9c24ea5a19895f7c75108a0"
base_url="https://api.instagram.com/v1/"


def download_media(media_id):
    media_id=media_id
    if media_id == None:
        print "requested media does not exist"
    else:
        url = "%smedia/%s?access_token=%s" % (base_url, media_id, token)
        r1 = requests.get(url)
        r1 = r1.json()
        if r1['meta']['code'] == 200:
            print "successfully downloaded post and it's id is %s" % (media_id)
        else:
            print "something went wrong"
        media_type = r1['data']['type']
        if media_type == "image":
            url1 = r1['data']['images']['low_resolution']['url']
            urllib.urlretrieve(url1, 'image.jpg')
        elif media_type == "carousel":  # carousel means collection of images like slider on facebook
            url1 = r1['data']['carousel_media'][0]['images']['low_resolution']['url']
            urllib.urlretrieve(url1, 'img1.jpg')
        elif media_type == "video":
            url1 = r1['data']['videos']['low_resolution']['url']
            urllib.urlretrieve(url1, 'video.mp4')

def getting_self_id():
        url="users/self/?access_token="
        endpoint=base_url + url + token
        r=requests.get(endpoint) # to get the response
        r=r.json()  # to convert the response in json
        # print r
        print "your id is"
        print r['data']['id'] # extracting the data we need from json

def getting_user_id():
        user_name=raw_input("enter the user name")
        # url1="users/search?q="
        # url2="&access_token="
        # endpoint=base_url+url1+user_name+url2+token
        # r=requests.get(endpoint)
        url= "%susers/search?q=%s&access_token=%s" % (base_url , user_name , token)
        r=requests.get(url)
        r=r.json()
        if r['meta']['code']==200:
            if len(r['data'])!=0: # r['data'] returns an array having the data of all users matching the name entered if it is an empty array this means there is no user of the name entered
                print user_name + "\'s id is"
                user_id= r['data'][0]['id'] # r['data'][0] gives the data of first user in the array r['data']
                print user_id
                return user_id
            else:
                print "there is no person on instagram with this username"
        else:
            print "something went wrong.Try again later"

def getting_user_media_id():
    user_id=getting_user_id()
    # url3="users/"
    # url4="/media/recent/?access_token="
    # endpoint2=base_url+url3 + user_id + url4 + token
    # r=requests.get(endpoint2)
    url="%susers/%s/media/recent/?access_token=%s" % (base_url, user_id, token)
    r1=requests.get(url)
    r1=r1.json()
    # return r1      return r1 if u r using another way to download media
    # print r1
    # print r1['data'][0]['id']
    if r1['meta']['code']==200:
        media_id=r1['data'][0]['id']
        return media_id
    else:
        print "something went wrong or may be you cannot view this resource"

# another way to download media
# def downloading_user_media():
#     r1=getting_user_media_id()
#     media_type=r1['data'][0]['type']
#     if media_type=="image":
#         url1=r1['data'][0]['images']['low_resolution']['url']
#         urllib.urlretrieve(url1,'image.jpg')
#     elif media_type=="carousel":
#         url1=r1['data'][0]['carousel_media'][0]['images']['low_resolution']['url']
#         urllib.urlretrieve(url1,'img1.jpg')
#     elif media_type=="video":
#         url1=r1['data'][0]['videos']['low_resolution']['url']
#     urllib.urlretrieve(url1,'video.jpg')

def downloading_user_media():
    media_id=getting_user_media_id()
    download_media(media_id)

def liking_user_post():
    media_id = getting_user_media_id()
    url="%smedia/%s/likes" % (base_url, media_id)
    data={"access_token":token}
    r=requests.post(url,data)
    r=r.json()
    if r['meta']['code']==200:
        print "post is successfully liked"

def comment_user_post():
    media_id = getting_user_media_id()
    comment=raw_input("enter your comment:")
    data={"access_token": token,"text": comment}
    url="%smedia/%s/comments" % (base_url, media_id)
    r=requests.post(url,data)
    r=r.json()
    # print r
    if r['meta']['code']==200:
        print "successfull"

def download_your_recent_post():
    url=base_url + "users/self/media/recent/?access_token=%s" % (token)
    r=requests.get(url)
    r = r.json()
    if len(r['data'])!=0:
        media_id = r['data'][0]['id']
        if r['meta']['code']==200:
            print "post is successfully downloaded and the post id is %s" % (media_id)
        media_type = r['data'][0]['type']
        if media_type == "image":
            url1 = r['data'][0]['images']['low_resolution']['url']
            urllib.urlretrieve(url1, 'image.jpg')
        elif media_type == "carousel":  # carousel means collection of images like slider on facebook
            url1 = r['data'][0]['carousel_media'][0]['images']['low_resolution']['url']
            urllib.urlretrieve(url1, 'img1.jpg')
        elif media_type == "video":
            url1 = r['data'][0]['videos']['low_resolution']['url']
            urllib.urlretrieve(url1, 'video.mp4')
    else :
        print "you don't have any post on instagram"

def download_post_in_creative_way():
    user_id = getting_user_id()
    url2 = "%susers/%s/media/recent/?access_token=%s" % (base_url, user_id, token)
    r = requests.get(url2)
    r = r.json()
    ch = 1
    media_id=r['data'][0]['id']
    while ch!=7:
        ch = int(raw_input("which type of user\'s media you want to download. The one with\n 1.minimum no of likes\n 2.maximum no of likes\n 3.having a particular text\n 4.most recent\n 5.minimum comments\n 6.maximum comments\n 7.to come out of this loop"))
        if ch==1:
            i=1
            while i<len(r['data']):
                if r['data'][i]['likes']['count'] < r['data'][i-1]['likes']['count']:
                    media_id=r['data'][i]['id']
                i=i+1

        elif ch==2:
            i = 1
            while i < len(r['data']):
                if r['data'][i]['likes']['count'] > r['data'][i-1]['likes']['count']:
                    media_id=r['data'][i]['id']
                    i = i+1

        elif ch==3:
            text=raw_input("enter the text that the media's caption has which you want to download:-")
            for item in r['data']:
                # print item['id']
                if item['caption']!= None:
                    if text.lower() in item['caption']['text'].lower():
                        media_id = item['id']
                        break;
                    media_id = None

        elif ch==4:
            media_id = r['data'][0]['id']

        elif ch==5:
            i = 1
            while i < len(r['data']):
                if r['data'][i]['comments']['count'] < r['data'][i - 1]['comments']['count']:
                    media_id = r['data'][i]['id']
                    i = i + 1

        elif ch==6:
            i = 1
            while i < len(r['data']):
                if r['data'][i]['comments']['count'] > r['data'][i - 1]['comments']['count']:
                    media_id = r['data'][i]['id']
                    i = i + 1

        elif ch==7:
            break;

        else:
            print "you can only choose from 1-7"

        download_media(media_id)


def get_recent_media_liked_by_user():
    url=base_url + "users/self/media/liked?access_token=" + token
    r=requests.get(url)
    r=r.json()
    print "media id of recent media liked by the user" + r['data'][0]['id']

def get_commentlist_on_user_post():
    media_id = getting_user_media_id()
    url="%smedia/%s/comments?access_token=%s" % (base_url,media_id,token)
    r=requests.get(url)
    r=r.json()
    i=0
    while i<len(r['data']):
        print "comment is \"" + r['data'][i]['text'] + "\" from " + r['data'][i]['from']['username']
        i=i+1


choice=1
while choice!=10:
    choice = int(raw_input(
        "what u want to do? 1.get ur own id\n 2.get another user\'s id\n 3.download user\'s recent media\n 4.like user\'s post\n 5.comment on user\'s post\n 6.download your recent media\n 7.get the media id of recent media liked by the user(owner of access token)\n 8.get_commentlist_on_user_post\n 9.download_post_in_creative_way\n 10. to exit"))
    if choice==1:
        getting_self_id()
    elif choice==2:
        getting_user_id()
    elif choice==3:
        downloading_user_media()
    elif choice==4:
        liking_user_post()
    elif choice==5:
        comment_user_post()
    elif choice==6:
        download_your_recent_post()
    elif choice==7:
        get_recent_media_liked_by_user()
    elif choice==8:
        get_commentlist_on_user_post()
    elif choice==9:
        download_post_in_creative_way()
    elif choice==10:
         exit();
    else :
        print "you can only choose 1-10"