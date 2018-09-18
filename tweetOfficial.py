Punctuation =  "!$%&\'(’)*+,-./:;<=>?[\\]^_`{|}~.“”~"
DIGIT = ("0","1","2","3","4","5","6","7","8","9")
def extract_mentions(tweet):
    '''(str) -> list of str
    
    Return a list of all mentions in the tweet.

    >>> extract_mentions("Love the new Mackbook, #MakeAmericaGreatAgain #Life
    #HappyHolic")
    []
    
    >>> extract_mentions("@realDonaldTrump's hair is funny")
    ['realDonaldTrump']
    
    >>> extract_mentions("")
    []
    
    >>> extract_mentions("@realDonaldTrump: Mexico will pay for the wall,
    @realDonaldTrump are u 4 real?")
    ['realDonaldTrump', 'realDonaldTrump']
    
    >>> extract_mentions("Check @luisdortiz new bracelets line, amazing and 
    beautiful #HappyHolic")
    ['luisdortiz']
    
    >>> extract_mentions("I told both @BillGates and @elonmusk that future is
    green energy")
    ['BillGates', 'elonmusk']
    
    >>> extract_mentions("if you need lawyer go for @HarveySpector")
    ['HarveySpector']
    '''
    words = tweet.split()
    mentions = []
    for w in words:
        if w.startswith("@"):
            if _find_punctuation_(w) == -1:
                mentions.append(w[1:])
            else:
                mentions.append(w[1:_find_punctuation_(w)])
    return mentions          
#-------------------------------------------------------------------------------
def extract_hashtags(tweet):
    '''(str) -> list of str

    Return a list of all hashtags in the tweet. Repeat hashtags will be included
    only once.
    
    >>> extract_hashtags("Survey shows Tesla owners in Germany understand the
    meaning and function of Autopilot")
    []
    
    >>> extract_hashtags("")
    []
    
    >>> extract_hashtags("#Mars is hard, but it’s worth the risks to extend
    humanity’s frontier beyond Earth. Learn about our neighbor planet:
    http://go.nasa.gov/2fU2fmu")
    ['Mars']
    
    >>> extract_hashtags("Battle for #Mosul Day 31: #Iraq’s #PMF hands over 16
    #Mosul villages to #Army")
    ['Mosul', 'Iraq’s', 'PMF', 'Army']
    
    >>> extract_hashtags("Video: #BlackLivesMatter, Protesters Who Blocked
    Highway Get Jail Time")
    ['BlackLivesMatter']
    '''
    words = tweet.split()
    tags = []
    for w in words:
        if w.startswith("#"):
            if _find_punctuation_(w) == -1:
                if not(w[1:] in tags):
                    tags.append(w[1:])
            else:
                if not(w[1:_find_punctuation_(w)] in tags):
                    tags.append(w[1:_find_punctuation_(w)])
    return tags
#-------------------------------------------------------------------------------
def count_words(tweet, word_count):
    '''(str, dict of {str: int}) -> None

    Update the count of words in the dictionary and adding the new words and
    their counts to it.
    
    >>> word = {}
    >>> count_words("@WalkingDead_AMC Countdown: Ranking the Show's Top 20
    Villains of All Time #TheWalkingDead", word)
    >>> word
    {'time': 1, 'shows': 1, 'ranking': 1, 'of': 1, 'countdown': 1, 'all': 1,
    'villains': 1, 'the': 1, 'top': 1, '20': 1}
    
    >>> word = {"cnn":1, "app":2, "nyc":1}
    >>> count_words("CNN BOUGHT BEME ( the app created by Casey Neistat ) #beme
    @bemeapp @CNN #youtube", word)
    >>> word
    {'by': 1, 'created': 1, 'casey': 1, 'bought': 1, 'app': 3, 'nyc': 1, 'cnn':
    2, 'neistat': 1, 'the': 1, 'beme': 1}

    >>> word = {}
    >>> count_words("", word)
    >>> word
    {}

    >>> word = {}
    >>> count_words("@realDonaldTrump https://twitter.com/realdonaldtrump
    #MakeAmericaGreatAgain", word)
    >>> word
    {}

    >>> word = {"utm":1, "csc":1, "assignment":3, "hate":2, "my":1, "life":1}
    >>> count_words("", word)
    >>> word
    {'assignment': 3, 'csc': 1, 'life': 1, 'hate': 2, 'utm': 1, 'my': 1}
    '''
    tweet_cleaned = ""
    for char in tweet:
        if not(char in Punctuation):
            tweet_cleaned = tweet_cleaned + char.lower()
    words = tweet_cleaned.split()
    for w in words:
        if not(w.startswith("#") or w.startswith("@") or w.startswith("http")) :
            word_count[w] = word_count.get(w, 0) + 1           
