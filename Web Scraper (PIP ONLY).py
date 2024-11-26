from selenium import webdriver
from selenium.webdriver.common.by import By
from chromedriver_py import binary_path

cService = webdriver.ChromeService(executable_path=binary_path) #For pip version use binary_path instead of Chrome Driver install location
driver = webdriver.Chrome(service = cService)

url = 'https://www.bmet.ac.uk/courses/' #Url being searched

driver.get(url)#Opens chrome tab with the url provided

numberOfCourses = '/html/body/main/article/section[2]/div/div[1]/div/div[1]/h3[1]' #XPath of element containing the number of courses on the site

link = driver.find_element(By.XPATH, numberOfCourses)
numberOfCourses = int(link.text.split(" ")[0])

for x in range(1,numberOfCourses+1):
    print(driver.find_element(By.XPATH, "/html/body/main/article/section[2]/div/div[2]/div/div/div["+str(x)+"]/a/div[1]/div/div[3]").text)

driver.close() #Closes the chrome window that it opens

#Layout of the XPath for each course
#/html/body/main/article/section[2]/div/div[2]/div/div/div[1]/a/div[1]/div/div[3]
#/html/body/main/article/section[2]/div/div[2]/div/div/div[2]/a/div[1]/div/div[3]
#...
#/html/body/main/article/section[2]/div/div[2]/div/div/div[266]/a/div[1]/div/div[3]

#XPath of the number of courses
#/html/body/main/article/section[2]/div/div[1]/div/div[1]/h3[1]
