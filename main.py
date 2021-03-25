# Required libraries 
import time
import json
from datetime import date, timedelta, datetime
import requests
import random
import urllib.parse
import ipapi
import pickle
import os
import stdiomask

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, UnexpectedAlertPresentException, NoAlertPresentException



# Define user-agents
PC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63'
MOBILE_USER_AGENT = 'Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0. 3945.79 Mobile Safari/537.36'

POINTS_COUNTER = 0

# Define delay function
def delay ():
    time.sleep(random.randint(2,3))

# Define function to check if config.pickle is empty or not
def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


# Define function to input email and password onto config.pickle using pickle lib
def inputCredentials():
	Accounts = (input('[INPUT] Enter the number of accounts in your Microsoft Family: '))
	numberAccounts = int(Accounts)
	if numberAccounts > 5:
		print('[IP LIMIT] MS Family only allows 5 accounts per IP.')
		inputCredentials()
	else:
		mydict = email_password(numberAccounts)
		with open('config.pickle', 'wb') as handle:
			pickle.dump(mydict, handle, protocol=pickle.HIGHEST_PROTOCOL)

		# Load data (deserialize)
		with open('config.pickle', 'rb') as handle:
			unserialized_data = pickle.load(handle)

		print(mydict == unserialized_data)

	displayCredentials()

# Define display credentials
def displayCredentials():
	# Open config.pickle to unpickle email and password and send to login function
	with open('config.pickle', 'rb') as handle:
				b = pickle.load(handle)
				#print (b)
				
	key_iterable = b.keys()
	key_list = list(key_iterable)
	#print(key_list)

	item_iterable = b.values()
	item_list = list(item_iterable)
	#print(item_list)

	return key_list, item_list;

def email_password(numberAccounts: int):
    mydict = dict()
    i = 1
    while i <= numberAccounts:
    	print('[INPUT] Rewards account '+str(i))
    	email = input("Enter email address: ")
    	email = email.strip()
    	if email == '':
    		break
    	password = stdiomask.getpass('Enter password: ')
    	#password = input("Password: ")
    	password = password.strip()
    	mydict[email] = password
    	#print(mydict)
    	i+=1

    return mydict