#-------------------------------------------------------------------------------  
def common_words(word_count, amount): 
    '''(dict of {str: int}, int) -> None

    Update the dictionary so it only contain the N most frequently words.

    >>> dicti = {"mixed":1, "with":1, "lil":2, "bit":3, "persian":99}
    >>> common_words(dicti, 3)
    >>> dicti
    {'persian': 99, 'lil': 2, 'bit': 3}

    >>> dicti = {"criminalistic":1, "forensic":1, "science":1}
    >>> common_words(dicti, 2)
    >>> dicti
    {}

    >>> dicti = {"death":1, "metal":2}
    >>> common_words(dicti, 2)
    >>> dicti
    {'metal': 2, 'death': 1}

    >>> dicti = {}
    >>> common_words(dicti, 2)
    >>> dicti
    {}
    
    >>> dicti = {"hp":1, "spectre":8}
    >>> common_words(dicti, 4)
    >>> dicti
    {'spectre': 8, 'hp': 1}

    >>> dicti = {"determining":1, "cause":1, "of":1, "death":2, "forensic":2,
    "science":3}
    >>> common_words(dicti, 4)
    >>> dicti
    {'death': 2, 'forensic': 2, 'science': 3}
    '''
    if not(amount >= len(word_count)):
        clean_value = []
        count = _value_dict_sorter_(word_count,amount + 1)
        if count[-1] == count[-2]:
            extra = count[-1]
            while extra in count: count.remove(extra)
            value = list(word_count.values())
            for i in count: value.remove(i)
            for j in value:
                if not(j in clean_value): clean_value.append(j)
            _key_deleter_(word_count,clean_value)
        else:
            count = count[:-1]
            value = list(word_count.values())
            for i in count: value.remove(i)
            for j in value:
                if not(j in clean_value): clean_value.append(j)
            _key_deleter_(word_count,clean_value)     
#-------------------------------------------------------------------------------
def read_tweets(file_name):
    '''(filename) -> dict of {str: list of tweet tuples}

    Return a dictionary of candidates name as key and list of each tweet
    information as value.
    
     >>> read_tweets("tweet_data.txt")
    {'Mahan Mohamadi': [('Mahan Mohamadi', 'It is not fair that we are in #peace
    and there is war in #Iraq and #syria\n', '1478038431', 'Twitter for Android'
    , '228', '6969')], 'Bear Grylls': [('Bear Grylls', 'Just finished
    #AbsoluteWild journey with the very unique @YaoMing great man who did so
    well!\n', '1396843618', 'Twitter for Iphone', '23', '132')], 'John Kerry': [
    ('John Kerry', 'As a former small biz owner & @SmallBizCmte leader I know the
    value of local patronage. #ShopSmall on #SmallBizSat! http://go.usa.gov/x89Sp
    \n', '1304969685', 'Twitter for Iphone', '337', '500'), ('John Kerry',
    'Productive discussion with UAE Crown Prince bin Zayed today on #Libya,
    #Yemen. US and UAE working together on major regional challenges #peace. \n',
    '1412320469', 'Twitter for Iphone', '266', '625')]}

    >>> read_tweets("tweet_data_longer.txt")
    {'Barack Obama': [('Barack Obama', 'In the weekly address, President Obama
    discusses what #Obamacare has done to improve health care.
    http://ofa.bo/2ebbyAo \n', '1402138456', 'Twitter for Android', '2211',
    '12124'), ('Barack Obama', 'Lions and Tiggers and bears! Oh my!
    #HappyHalloween\n', '1394658124', 'Twitter for Android', '5415', '1687'), (
    'Barack Obama', 'The need for a ninth justice is undeniably clear.
    #DoYourJob\n', '1375349651', 'Twitter for Android', '2314', '5036')],'Jordan
    Belfort': [('Jordan Belfort', 'Leo & I spent months and months, working
    tirelessly, to ensure he understood my #mannerisms, language and tonality.
    Devil is in the details #DoYourJob\n', '1478961576', 'Twitter for Iphone',
    '325', '1000'), ('Jordan Belfort', 'View your life with wider vision. The
    contrast between the past and present is more easily defined. #NewBlogPost
    #JB\n', '1387961349', 'Unknown Location', '40', '169')], 'Casey Neistat': [(
    'Casey Neistat', 'are there speaks designed specifically to work with Google
    Home?  can anyone recommend? looking at you @MKBHD & @madebygoogle\n',
    '1496897534', 'Twitter for Iphone', '73', '1032'), ('Casey Neistat', 'umm
    @jimmisimpson & @evanrachelwood #dubsmash clips from the #WestWorld set are
    arguably as good as the actual series\n', '1364752986', 'Twitter for Iphone'
    , '158', '1184')], 'Fredrik Eklund': [('Fredrik Eklund', "Here's to over
    $35M in new deals today. #RecordYear #RainingMeatballs #ILOVENY #Grateful
    https://www.instagram.com/p/BMEe4iUDEm6/ \n", '1476593482', 'TweetDeck', '2'
    , '36')]}
    '''
    result = {}; list_tuple = []; multi_line = "";
    text = open(file_name).read().splitlines();
    if len(text) == 0: return result
    else:
        name = text[0][:-1]
        result[name] = []
        for line in range(1,len(text) + 1):
            if line == len(text) - 1:
                return _dict_list_appender_(list_tuple, multi_line, name,result)
            elif text[line + 1].startswith(DIGIT) and text[line].endswith(":")\
            and ("<<<EOT" in text[line - 1]):
                name = text[line][:-1]
                result[name] = []
            elif text[line].startswith(DIGIT) and len(text[line].split(",")) ==\
            6:
                list_tuple = _list_modifier_(list_tuple, text[line], name)
            elif ("<<<EOT" in text[line]) and text[line - 1] != "":
                _dict_list_appender_(list_tuple, multi_line, name, result)
                multi_line = ""
            else: multi_line = multi_line + text[line] + "\n"
