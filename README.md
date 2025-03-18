To use the BMET Course Scraper.py just pip install selenium and the chrome driver

Selenium:
pip install selenium

Chrome Driver:
pip install chromedriver-py

-------------------------------------------BMET Individual Courses Checker.py ------------------------------------------------------  
NOTE: If you are having problems with the drivers being out of date make sure to check Selenium version so that it works with the latest chrome if not then see if there is an update and update Selenium.

The Individual Course checker also just needs selenium. But no Chrome or Firefox Driver as I found out Selenium has it built in.

KEY:  
Missing Apply/Enquire Section = The apply/enquire section is completely missing (This does not check if individual buttons are missing just the section itself)  
Missing Video Section = The entire video section is missing  
Video is wrong file type = Video section is there but the file type given to it is wrong (Usually image is given instead of an mp4)  
Program Data Section is missing = The entire EMSI section is missing  
Program Data has an Error = EMSI section is there but there is an error (The 2 errors I have seen are "Program data cannot be found" see "Access to Education and Teaching - Online" and "Career data cannot be found" see "Understanding Safeguarding and Prevent Certificate Level 2")

Format of results in the end is [URL, Error 1, Error 2, etc.]   
Order is in Key Order listed above so Apply error will appear before Video Errors if they both exist
