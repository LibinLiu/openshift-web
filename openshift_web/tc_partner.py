from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
import baseutils
import config
import HTMLTestRunner


class Partner(unittest.TestCase):

    def setUp(self):
        self.driver = ""
        self.base_url = ""
        self.profile = ""
        self.binary= ""
        self.verificationErrors = []
        baseutils.initiate(self)

#Check Partners page contents    
    def test_check_partner_contents(self):
        baseutils.go_to_partners(self)
        baseutils.assert_text_equal_by_css(self,"MEET OUR PARTNERS","section.main > header > h1")
        partners=["img[alt='Couchbase']","img[alt='Zend']","img[alt='Opencrowd']","img[alt='Mudynamics']","img[alt='Dyn']","img[alt='Appcelerator']","img[alt='Exo']","img[alt='Bitnami']","img[alt='Opsource']","img[alt='Enterprisedb']","img[alt='Cotendo']","img[alt='10gen']"]
        for p in partners:
            baseutils.assert_element_present_by_css(self,p)
            


    
# Check partners page links
    def test_check_partners_link(self):
        baseutils.go_to_partners(self)
        __learnMorelinks=["//a[contains(@href, '/app/partners/couchbase')]"]
        __learnMorelinks+=["//a[contains(@href, '/app/partners/zend')]"]
        __learnMorelinks+=["//a[contains(@href, '/app/partners/opencrowd')]"]
        __learnMorelinks+=["//a[contains(@href, '/app/partners/mu-dynamics')]"]
        __learnMorelinks+=["//a[contains(@href, '/app/partners/dyn')]"]
        __learnMorelinks+=["//a[contains(@href, '/app/partners/appcelerator')]"]
        __learnMorelinks+=["//a[contains(@href, '/app/partners/exo')]"]
        __learnMorelinks+=["//a[contains(@href, '/app/partners/bitnami')]"]
        __learnMorelinks+=["//a[contains(@href, '/app/partners/opsource')]"]
        __learnMorelinks+=["//a[contains(@href, '/app/partners/enterprisedb')]"]
        __learnMorelinks+=["//a[contains(@href, '/app/partners/cotendo')]"]
        __learnMorelinks+=["//a[contains(@href, '/app/partners/10gen')]"]
        __partnerTitles=["OpenShift by Red Hat | Partnership with Couchbase"]
        __partnerTitles+=["OpenShift by Red Hat | Partnership with Zend"]
        __partnerTitles+=["OpenShift by Red Hat | Partnership with Opencrowd"]
        __partnerTitles+=["OpenShift by Red Hat | Partnership with Mu Dynamics"]
        __partnerTitles+=["OpenShift by Red Hat | Partnership with Dyn"]
        __partnerTitles+=["OpenShift by Red Hat | Partnership with Appcelerator"]
        __partnerTitles+=["OpenShift by Red Hat | Partnership with eXo"]
        __partnerTitles+=["OpenShift by Red Hat | Partnership with BitNami"]
        __partnerTitles+=["OpenShift by Red Hat | Partnership with OpSource"]
        __partnerTitles+=["OpenShift by Red Hat | Partnership with EnterpriseDB"]
        __partnerTitles+=["OpenShift by Red Hat | Partnership with Cotendo"]
        __partnerTitles+=["OpenShift by Red Hat | Partnership with MongoDB by 10gen"]
        __partnerlink="//div[@id='partner_overview']/a"
        for i in range(len(__learnMorelinks)):
               baseutils.click_element_by_xpath(self,__learnMorelinks[i])
               time.sleep(2)
               baseutils.check_title(self,__partnerTitles[i])
               baseutils.go_to_partners(self)
               time.sleep(2)
    
        
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
        

if __name__ == "__main__":
    unittest.main()
    #HTMLTestRunner.main()