#-------------------------------------------------------------------------------
def most_popular(tweet_info, dateStart, dateFinish):
    '''(dict of {str: list of tweet tuples}, int, int) -> list of str

    Return a list of canidades names that posted a tweet between the given time
    and sort them by their popularity.

    >>> tweet_info = read_tweets("tweet_data.txt")
    >>> most_popular(tweet_info, 1342147001, 1478038433)
    ['Mahan Mohamadi', 'John Kerry', 'Bear Grylls']

    >>> tweet_info = read_tweets("tweet_data_longer.txt")
    >>> most_popular(tweet_info, 1390000000, 1477000000)
    ['Barack Obama', 'Fredrik Eklund']

    >>> tweet_info = read_tweets("tweet_data_longer.txt")
    >>> most_popular(tweet_info,1410000000,1450000000)
    []
    '''
    result = {}; values = []; popularity = 0
    for key in tweet_info:
        for log in tweet_info[key]:
            if int(log[2]) >= dateStart and int(log[2]) <= dateFinish:
                popularity = int(log[4]) + int(log[5])
                if not(result.__contains__(log[0])):
                    result[log[0]] = popularity
                elif popularity > result[log[0]]:
                    result[log[0]] = popularity
    values = _value_dict_sorter_(result, -1)
    for i in range(len(values)):
        values[i] = _dict_invertor_(result)[values[i]]
    return values
#-------------------------------------------------------------------------------
def detect_author(tweet_info, tweet):
    '''(dict of {str: list of tweet tuples}, str) -> str

    Return the name of most likely writer of the tweet based on its hashtags.

    >>> tweet_info = read_tweets("tweet_data.txt")
    >>> detect_author(tweet_info, "New amazing finding on #Lennon' s wall in
    #Prague - John with president #Havel. #peace and have a great #weekend
    #visitCZ")
    'Unknown'

    >>> tweet_info = read_tweets("tweet_data_longer.txt")
    >>> detect_author(tweet_info, "You need to lear their #mannerisms and
    language to be able to perfotm well. #DoYourJob #DontBeLazy")
    'Jordan Belfort'

    >>> tweet_info = read_tweets("tweet_data.txt")
    >>> detect_author(tweet_info, "“The truth is not always beautiful, nor
    beautiful words the truth.” ~Lao Tzu")
    'Unknown'
    '''
    tags = {}
    tweet_tag = extract_hashtags(tweet)
    tags = _unique_tags_(_candidate_hashtag_extract_(tweet_info), tweet_tag)
    if len(tags) == 0:
        return "Unknown"
    elif len(tags) == 1:
        return list(tags.keys())[0]
    else:
        return "Unknown"
