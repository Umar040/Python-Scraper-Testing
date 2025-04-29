from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
import csv
import datetime

opts = Options()
opts.add_argument("--headless")#Run without GUI so less resource intensive

driver = webdriver.Chrome(options=opts) #Webdriver
driver.command_executor._client_config._timeout = 10000 #Timeout increased so program does not quit early
baseUrl = 'https://www.bmet.ac.uk/courses/' #Url being searched
driver.get(baseUrl)#Opens internet tab with the url provided
driver.implicitly_wait(10)
driver.find_element(By.XPATH,"/html/body/div[3]/div/div/div/div[2]/button[2]").click()
numberOfCourses = '/html/body/main/article/section[2]/div/div[1]/div/div[1]/h3[1]'
link = driver.find_element(By.XPATH, numberOfCourses)#Get number of courses
numberOfCourses = int(link.text.split(" ")[0])
pagesWithErrors = []
errorWhileRunning = False

start = int(input("There is "+str(numberOfCourses)+" number of courses. Enter the starting value of the scraper:"))
end = int(input("Now the ending value:"))

for x in range(start-1,end):#Keep running until all courses have been checked from range specified by user
    try:
        print(x)
        vidExist = False
        progExist = False
        errors = []
        driver.implicitly_wait(5)
        driver.find_elements(By.CLASS_NAME,"course-search-result__inner")[x].click()
        errors.append(driver.current_url)
        #Missing Apply/Enquire Section Check
        try:
            applySec = driver.find_element(By.CLASS_NAME,"crs_schedule")
        except NoSuchElementException:
            errors.append("Missing Apply/Enquire Section")

        #Missing Video Section Check
        try:
            video = driver.find_element(By.CLASS_NAME,"crs_video")
            vidExist = True
        except NoSuchElementException:
            errors.append("Video Section Missing")

        #Video File Type Check
        if vidExist:
            video = driver.find_element(By.XPATH,"//section[@class='crs_video']/div/div/video/source")
            video = video.get_attribute("src")
            if video[-3:] != "mp4":
                errors.append("Video is wrong file type")

        #Program Data(EMSI) Section Check
        try:
            programData = driver.find_element(By.CLASS_NAME,"crs_careers")
            progExist = True
        except NoSuchElementException:
            errors.append("EMSI Section Missing")

        #Program Data(EMSI) Error Check
        if progExist:
            driver.switch_to.frame(frame_reference=driver.find_element(By.XPATH,"//iframe[contains(@id,'widget')]"))
            again=False
            try:
                progError = driver.find_element(By.XPATH,"//div[@id='__next']/div")
                progError = progError.get_attribute("class")[:5]
            except StaleElementReferenceException:
                again=True
            #Does the above code again if Stale Reference as it would happen after running for a while
            if again:
                progError = driver.find_element(By.XPATH,"//div[@id='__next']/div")
                progError = progError.get_attribute("class")[:5]
            if progError == "Error":
                errors.append("EMSI has an Error")
            driver.switch_to.window(driver.window_handles[0]) #Switch back to original driver window

        #If there is an error then add the URL and the errors to the pagesWithErrors list
        if len(errors)>1:
            pagesWithErrors.append(errors)
        driver.back()
    except (StaleElementReferenceException,NoSuchElementException,IndexError):
        errorWhileRunning = True
        stoppedAt = str(x)

driver.close() #Closes the chrome window that it opens


with open('BMET Course Data.csv', 'a', newline='') as File:#Create or Open CSV File with given name in write mode
    csvWrite = csv.writer(File, quoting=csv.QUOTE_ALL)
    csvWrite.writerow([datetime.datetime.now()])
    if errorWhileRunning:
        csvWrite.writerow(["Error happened while running","Stopped at "+stoppedAt])
    csvWrite.writerow(['Course URL', 'Does the page have a Apply/Enquire section?','Does the page have a video section?','Is the video file type correct?','Does the page have EMSI?', 'Does the EMSI work correctly?'])
    for x in pagesWithErrors:#For each error check if it exists then add it to the list
        check=1
        addList = [x[0]]
        if x[check] == "Missing Apply/Enquire Section":
            addList.append(x[check])
            if check+1 > len(x)-1:
                pass
            else:
                check+=1
        else:
            addList.append("")
        if x[check] == "Video Section Missing":
            addList.append(x[check])
            if check+1 > len(x)-1:
                pass
            else:
                check+=1
        else:
            addList.append("")
        if x[check] == "Video is wrong file type":
            addList.append(x[check])
            if check+1 > len(x)-1:
                pass
            else:
                check+=1
        else:
            addList.append("")
        if x[check] == "EMSI Section Missing":
            addList.append(x[check])
            if check+1 > len(x)-1:
                pass
            else:
                check+=1
        else:
            addList.append("")
        if x[check] == "EMSI has an Error":
            addList.append(x[check])
            if check+1 > len(x)-1:
                pass
            else:
                check+=1
        else:
            addList.append("")
        csvWrite.writerow(addList)#Write the list to the CSV as a new row
        
print(pagesWithErrors)

