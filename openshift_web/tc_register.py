from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
import baseutils
import config
import HTMLTestRunner
import random

class RegisterPage(unittest.TestCase):
    def setUp(self):
        self.driver = ""
        self.base_url = ""
        self.profile = ""
        self.verificationErrors = []
        baseutils.initiate(self)
    '''
    def test_check_register_form(self):
        baseutils.go_to_signup(self)
        baseutils.assert_text_equal_by_css(self,"Sign up for OpenShift - it's Easy!","#signup > header > h1")
        baseutils.click_element_by_xpath(self,"//a[contains(text(),'Already have a redhat.com or RHN account?')]")
        baseutils.is_element_hidden(self,By.ID,"signup")
        baseutils.is_element_displayed(self,By.ID,"login-form")
        baseutils.click_element_by_css_no_wait(self,"#signup > a.close_button > img")
        baseutils.is_element_hidden(self,By.ID,"login-form")
    '''

    def get_confirm_link(self):
        self.driver.get("http://post-office.corp.redhat.com/archives/libra-test/")
        self.driver.find_element_by_xpath("html/body/table/tbody/tr[2]/td[2]/a[1]").click()
        elements=self.driver.find_elements_by_link_text("Confirm your Red Hat account")
        elements.reverse()
        for element in elements :
            #print element.text
            element.click()
            time.sleep(3)
            email=self.driver.find_element_by_xpath("//li[2]").text
            time.sleep(2)
            # print email
            # extract the user name
            if config.new_user[0:23] in email[5:29]:break
            self.driver.back()
        _confirm_link=self.driver.find_element_by_xpath("//pre/a").get_attribute('href')
        print _confirm_link
        baseutils.update_config_file('environment','confirm_url_express',_confirm_link)
              #  print self.driver.find_element_by_xpath("html/body/pre/a").text
                #break
            #self.driver.back()

    def test_register_normally(self):
        i=random.uniform(1,10)
        generate_new_user="libra-test+stage"+str(i)[3:10]+"@redhat.com"
        baseutils.update_config_file('environment','new_user',generate_new_user)
        baseutils.go_to_signup(self)
        baseutils.register_a_user(self,config.new_user,config.password,config.password,True)
        time.sleep(5)
        baseutils.is_text_equal_by_xpath(self,"WHAT'S NEXT?","html/body/section/header/h1")
        self.get_confirm_link()
        #baseutils.update_config_file('environment','confirm_url_express',_confirm_link)

    def test_register_with_existing_user(self):
        baseutils.go_to_signup(self)
        baseutils.register_a_user(self,config.granted_user[0],config.granted_user[1],config.granted_user[1],True)
        time.sleep(5)
        baseutils.is_text_equal_by_xpath(self,"A user with the same email is already registered",".//*[@id='new-user']/div[1]/div") 

    def test_register_with_mismatch_pwd(self):
  #      baseutils.go_to_home(self)
        baseutils.go_to_signup(self)
        baseutils.register_a_user(self,config.toregister_user,"123456","1234567")
        baseutils.is_text_equal_by_css(self,"Please enter the same value again.","label.error")

    def test_register_withless_length_pwd(self):
 #       baseutils.go_to_home(self)
        baseutils.go_to_signup(self)
        baseutils.register_a_user(self,config.toregister_user,"12345")
        baseutils.is_text_equal_by_css(self,"Please enter at least 6 characters.","label.error")

    def test_register_restricted_email(self):
#        baseutils.go_to_home(self)
        baseutils.go_to_signup(self)
        baseutils.register_a_user(self,config.restricted_user,config.password,config.password,True)
        baseutils.assert_contain_text_by_xpath(self,"We can not accept emails from the following top level domains: .ir, .cu, .kp, .sd, .sy",".//*[@id='new-user']/div[1]/div")


    def test_register_without_pwd(self):
#        baseutils.go_to_home(self)
        baseutils.go_to_signup(self)
        baseutils.register_a_user(self,config.toregister_user,"")
        baseutils.is_text_equal_by_css(self,"This field is required.","#web_user_password_confirmation_input > label.error")


    def test_register_without_email(self):
  #      baseutils.go_to_home(self)
        baseutils.go_to_signup(self)
        baseutils.register_a_user(self,"",config.password)
        baseutils.is_text_equal_by_css(self,"This field is required.","label.error")

    def test_register_without_captcha(self):
 #       baseutils.go_to_home(self)
        baseutils.go_to_signup(self)
        baseutils.register_a_user(self,config.toregister_user,config.password)
        baseutils.is_text_equal_by_css(self,"Captcha text didn't match","div.message.error > div")

    def test_register_invalid_email(self):
#        baseutils.go_to_home(self)
        baseutils.go_to_signup(self)
        baseutils.register_a_user(self,config.invalid_user,config.password)
        baseutils.is_text_equal_by_xpath(self,"Please enter a valid email address.","//li[@id='web_user_email_address_input']/label[2]")

        
    
    def tearDown(self):
        self.driver.quit()
        if len(self.verificationErrors)==1:
           self.assertEqual([''], self.verificationErrors)
        else:self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
    #HTMLTestRunner.main()