#-------------------------------------------------------------------------------
def _unique_tags_(cadidate_tags, tweet_tags):
    '''(dict of {str: list of str}, list of str) -> dict of {str: list of str}

    Return a dictionary containing the candidate names as key and the unique
    hashtags used by them as value. Return empty dictionary if it couldnt find
    any.

    >>> _unique_tags_({"Soroush Motesharei": ["metal", "slipknot", "saynotowar"
    , "iran", "tehran"], "Jennifer Lawrence": ["love", "soroush", "oscar",
    "election"], "Mike Ross": ["law","ny"]},["iraq", "middleEast", "Oil"])
    {}

    >>> _unique_tags_({"microsoft":["netFramework", "C", "windows", "office"],
    "google":["android", "office"], "Dell":["laptop", "xps"]}, ["programming",
    "office", "netFramework"])
    {'microsoft': ['netFramework']}

    >>> _unique_tags_({"Marilyn Manson":["evidence", "absinthe", "art", "music"]
    , "mozart":["confutatis", "money", "king", "music"], "insomnium":["tour",
    "wintersgate", "art"]},["art", "music", "money", "wintersgate"])
    {'mozart': ['money'], 'insomnium': ['wintersgate']}    
    '''
    empty_candidates = []
    for key in cadidate_tags:
        common_tags = []
        for i in tweet_tags:
            if i in cadidate_tags[key]: common_tags.append(i)
        cadidate_tags[key] =  common_tags
    for j in tweet_tags:
        count = 0
        for tag in cadidate_tags:
            if j in cadidate_tags[tag]:
                count += 1
        if count > 1:
            for delete in cadidate_tags:
                if j in cadidate_tags[delete]:
                    cadidate_tags[delete].remove(j)
    for empty in cadidate_tags:
        if len(cadidate_tags[empty]) == 0: empty_candidates.append(empty)
    for name in empty_candidates: del cadidate_tags[name]
    return cadidate_tags
#-------------------------------------------------------------------------------
def _candidate_hashtag_extract_(tweet_info):
    '''(dict of {str: list of tweet tuples}) -> dict of {str: list of str}

    Return a dictionary containing candidates name as key and a list of hashtags
    used by them as value.
    
    >>> info = read_tweets("tweet_data_longer.txt")
    >>> _candidate_hashtag_extract_(info)
    {'Jordan Belfort': ['mannerisms', 'DoYourJob', 'NewBlogPost', 'JB'],
    'Casey Neistat': ['dubsmash', 'WestWorld'], 'Barack Obama': ['Obamacare',
    'HappyHalloween', 'DoYourJob'], 'Fredrik Eklund': ['RecordYear',
    'RainingMeatballs', 'ILOVENY', 'Grateful']}

    >>> info = read_tweets("tweet_data.txt")
    >>> _candidate_hashtag_extract_(info)
    {'John Kerry': ['ShopSmall', 'SmallBizSat', 'Libya', 'Yemen', 'peace'],
    'Mahan Mohamadi': ['peace', 'Iraq', 'syria'], 'Bear Grylls': ['AbsoluteWild'
    ]}
    '''
    name_tags = {}
    for key in tweet_info:
        for log in tweet_info[key]:
            if not(name_tags.__contains__(log[0])): name_tags[log[0]] = []
            for i in extract_hashtags(log[1]):
                name_tags[log[0]].append(i)
    return name_tags
#-------------------------------------------------------------------------------
def _key_deleter_(dicti, value):
    '''(dict of {str: int}, list of int) -> None

    Modifies the dictionary by deleting the keys coresponding to the values
    provided.

    >>> dicti = {"wolfgang":1, "amadeus":2, "mozart":9}
    >>> _key_deleter_(dicti, [1,2])
    >>> dicti
    {'mozart': 9}

    >>> dicti = {"New":1, "blood":4, "joins":1, "this":1, "earth":3, "quickly":2
    , "subdued":2}
    >>> _key_deleter_(dicti, [1])
    >>> dicti
    {'earth': 3, 'subdued': 2, 'blood': 4, 'quickly': 2}

    >>> dicti = {"SyntaxError":0, "invalid":2, "syntax":1}
    >>> _key_deleter_(dicti, [])
    >>> dicti
    {'SyntaxError': 0, 'syntax': 1, 'invalid': 2}
    '''
    list_tuple = list(dicti.items())
    for i in value:
        for j in list_tuple:
                if j[1] == i : del dicti[j[0]]
#-------------------------------------------------------------------------------
def _value_dict_sorter_(dicti, index):
    '''(dict of {str: int}, int) -> list of int

    Return a list of values in the dictionary in aascending order up to the
    index point provided.
    
    >>> dicti = {"life":1, "death":1, "uni":3, "scotch":9, "cigar":3}
    >>> _value_dict_sorter_(dicti, 3)
    [9, 3, 3]

    >>> dicti = {"one":2, "life":1, "chance":5, "all":1, "ephemeral":9}
    >>> _value_dict_sorter_(dicti, -1)
    [9, 5, 2, 1, 1]
    '''
    value = list(dicti.values())
    value.sort()
    value.reverse()
    if index != -1:
        value = value[:index]
    return value
