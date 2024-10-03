from selenium import webdriver
from selenium.webdriver.common.by import By

cService = webdriver.ChromeService(executable_path='C:/Users/Muna2/Downloads/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service = cService)

url = 'https://www.bmet.ac.uk/courses/'

driver.get(url)

numberOfCourses = '/html/body/main/article/section[2]/div/div[1]/div/div[1]/h3[1]'

link = driver.find_element(By.XPATH, numberOfCourses)
numberOfCourses = int(link.text.split(" ")[0])

for x in range(1,numberOfCourses+1):
    print(driver.find_element(By.XPATH, "/html/body/main/article/section[2]/div/div[2]/div/div/div["+str(x)+"]/a/div[1]/div/div[3]").text)


#/html/body/main/article/section[2]/div/div[2]/div/div/div[1]/a/div[1]/div/div[3]
#/html/body/main/article/section[2]/div/div[2]/div/div/div[2]/a/div[1]/div/div[3]
#/html/body/main/article/section[2]/div/div[2]/div/div/div[3]/a/div[1]/div/div[3]
#/html/body/main/article/section[2]/div/div[2]/div/div/div[4]/a/div[1]/div/div[3]
#/html/body/main/article/section[2]/div/div[2]/div/div/div[5]/a/div[1]/div/div[3]
#...
#/html/body/main/article/section[2]/div/div[2]/div/div/div[266]/a/div[1]/div/div[3]

#/html/body/main/article/section[2]/div/div[1]/div/div[1]/h3[1] (Number of Courses)
