#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 16:36:15 2021

@author: haroldribeiro
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd


def get_jobs(path,keyword,days,num_jobs, verbose,s_time):
    
    #including hyhpen
    keyword = keyword.replace(' ','-')
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
   
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path+"/chromedriver", options=options)
    driver.set_window_size(1120, 1000)

    #url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    #url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=&locId=&jobType="
    url = "https://www.glassdoor.com/Job/us-" + keyword + "-jobs-SRCH_IL.0,2_IN1_KO3,17.htm?fromAge=" + days + "&includeNoSalaryJobs=true"
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(s_time)

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element_by_class_name("eigr9kq3").click()    
           #driver.find_element_by_css_selector('[alt="Close"]').click 
        except ElementClickInterceptedException:
        #except:
            print("error on click element")
            pass
            

        time.sleep(2)

        try:
            driver.find_element_by_css_selector('[alt="Close"]').click() #clicking to the X.
            #SVGInline-svg modal_closeIcon-svg
            print(' x out worked')
        except NoSuchElementException:
            print(' x out failed')
            pass
        
        #Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("eigr9kq3")  #jl for Job Listing. These are the buttons we're going to click.
        
        for job_button in job_buttons:  
        
            try:

                print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
                
                if len(jobs) >= num_jobs:
                    #print("bigger than the qty")
                    break
    
                job_button.click()  #You might 
                
                collected_successfully = False
                
                time.sleep(1.5)
                
                while not collected_successfully:
                    try:
                        print("try collection successfully")
                        company_name = driver.find_element_by_xpath('.//div[@class="css-87uc0g e1tk4kwz1"]').text
                        #print(company_name)               
                        location = driver.find_element_by_xpath('.//div[@class="css-56kyx5 e1tk4kwz5"]').text
                        #print(location)  
                        job_title = driver.find_element_by_xpath('.//div[contains(@class, "e1tk4kwz4")]').text
                        #print(job_title)  
                        job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                        #print(job_description)  
                        collected_successfully = True                    
                    except:
                        print("try collection exception")
                        time.sleep(3)
                        pass
    
                try:
                    salary_estimate = driver.find_element_by_xpath('.//span[@class="css-56kyx5 css-16kxj2j e1wijj242"]').text
                except:
                #except NoSuchElementException:
                    print("salary exception")
                    salary_estimate = -1 #You need to set a "not found value. It's important."
                    pass
                
                try:
                    rating = driver.find_element_by_xpath('.//span[contains(@class,"e1tk4kwz2")]').text
                except:
                #except NoSuchElementException:
                    print("rating exception")
                    rating = -1 #You need to set a "not found value. It's important."
                    pass
    
                #Printing for debugging
                if verbose:
                    print("Job Title: {}".format(job_title))
                    print("Salary Estimate: {}".format(salary_estimate))
                    print("Job Description: {}".format(job_description[:500]))
                    print("Rating: {}".format(rating))
                    print("Company Name: {}".format(company_name))
                    print("Location: {}".format(location))
    
                #Going to the Company tab...
                #clicking on this:
                #<div class="tab" data-tab-type="overview"><span>Company</span></div>
                try:
                    driver.find_element_by_xpath('.//div[@data-item="tab" and @data-tab-type="overview"]').click()
                    
                    time.sleep(4)
    
                    try:
                        #<div class="infoEntity">
                        #    <label>Headquarters</label>
                        #    <span class="value">San Francisco, CA</span>
                        #</div>
                        headquarters = driver.find_element_by_xpath('.//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Headquarters"]//following-sibling::*').text
                    except:
                    #except NoSuchElementException:
                        print("headquarters exception")
                        headquarters = -1
                        pass
    
                    try:
                        size = driver.find_element_by_xpath('.//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Size"]//following-sibling::*').text
                    except:
                    #except NoSuchElementException:
                        print("size exception")
                        size = -1
                        pass
    
                    try:
                        founded = driver.find_element_by_xpath('.//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Founded"]//following-sibling::*').text
                    except:
                    #except NoSuchElementException:
                        print("founded excpetion")
                        founded = -1
                        pass
    
                    try:
                        type_of_ownership = driver.find_element_by_xpath('.//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Type"]//following-sibling::*').text
                    except:
                    #except NoSuchElementException:
                        print("ownership exception")
                        type_of_ownership = -1
                        pass
    
                    try:
                        industry = driver.find_element_by_xpath('.//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Industry"]//following-sibling::*').text
                    except:
                    #except NoSuchElementException:
                        print("industry exception")
                        industry = -1
                        pass
    
                    try:
                        sector = driver.find_element_by_xpath('.//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Sector"]//following-sibling::*').text
                    except:
                    #except NoSuchElementException:
                        print("sector exception")
                        sector = -1
                        pass
    
                    try:
                        revenue = driver.find_element_by_xpath('.//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Revenue"]//following-sibling::*').text
                    except:
                    #except NoSuchElementException:
                        print("reveneu exception")
                        revenue = -1
                        pass
    
                    try:
                        competitors = driver.find_element_by_xpath('.//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Competitors"]//following-sibling::*').text
                    except:
                    #except NoSuchElementException:
                        print("competitors exception")
                        competitors = -1
                        pass
    
                #except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                except:
                    headquarters = -1
                    size = -1
                    founded = -1
                    type_of_ownership = -1
                    industry = -1
                    sector = -1
                    revenue = -1
                    competitors = -1
                    pass
    
                    
                if verbose:
                    print("Headquarters: {}".format(headquarters))
                    print("Size: {}".format(size))
                    print("Founded: {}".format(founded))
                    print("Type of Ownership: {}".format(type_of_ownership))
                    print("Industry: {}".format(industry))
                    print("Sector: {}".format(sector))
                    print("Revenue: {}".format(revenue))
                    print("Competitors: {}".format(competitors))
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    
                jobs.append({"Job Title" : job_title,
                "Salary Estimate" : salary_estimate,
                "Job Description" : job_description,
                "Rating" : rating,
                "Company Name" : company_name,
                "Location" : location,
                "Headquarters" : headquarters,
                "Size" : size,
                "Founded" : founded,
                "Type of ownership" : type_of_ownership,
                "Industry" : industry,
                "Sector" : sector,
                "Revenue" : revenue,
                "Competitors" : competitors})           
                #add job to jobs
            
            # Appending data into csv
            except Exception as e:
                print(e)
                return pd.DataFrame(jobs) #This line converts the dictionary object into a pandas DataFrame.
          
            
           
        #Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('.//li[@class="css-114lpwu e1gri00l4"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