#-------------------------------------------------------------------------------
def _dict_invertor_(dicti):
    '''(dict of {str: int}) -> dict of {int: str}

    Return a new dictionary containing keys and values from parameter as values
    and keys.
    Precondition: Keys in the dictionary must be unique.
    
    >>> dicti = {"key1":"value1", "key2":"value2"}
    >>> _dict_invertor_(dicti)
    {'value1': 'key1', 'value2': 'key2'}
    '''
    inv_dict = {}
    for key, value in dicti.items():
        inv_dict[value] = key
    return inv_dict
#-------------------------------------------------------------------------------
def _find_punctuation_(word):
    '''(str) -> int

    Return the index of first punctuation in the word. Return -1 if nothing
    found.
    
    >>> _find_punctuation_("")
    -1
    
    >>> _find_punctuation_("Reza")
    -1

    >>> _find_punctuation_("Iraq's")
    4
    
    >>> _find_punctuation_("Obama's?")
    5
    '''
    for char in range(len(word)):
        if word[char] in Punctuation: return char
    return -1
#-------------------------------------------------------------------------------
def _dict_list_appender_(lst, value, key, dicti):
    '''(list, str, str, dict of {str: list of tweet tuples}) -> list

    Update and return the dictionary by appending values to certain key.
    
    >>> lst = ["Reza Jam", "Tehran", "1478038431", "Twitter for Android",
    "228", "6969"]
    >>> dicti = {"Reza Jam":[]}
    >>> _dict_list_appender_(lst, "It is not fair that we are in #peace and
    there is war in #Iraq and #syria\n", "Reza Jam", dicti)
    {'Mahan Mohamadi': [('Mahan Mohamadi', 'It is not fair that we are in #peace
    and there is war in #Iraq and #syria\n', '1478038431', 'Twitter for Android'
    , '228', '6969')]}
    >>> dicti
    {'Mahan Mohamadi': [('Mahan Mohamadi', 'It is not fair that we are in #peace
    and there is war in #Iraq and #syria\n', '1478038431', 'Twitter for Android'
    , '228', '6969')]}

    >>> lst = ["Megan Fox", "California", "1432689543", "Twitter for Iphone",
    "69", "6985"]
    >>> dicti = {"Megan Fox":[("Megan Fox", "I still miss Matt Barnes. He is
    ferocious", "1465982345", "Twitter for Iphone", "1430", "535")]}
    >>> _dict_list_appender_(lst, "I'm incredibly late to the party but I'm here
    nonetheless, so what now?", "Megan Fox", dicti)
    {'Megan Fox': [('Megan Fox', 'I still miss Matt Barnes. He is ferocious',
    '1465982345', 'Twitter for Iphone', '1430', '535'), ('Megan Fox', "I'm
    incredibly late to the party but I'm here nonetheless, so what now?",
    '1432689543', 'Twitter for Iphone', '69', '6985')]}
    >>> dicti
    {'Megan Fox': [('Megan Fox', 'I still miss Matt Barnes. He is ferocious',
    '1465982345', 'Twitter for Iphone', '1430', '535'), ('Megan Fox', "I'm
    incredibly late to the party but I'm here nonetheless, so what now?",
    '1432689543', 'Twitter for Iphone', '69', '6985')]}
    '''
    lst[1] = value
    dicti[key].append(tuple(lst))
    return dicti
#-------------------------------------------------------------------------------
def _list_modifier_(lst, lines, names):
    '''(list, str, str) -> list

    Return the modified version of the given list by adding items and updating
    it.
    
    >>> lst = []
    >>> _list_modifier_(lst, "793520599560096388,1478038431,Tehran,Twitter for
    Android,228,6969", "Mahan Mohamadi")
    ['Mahan Mohamadi', 'Tehran', '1478038431', 'Twitter for Android', '228',
    '6969']

    >>> lst = []
    >>> _list_modifier_(lst, "7895206574575,1498637859,LA,Twitter for Iphone
    ,608,6895", "Kylie Jenner")
    ['Kylie Jenner', 'LA', '1498637859', 'Twitter for Iphone', '608', '6895']
    '''
    lst = lines.split(",")
    lst[1], lst[2] = lst[2], lst[1]
    lst[0] = names
    return lst