# Define browser setup function
def browserSetup(headless_mode: bool = False, user_agent: str = PC_USER_AGENT) -> WebDriver:
    # Create Chrome browser
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument("user-agent=" + user_agent)
    options.add_argument('lang=' + LANG.split("-")[0])
    if headless_mode :
        options.add_argument("--headless")
    options.add_argument('log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_browser_obj = webdriver.Chrome(ChromeDriverManager().install(), options = options)
    return chrome_browser_obj

# Define login function
def login(browser: WebDriver, email: str, pwd: str, isMobile: bool = False):
    # Access to bing.com
    browser.get('https://login.live.com/')
    # Wait complete loading
    waitUntilVisible(browser, By.ID, 'loginHeader', 10)
    # Enter email
    print('[LOGIN]', 'Writing email...')
    browser.find_element_by_name("loginfmt").send_keys(email)
    # Click next
    browser.find_element_by_id('idSIButton9').click()
    # Wait 2 seconds
    time.sleep(2)
    # Wait complete loading
    waitUntilVisible(browser, By.ID, 'loginHeader', 10)
    # Enter password
    #browser.find_element_by_id("i0118").send_keys(pwd)
    browser.execute_script("document.getElementById('i0118').value = '" + pwd + "';")
    print('[LOGIN]', 'Writing password...')
    # Click next
    browser.find_element_by_id('idSIButton9').click()
    # Wait 5 seconds
    time.sleep(5)
    # Click Security Check
    print('[LOGIN]', 'Passing security checks...')
    try:
        browser.find_element_by_id('iLandingViewAction').click()
    except (NoSuchElementException, ElementNotInteractableException) as e:
        pass
    # Wait complete loading
    try:
        waitUntilVisible(browser, By.ID, 'KmsiCheckboxField', 10)
    except (TimeoutException) as e:
        pass
    # Click next
    try:
        browser.find_element_by_id('idSIButton9').click()
        # Wait 5 seconds
        time.sleep(5)
    except (NoSuchElementException, ElementNotInteractableException) as e:
        pass
    print('[LOGIN]', 'Logged-in!')
    # Check Login
    print('[LOGIN]', 'Ensuring login on Bing...')
    checkBingLogin(browser, isMobile)

def checkBingLogin(browser: WebDriver, isMobile: bool = False):
    global POINTS_COUNTER
    #Access Bing.com
    browser.get('https://bing.com/')
    # Wait 8 seconds
    time.sleep(8)
    #Accept Cookies
    try:
        browser.find_element_by_id('bnp_btn_accept').click()
    except:
        pass
    if isMobile:
        try:
            time.sleep(1)
            browser.find_element_by_id('mHamburger').click()
        except:
            try:
                browser.find_element_by_id('bnp_btn_accept').click()
            except:
                pass
            time.sleep(1)
            try:
                browser.find_element_by_id('mHamburger').click()
            except:
                pass
        try:
            time.sleep(1)
            browser.find_element_by_id('HBSignIn').click()
        except:
            pass
        try:
            time.sleep(2)
            browser.find_element_by_id('iShowSkip').click()
            time.sleep(3)
        except:
            if str(browser.current_url).split('?')[0] == "https://account.live.com/proofs/Add":
                input('[LOGIN] Please complete the Security Check on ' + browser.current_url)
                exit()
    #Wait 2 seconds
    time.sleep(2)
    # Refresh page
    browser.get('https://bing.com/')
    # Wait 5 seconds
    time.sleep(10)
    #Update Counter
    try:
        if not isMobile:
            POINTS_COUNTER = int(browser.find_element_by_id('id_rc').get_attribute('innerHTML'))
        else:
            try:
                browser.find_element_by_id('mHamburger').click()
            except:
                try:
                    browser.find_element_by_id('bnp_btn_accept').click()
                except:
                    pass
                time.sleep(1)
                browser.find_element_by_id('mHamburger').click()
            time.sleep(1)
            POINTS_COUNTER = int(browser.find_element_by_id('fly_id_rc').get_attribute('innerHTML'))
    except:
        checkBingLogin(browser, isMobile)

def waitUntilVisible(browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10):
    WebDriverWait(browser, time_to_wait).until(ec.visibility_of_element_located((by_, selector)))

def waitUntilClickable(browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10):
    WebDriverWait(browser, time_to_wait).until(ec.element_to_be_clickable((by_, selector)))

def findBetween(s: str, first: str, last: str) -> str:
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def getCCodeLangAndOffset():
    nfo = ipapi.location()
    lang = nfo['languages'].split(',')[0]
    geo = nfo['country']
    if nfo['utc_offset'] == None:
        tz = str(0)
    else:
        tz = str(round(int(nfo['utc_offset']) / 100 * 60))
    return(lang, geo, tz)

def getGoogleTrends(numberOfwords: int) -> list:
    search_terms = []
    i = 0
    while len(search_terms) < numberOfwords :
        i += 1
        r = requests.get('https://trends.google.com/trends/api/dailytrends?hl=' + LANG + '&ed=' + str((date.today() - timedelta(days = i)).strftime('%Y%m%d')) + '&geo=' + GEO + '&ns=15')
        google_trends = json.loads(r.text[6:])
        for topic in google_trends['default']['trendingSearchesDays'][0]['trendingSearches']:
            search_terms.append(topic['title']['query'].lower())
            for related_topic in topic['relatedQueries']:
                search_terms.append(related_topic['query'].lower())
        search_terms = list(set(search_terms))
    del search_terms[numberOfwords:(len(search_terms)+1)]
    return search_terms

def getRelatedTerms(word: str) -> int:
    r = requests.get('https://api.bing.com/osjson.aspx?query=' + word, headers = {'User-agent': PC_USER_AGENT})
    return r.json()[1]

def resetTabs(browser: WebDriver):
    curr = browser.current_window_handle

    for handle in browser.window_handles:
        if handle != curr:
            browser.switch_to.window(handle)
            time.sleep(0.5)
            browser.close()
            time.sleep(0.5)

    browser.switch_to.window(curr)
    time.sleep(0.5)
    browser.get('https://account.microsoft.com/rewards/')

def getAnswerCode(key: str, string: str) -> str:
	t = 0
	for i in range(len(string)):
		t += ord(string[i])
	t += int(key[-2:], 16)
	return str(t)

def bingSearches(browser: WebDriver, numberOfSearches: int, isMobile: bool = False):
    global POINTS_COUNTER
    i = 0
    search_terms = getGoogleTrends(numberOfSearches)
    for word in search_terms :
        i += 1
        print('[BING]', str(i) + "/" + str(numberOfSearches))
        points = bingSearch(browser, word, isMobile)
        if points <= POINTS_COUNTER :
            relatedTerms = getRelatedTerms(word)
            for term in relatedTerms :
                points = bingSearch(browser, term, isMobile)
                if not points <= POINTS_COUNTER :
                    break
        
        POINTS_COUNTER = points

def bingSearch(browser: WebDriver, word: str, isMobile: bool):
    browser.get('https://bing.com')
    time.sleep(2)
    searchbar = browser.find_element_by_id('sb_form_q')
    searchbar.send_keys(word)
    searchbar.submit()
    time.sleep(random.randint(10, 15))
    points = 0
    try:
        if not isMobile:
            points = int(browser.find_element_by_id('id_rc').get_attribute('innerHTML'))
        else:
            try :
                browser.find_element_by_id('mHamburger').click()
            except UnexpectedAlertPresentException:
                try :
                    browser.switch_to.alert.accept()
                    time.sleep(1)
                    browser.find_element_by_id('mHamburger').click()
                except NoAlertPresentException :
                    pass
            time.sleep(1)
            points = int(browser.find_element_by_id('fly_id_rc').get_attribute('innerHTML'))
    except:
        pass
    return points

def completeDailySetSearch(browser: WebDriver, cardNumber: int):
    time.sleep(5)
    browser.find_element_by_xpath('//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(random.randint(13, 17))
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeDailySetSurvey(browser: WebDriver, cardNumber: int):
    time.sleep(5)
    browser.find_element_by_xpath('//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(8)
    browser.find_element_by_id("btoption" + str(random.randint(0, 1))).click()
    time.sleep(random.randint(10, 15))
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeDailySetQuiz(browser: WebDriver, cardNumber: int):
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(8)
    loaded = False
    while(loaded == False):
        try:
            browser.find_element_by_xpath('//*[@id="rqStartQuiz"]')
            loaded = False
        except:
            time.sleep(0.5)
    browser.find_element_by_xpath('//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    numberOfQuestions = browser.execute_script("return _w.rewardsQuizRenderInfo.maxQuestions")
    numberOfOptions = browser.execute_script("return _w.rewardsQuizRenderInfo.numberOfOptions")
    for question in range(numberOfQuestions):
        if numberOfOptions == 8:
            answers = []
            for i in range(8):
                if browser.find_element_by_id("rqAnswerOption" + str(i)).get_attribute("iscorrectoption").lower() == "False":
                    answers.append("rqAnswerOption" + str(i))
            for answer in answers:
                browser.find_element_by_id(answer).click()
                time.sleep(5)
                tries = 0
                while False:
                    try:
                        browser.find_elements_by_class_name('rqECredits')[0]
                        break
                    except IndexError:
                        if tries < 10:
                            tries += 1
                            time.sleep(0.5)
                        else:
                            browser.refresh()
                            tries = 0
                            time.sleep(5)
            time.sleep(5)
        elif numberOfOptions == 4:
            correctOption = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
            for i in range(4):
                if browser.find_element_by_id("rqAnswerOption" + str(i)).get_attribute("data-option") == correctOption:
                    browser.find_element_by_id("rqAnswerOption" + str(i)).click()
                    time.sleep(5)
                    tries = 0
                    while False:
                        try:
                            browser.find_elements_by_class_name('rqECredits')[0]
                            break
                        except IndexError:
                            if tries < 10:
                                tries += 1
                                time.sleep(0.5)
                            else:
                                browser.refresh()
                                tries = 0
                                time.sleep(5)
                    break
            time.sleep(5)
    time.sleep(5)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeDailySetVariableActivity(browser: WebDriver, cardNumber: int):
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(8)
    try :
        browser.find_element_by_xpath('//*[@id="rqStartQuiz"]').click()
        waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 3)
    except (NoSuchElementException, TimeoutException):
        try:
            counter = str(browser.find_element_by_xpath('//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
            numberOfQuestions = max([int(s) for s in counter.split() if s.isdigit()])
            for question in range(numberOfQuestions):
                browser.execute_script('document.evaluate("//*[@id=\'QuestionPane' + str(question) + '\']/div[1]/div[2]/a[' + str(random.randint(1, 3)) + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
                time.sleep(5)
                browser.find_element_by_xpath('//*[@id="AnswerPane' + str(question) + '"]/div[1]/div[2]/div[4]/a/div/span/input').click()
                time.sleep(3)
            time.sleep(5)
            browser.close()
            time.sleep(2)
            browser.switch_to.window(window_name=browser.window_handles[0])
            time.sleep(2)
            return
        except NoSuchElementException:
            time.sleep(random.randint(5, 9))
            browser.close()
            time.sleep(2)
            browser.switch_to.window(window_name = browser.window_handles[0])
            time.sleep(2)
            return
    time.sleep(3)
    correctAnswer = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
    if browser.find_element_by_id("rqAnswerOption0").get_attribute("data-option") == correctAnswer:
        browser.find_element_by_id("rqAnswerOption0").click()
    else :
        browser.find_element_by_id("rqAnswerOption1").click()
    time.sleep(10)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeDailySetThisOrThat(browser: WebDriver, cardNumber: int):
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    loaded = False
    while(loaded == False):
        try:
            browser.find_element_by_xpath('//*[@id="rqStartQuiz"]')
            loaded = False
        except:
            time.sleep(0.5)
    browser.find_element_by_xpath('//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    for question in range(10):
        answerEncodeKey = browser.execute_script("return _G.IG")

        answer1 = browser.find_element_by_id("rqAnswerOption0")
        answer1Title = answer1.get_attribute('data-option')
        answer1Code = getAnswerCode(answerEncodeKey, answer1Title)

        answer2 = browser.find_element_by_id("rqAnswerOption1")
        answer2Title = answer2.get_attribute('data-option')
        answer2Code = getAnswerCode(answerEncodeKey, answer2Title)

        correctAnswerCode = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")

        if (answer1Code == correctAnswerCode):
            answer1.click()
            time.sleep(8)
        elif (answer2Code == correctAnswerCode):
            answer2.click()
            time.sleep(8)

    time.sleep(5)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)

def getDashboardData(browser: WebDriver) -> dict:
    dashboard = findBetween(browser.find_element_by_xpath('/html/body').get_attribute('innerHTML'), "var dashboard = ", ";\n        appDataModule.constant(\"prefetchedDashboard\", dashboard);")
    dashboard = json.loads(dashboard)
    return dashboard

def completeDailySet(browser: WebDriver):
    d = getDashboardData(browser)['dailySetPromotions']
    todayDate = datetime.today().strftime('%m/%d/%Y')
    todayPack = []
    for date, data in d.items():
        if date == todayDate:
            todayPack = data
    for activity in todayPack:
        try:
            if activity['complete'] == False:
                cardNumber = int(activity['offerId'][-1:])
                if activity['promotionType'] == "urlreward":
                    print('[DAILY SET]', 'Completing search of card ' + str(cardNumber))
                    completeDailySetSearch(browser, cardNumber)
                if activity['promotionType'] == "quiz":
                    if activity['pointProgressMax'] == 50:
                        print('[DAILY SET]', 'Completing This or That of card ' + str(cardNumber))
                        completeDailySetThisOrThat(browser, cardNumber)
                    elif activity['pointProgressMax'] == 40 or activity['pointProgressMax'] == 30:
                        print('[DAILY SET]', 'Completing quiz of card ' + str(cardNumber))
                        completeDailySetQuiz(browser, cardNumber)
                    elif activity['pointProgressMax'] == 10:
                        searchUrl = urllib.parse.unquote(urllib.parse.parse_qs(urllib.parse.urlparse(activity['destinationUrl']).query)['ru'][0])
                        searchUrlQueries = urllib.parse.parse_qs(urllib.parse.urlparse(searchUrl).query)
                        filters = {}
                        for filter in searchUrlQueries['filters'][0].split(" "):
                            filter = filter.split(':', 1)
                            filters[filter[0]] = filter[1]
                        if "PollScenarioId" in filters:
                            print('[DAILY SET]', 'Completing poll of card ' + str(cardNumber))
                            completeDailySetSurvey(browser, cardNumber)
                        else:
                            print('[DAILY SET]', 'Completing quiz of card ' + str(cardNumber))
                            completeDailySetVariableActivity(browser, cardNumber)
        except:
            resetTabs(browser)

def getAccountPoints(browser: WebDriver) -> int:
    return getDashboardData(browser)['userStatus']['availablePoints']

def completePunchCard(browser: WebDriver, url: str, childPromotions: dict):
    browser.get(url)
    for child in childPromotions:
        if child['complete'] == False:
            if child['promotionType'] == "urlreward":
                browser.execute_script("document.getElementsByClassName('offer-cta')[0].click()")
                time.sleep(1)
                browser.switch_to.window(window_name = browser.window_handles[1])
                time.sleep(random.randint(13, 17))
                browser.close()
                time.sleep(2)
                browser.switch_to.window(window_name = browser.window_handles[0])
                time.sleep(2)
            if child['promotionType'] == "quiz":
                browser.execute_script("document.getElementsByClassName('offer-cta')[0].click()")
                time.sleep(1)
                browser.switch_to.window(window_name = browser.window_handles[1])
                time.sleep(8)
                counter = str(browser.find_element_by_xpath('//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
                numberOfQuestions = max([int(s) for s in counter.split() if s.isdigit()])
                for question in range(numberOfQuestions):
                    browser.execute_script('document.evaluate("//*[@id=\'QuestionPane' + str(question) + '\']/div[1]/div[2]/a[' + str(random.randint(1, 3)) + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
                    time.sleep(5)
                    browser.find_element_by_xpath('//*[@id="AnswerPane' + str(question) + '"]/div[1]/div[2]/div[4]/a/div/span/input').click()
                    time.sleep(3)
                time.sleep(5)
                browser.close()
                time.sleep(2)
                browser.switch_to.window(window_name = browser.window_handles[0])
                time.sleep(2)

def completePunchCards(browser: WebDriver):
    punchCards = getDashboardData(browser)['punchCards']
    for punchCard in punchCards:
        try:
            if punchCard['parentPromotion'] != None and punchCard['childPromotions'] != None and punchCard['parentPromotion']['complete'] == False and punchCard['parentPromotion']['pointProgressMax'] != 0:
                url = punchCard['parentPromotion']['attributes']['destination']
                path = url.replace('https://account.microsoft.com/rewards/dashboard/','')
                userCode = path[:4]
                dest = 'https://account.microsoft.com/rewards/dashboard/' + userCode + path.split(userCode)[1]
                completePunchCard(browser, dest, punchCard['childPromotions'])
        except:
            resetTabs(browser)
    time.sleep(2)
    browser.get('https://account.microsoft.com/rewards/')
    time.sleep(2)

def completeMorePromotionSearch(browser: WebDriver, cardNumber: int):
    browser.find_element_by_xpath('//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(random.randint(13, 17))
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeMorePromotionQuiz(browser: WebDriver, cardNumber: int):
    browser.find_element_by_xpath('//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    loaded = False
    while(loaded == False):
        try:
            browser.find_element_by_xpath('//*[@id="rqStartQuiz"]')
            loaded = False
        except:
            time.sleep(0.5)
    browser.find_element_by_xpath('//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    numberOfQuestions = browser.execute_script("return _w.rewardsQuizRenderInfo.maxQuestions")
    numberOfOptions = browser.execute_script("return _w.rewardsQuizRenderInfo.numberOfOptions")
    for question in range(numberOfQuestions):
        if numberOfOptions == 8:
            answers = []
            for i in range(8):
                if browser.find_element_by_id("rqAnswerOption" + str(i)).get_attribute("iscorrectoption").lower() == "False":
                    answers.append("rqAnswerOption" + str(i))
            for answer in answers:
                browser.find_element_by_id(answer).click()
                time.sleep(5)
                tries = 0
                while False:
                    try:
                        browser.find_elements_by_class_name('rqECredits')[0]
                        break
                    except IndexError:
                        if tries < 10:
                            tries += 1
                            time.sleep(0.5)
                        else:
                            browser.refresh()
                            tries = 0
                            time.sleep(5)
            time.sleep(5)
        elif numberOfOptions == 4:
            correctOption = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
            for i in range(4):
                if browser.find_element_by_id("rqAnswerOption" + str(i)).get_attribute("data-option") == correctOption:
                    browser.find_element_by_id("rqAnswerOption" + str(i)).click()
                    time.sleep(5)
                    tries = 0
                    while False:
                        try:
                            browser.find_elements_by_class_name('rqECredits')[0]
                            break
                        except IndexError:
                            if tries < 10:
                                tries += 1
                                time.sleep(0.5)
                            else:
                                browser.refresh()
                                tries = 0
                                time.sleep(5)
                    break
            time.sleep(5)
    time.sleep(5)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)

def completeMorePromotionABC(browser: WebDriver, cardNumber: int):
    browser.find_element_by_xpath('//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    counter = str(browser.find_element_by_xpath('//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
    numberOfQuestions = max([int(s) for s in counter.split() if s.isdigit()])
    for question in range(numberOfQuestions):
        browser.execute_script('document.evaluate("//*[@id=\'QuestionPane' + str(question) + '\']/div[1]/div[2]/a[' + str(random.randint(1, 3)) + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        time.sleep(5)
        browser.find_element_by_xpath('//*[@id="AnswerPane' + str(question) + '"]/div[1]/div[2]/div[4]/a/div/span/input').click()
        time.sleep(3)
    time.sleep(5)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)

def completeMorePromotionThisOrThat(browser: WebDriver, cardNumber: int):
    browser.find_element_by_xpath('//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    loaded = False
    while(loaded == False):
        try:
            browser.find_element_by_xpath('//*[@id="rqStartQuiz"]')
            loaded = False
        except:
            time.sleep(0.5)
    browser.find_element_by_xpath('//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    for question in range(10):
        answerEncodeKey = browser.execute_script("return _G.IG")

        answer1 = browser.find_element_by_id("rqAnswerOption0")
        answer1Title = answer1.get_attribute('data-option')
        answer1Code = getAnswerCode(answerEncodeKey, answer1Title)

        answer2 = browser.find_element_by_id("rqAnswerOption1")
        answer2Title = answer2.get_attribute('data-option')
        answer2Code = getAnswerCode(answerEncodeKey, answer2Title)

        correctAnswerCode = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")

        if (answer1Code == correctAnswerCode):
            answer1.click()
            time.sleep(8)
        elif (answer2Code == correctAnswerCode):
            answer2.click()
            time.sleep(8)

    time.sleep(5)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)

def completeMorePromotions(browser: WebDriver):
    morePromotions = getDashboardData(browser)['morePromotions']
    i = 0
    for promotion in morePromotions:
        try:
            i += 1
            if promotion['complete'] == False and promotion['pointProgressMax'] != 0:
                if promotion['promotionType'] == "urlreward":
                    completeMorePromotionSearch(browser, i)
                elif promotion['promotionType'] == "quiz":
                    if promotion['pointProgressMax'] == 10:
                        completeMorePromotionABC(browser, i)
                    elif promotion['pointProgressMax'] == 30 or promotion['pointProgressMax'] == 40:
                        completeMorePromotionQuiz(browser, i)
                    elif promotion['pointProgressMax'] == 50:
                        completeMorePromotionThisOrThat(browser, i)
                else:
                    if promotion['pointProgressMax'] == 100 or promotion['pointProgressMax'] == 200:
                        completeMorePromotionSearch(browser, i)
        except:
            resetTabs(browser)

def getRemainingSearches(browser: WebDriver):
    dashboard = getDashboardData(browser)
    searchPoints = 1
    counters = dashboard['userStatus']['counters']
    progressDesktop = counters['pcSearch'][0]['pointProgress'] + counters['pcSearch'][1]['pointProgress']
    targetDesktop = counters['pcSearch'][0]['pointProgressMax'] + counters['pcSearch'][1]['pointProgressMax']
    if targetDesktop == 33 :
        #Level 1 EU
        searchPoints = 3
    elif targetDesktop == 55 :
        #Level 1 US
        searchPoints = 5
    elif targetDesktop == 102 :
        #Level 2 EU
        searchPoints = 3
    elif targetDesktop >= 170 :
        #Level 2 US
        searchPoints = 5
    remainingDesktop = int((targetDesktop - progressDesktop) / searchPoints)
    remainingMobile = 0
    if dashboard['userStatus']['levelInfo']['activeLevel'] != "Level1":
        progressMobile = counters['mobileSearch'][0]['pointProgress']
        targetMobile = counters['mobileSearch'][0]['pointProgressMax']
        remainingMobile = int((targetMobile - progressMobile) / searchPoints)
    return(remainingDesktop, remainingMobile)


print("""
██████╗ ███████╗██╗    ██╗ █████╗ ██████╗ ██████╗ ███████╗    ██████╗  ██████╗ ████████╗
██╔══██╗██╔════╝██║    ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝
██████╔╝█████╗  ██║ █╗ ██║███████║██████╔╝██║  ██║███████╗    ██████╔╝██║   ██║   ██║   
██╔══██╗██╔══╝  ██║███╗██║██╔══██║██╔══██╗██║  ██║╚════██║    ██╔══██╗██║   ██║   ██║   
██║  ██║███████╗╚███╔███╔╝██║  ██║██║  ██║██████╔╝███████║    ██████╔╝╚██████╔╝   ██║   
╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝    ╚═════╝  ╚═════╝    ╚═╝   
""")
print("         Powered by: Passivebot.com              version 1.0\n")

LANG, GEO, TZ = getCCodeLangAndOffset()

#ticker used to determine if email.pickle is empty or not
ticker = is_non_zero_file('config.pickle')


if ticker ==0:
	print ("[LOGIN] Provide input credentials...")
	inputCredentials()
else:
	print ("[LOGIN] Retrieving credentials...")
	key_list, item_list = displayCredentials()
	for key, item in zip(key_list, item_list):
		#print(key, item)
		print('********************'+str.upper(key)+'********************')
		browser = browserSetup(False, PC_USER_AGENT)
		print('[LOGIN]', 'Logging-in...')
		login(browser, key, item)
		print('[LOGIN] Logged-in successfully !')
		startingPoints = POINTS_COUNTER
		print('[POINTS] You have ' + str(POINTS_COUNTER) + ' points on your account !')
		browser.get('https://account.microsoft.com/rewards/')
		print('[DAILY SET]', 'Trying to complete the Daily Set...')
		completeDailySet(browser)
		print('[DAILY SET] Completed the Daily Set successfully !')
		print('[PUNCH CARDS]', 'Trying to complete the Punch Cards...')
		completePunchCards(browser)
		print('[PUNCH CARDS] Completed the Punch Cards successfully !')
		print('[MORE PROMO]', 'Trying to complete More Promotions...')
		completeMorePromotions(browser)
		print('[MORE PROMO] Completed More Promotions successfully !')
		remainingSearches, remainingSearchesM = getRemainingSearches(browser)
		if remainingSearches != 0:
			print('[BING]', 'Starting Desktop and Edge Bing searches...')
			bingSearches(browser, remainingSearches)
			print('[BING] Finished Desktop and Edge Bing searches !')
			browser.quit()

		if remainingSearchesM != 0:
			browser = browserSetup(False, MOBILE_USER_AGENT)
			print('[LOGIN]', 'Logging-in...')
			login(browser, key, item, False)
			print('[LOGIN]', 'Logged-in successfully !')
			print('[BING]', 'Starting Mobile Bing searches...')
			bingSearches(browser, remainingSearchesM, False)
			print('[BING] Finished Mobile Bing searches !')
			browser.quit()

			print('[POINTS] You have earned ' + str(POINTS_COUNTER - startingPoints) + ' points today !')
			print('[POINTS] You are now at ' + str(POINTS_COUNTER) + ' points !\n')
	
	delay()
	browser.close()
	print('POWERED BY PASSIVEBOT.COM')
	input()
	browser.quit()

