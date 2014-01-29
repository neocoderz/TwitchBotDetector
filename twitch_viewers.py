import requests
import json
import sys # for printing to stderr

MAX = 100
limit = str(MAX)
offset = str(0)

def print_game_viewers(game):
    num_channels = -1
    for i in range(0, len(gamedata['top'])):
#       if the game isn't found, increment offset and search again
        if gamedata['top'][i]['game']['name'] == game:
            num_channels = gamedata['top'][i]['channels']

    if num_channels == -1:
        print '... couldn\'t find ' + game + ':(\ndaed game'

    offset = str(0)
    for i in range(0, 1 + num_channels / MAX):
        p = requests.get('https://api.twitch.tv/kraken/streams?limit=' + limit + 
                         '&offset=' + offset + 
                         '&game=' + game) 
        p.text
        userdata = p.json()
        offset = str(int(offset) + MAX)
        for j in range(0, len(userdata['streams'])): 
            print userdata['streams'][j]['channel']['display_name'] + ": " + str(userdata['streams'][j]['viewers'])

def removeNonAscii(s): return "".join([x if ord(x) < 128 else '?' for x in s])

r = requests.get('https://api.twitch.tv/kraken/games/top' +
                 '?limit=' + limit)
r.text
flag = 1
while flag: #jank bugfix - sometimes can't read json
    try:
        gamedata = r.json()
        flag = 0
    except:
        pass


def user_viewers(user):
    errlog = open('errlog.txt', 'w')
    req = 0
    while (not req):
        try: 
            req = requests.get("https://api.twitch.tv/kraken/streams/" + user)
        except requests.exceptions.ConnectionError:
            errlog.write("bad error. retry?\n")
            pass
    while (req.status_code != 200):
        print.write(req.status_code + " viewerlist unavailable")
        errlog.write(req.status_code + " viewerlist unavailable")
        req = requests.get("https://api.twitch.tv/kraken/streams/" + user)
    try:
        userdata = req.json()
    except ValueError:
        errlog.write("nope starting over - check out user_viewers recursion\n")
        return user_viewers(user) #nope start over
    if (len(userdata.keys()) == 2):
        viewers = 0
        if (userdata['stream']): # if the streamer is offline, userdata returns null
            viewers = userdata['stream']['viewers']
        if (viewers == 0):
            print user + " appears to be offline!"
        return viewers
    else:
        print str(userdata['status']) + " " + userdata['message'] + " " + userdata['error']
        print user + " is not live right now, or the API is down."
        return 0

def print_all_games():

    for i in range(0,int(limit)):
        game = removeNonAscii(gamedata['top'][i]['game']['name'])
        print 'Users for ' + game + ':'
        print_game_viewers(game)
        print
        print
        print

