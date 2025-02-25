from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.firefox.options import Options
import time

opts = Options()
opts.add_argument("--headless")#Run without GUI so less resource intensive

driver = webdriver.Firefox(options=opts) #Webdriver
driver.command_executor._client_config._timeout = 10000 #Timeout increased so program does not quit early
baseUrl = 'https://www.bmet.ac.uk/courses/' #Url being searched
driver.get(baseUrl)#Opens internet tab with the url provided

numberOfCourses = '/html/body/main/article/section[2]/div/div[1]/div/div[1]/h3[1]'
link = driver.find_element(By.XPATH, numberOfCourses)#Get number of courses
numberOfCourses = int(link.text.split(" ")[0])
pagesWithErrors = []

for x in range(numberOfCourses):#Keep running until all courses have been checked
    print(x)
    vidExist = False
    progExist = False
    errors = []
    driver.find_elements(By.CLASS_NAME,"course-search-result__inner")[x].click()#Navigate to selected course
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
        errors.append("Program Data Section Missing")

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
            errors.append("Program Data has an Error")
        driver.switch_to.window(driver.window_handles[0]) #Switch back to original driver window

    #If there is an error then add the URL and the errors to the pagesWithErrors list
    if len(errors)>1:
        pagesWithErrors.append(errors)
    driver.back()

driver.close() #Closes the chrome window that it opens

print(pagesWithErrors)

