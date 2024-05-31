from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
import baseutils
import config
import random
import HTMLTestRunner


class CreateApplication(unittest.TestCase):
    def setUp(self):
        self.driver = ""
        self.base_url = ""
        self.profile = ""
        self.verificationErrors = []
        self.exist_app="mypythonapp1"
        baseutils.initiate(self)



    def get_domain_name(self):
        return self.driver.find_element_by_id("show_namespace").text

    def generate_app_name(self):
        i=random.uniform(1,10)
        app_name="app"+str(i)[5:10]
        return app_name

    def get_cartridge_list(self,id_name="express_app_cartridge"):
        select=self.driver.find_element_by_id(id_name)
        options = select.find_elements_by_tag_name("option")
        return options

    def assert_app_url(self,appname):
        _domain_name=self.get_domain_name()
        _app_url="http://"+appname+"-"+_domain_name+"."+config.libra_server
        baseutils.assert_text_equal_by_partial_link_text(self,_app_url,"http://"+appname+"-")


    def create_application(self,app_name,cartridge_type):
        baseutils.go_to_express_console(self)
        baseutils.login(self,config.new_user,config.password)
        #VerifyDomainExist
        time.sleep(5)
        baseutils.assert_element_present_by_id(self,"show_namespace")
       # self.driver.refresh()
      #  self.driver.refresh()
        baseutils.wait_element_present_by_id(self,"express_app_app_name")
        self.driver.find_element_by_id("express_app_app_name").clear()
        self.driver.find_element_by_id("express_app_app_name").send_keys(app_name)
        cartridges=self.get_cartridge_list()
        self.assertTrue(len(cartridges) >= 5)
        for car in cartridges:
            if car.text == cartridge_type or car.text.find(cartridge_type) != -1:
               car.click()
               break
        self.driver.find_element_by_id("express_app_submit").click()
      #  time.sleep(2)
    
    def test_create_app_with_blank_appname(self):
        self.create_application("","jbossas")
        time.sleep(2)
        baseutils.assert_contain_text_by_xpath(self,"This field is required.","//li[@id='express_app_app_name_input']/label[2]")

        #baseutils.assert_text_equal_by_css(self,"App name is invalid; App name can't be blank","div.message.error")

    def test_create_app_with_nonalphnum_appname(self):
        self.create_application("app_1","jbossas")
        time.sleep(2)
        baseutils.assert_text_equal_by_xpath(self,"Only letters and numbers are allowed",".//*[@id='express_domain_namespace_input']/label[2]")

    def test_create_app_with_blank_cart(self):
        self.create_application("myapp","")
        time.sleep(2)
        baseutils.assert_contain_text_by_xpath(self,"This field is required.","//li[@id='express_app_cartridge_input']/label[2]")


    def test_create_app_with_blacklist_appname(self):
        self.create_application("openshift","perl")
        time.sleep(2)
        baseutils.assert_text_equal_by_css(self,"App name openshift is not a permitted app name","div.message.error")

    def test_create_app_with_blankapp_blankcart(self):
        self.create_application("","")
        time.sleep(2)
        baseutils.assert_contain_text_by_xpath(self,"This field is required.","//li[@id='express_app_app_name_input']/label[2]")
        baseutils.assert_contain_text_by_xpath(self,"This field is required.","//li[@id='express_app_cartridge_input']/label[2]")

        #baseutils.assert_text_equal_by_css(self,"App name is invalid; App name can't be blank; Cartridge can't be blank; Cartridge is not a valid cartridge.","div.message.error")        
    
    def test_create_jboss_app(self):
        _appname=self.generate_app_name()
        self.create_application(_appname,"jboss")
        baseutils.is_element_displayed(self,By.ID,"spinner")
        baseutils.assert_text_equal_by_id(self,"Creating your app...","spinner-text")
        time.sleep(5)
        if self.driver.find_element_by_css_selector("div.message.error").is_displayed():
            self.driver.refresh()
        else:
            baseutils.assert_contain_text_by_id(self,"using Java with JBossAS 7 on OpenShift:","spinner-text")
            baseutils.click_element_by_css_no_wait(self,"a.close > img")
        self.assert_app_url(_appname)
       # if baseutils.is_text_displayed (self,"We're sorry, this operation has timed out. It is possible that it was succfully completed, but we are unable to verify it.","div.message.error"):
        #    pass
       # else:
       # baseutils.assert_contain_text_by_id(self,"using Java with JBossAS 7 on OpenShift:","spinner-text")
       # baseutils.click_element_by_css_no_wait(self,"a.close > img")
       # baseutils.wait_element_not_displayed_by_id(self,"spinner")
       # self.assert_app_url(_appname)


    def test_create_perl_app(self):
        _appname=self.generate_app_name()
        self.create_application(_appname,"perl")
        baseutils.is_element_displayed(self,By.ID,"spinner")
        baseutils.assert_text_equal_by_id(self,"Creating your app...","spinner-text")
        time.sleep(5)
        #if baseutils.is_text_displayed (self,"We're sorry, this operation has timed out. It is possible that it was succfully completed, but we are unable to verify it.","div.message.error"):
        #    pass
        #else:
        baseutils.assert_contain_text_by_id(self,"OpenShift Perl app","spinner-text")
        baseutils.click_element_by_css_no_wait(self,"a.close > img")
        #baseutils.wait_element_not_displayed_by_id(self,"spinner")
        self.assert_app_url(_appname)

    def test_create_ruby_app(self):
        _appname=self.generate_app_name()
        self.create_application(_appname,"rack")
        baseutils.is_element_displayed(self,By.ID,"spinner")
        baseutils.assert_text_equal_by_id(self,"Creating your app...","spinner-text")
        time.sleep(5)
        if self.driver.find_element_by_css_selector("div.message.error").is_displayed():
            self.driver.refresh()
        else:
            baseutils.assert_contain_text_by_id(self,"popular Ruby frameworks on OpenShift","spinner-text")
            baseutils.click_element_by_css_no_wait(self,"a.close > img") 
        #if baseutils.is_text_displayed (self,"We're sorry, this operation has timed out. It is possible that it was succfully completed, but we are unable to verify it.","div.message.error"):
        #    pass
        #else:
        #baseutils.assert_contain_text_by_id(self,"popular Ruby frameworks on OpenShift","spinner-text")
        #baseutils.click_element_by_css_no_wait(self,"a.close > img")
        #baseutils.wait_element_not_displayed_by_id(self,"spinner")
        self.assert_app_url(_appname)
    

    def test_create_apython_app(self):
        #_appname=self.generate_app_name()
       # self.exist_app=_appname
        self.create_application(self.exist_app,"wsgi")
        baseutils.is_element_displayed(self,By.ID,"spinner")
        baseutils.assert_text_equal_by_id(self,"Creating your app...","spinner-text")
        time.sleep(5)
        #if baseutils.is_text_displayed (self,"We're sorry, this operation has timed out. It is possible that it was succfully completed, but we are unable to verify it.","div.message.error"):
        #    pass
        #else:
        baseutils.assert_contain_text_by_id(self,"deploy popular python frameworks","spinner-text")
        baseutils.click_element_by_css_no_wait(self,"a.close > img")
        #baseutils.wait_element_not_displayed_by_id(self,"spinner")
        self.assert_app_url(self.exist_app)
        

    def test_create_php_app(self):
        _appname=self.generate_app_name()
        self.create_application(_appname,"php")
        baseutils.is_element_displayed(self,By.ID,"spinner")
        baseutils.assert_text_equal_by_id(self,"Creating your app...","spinner-text")
        time.sleep(5)
        #if baseutils.is_text_displayed (self,"We're sorry, this operation has timed out. It is possible that it was succfully completed, but we are unable to verify it.","div.message.error"):
        #    pass
        #else:
        baseutils.assert_contain_text_by_id(self,"OpenShift PHP app","spinner-text")
        baseutils.click_element_by_css_no_wait(self,"a.close > img")
        #baseutils.wait_element_not_displayed_by_id(self,"spinner")
        self.assert_app_url(_appname)


    def test_z_check_url_after_changedomain(self):
        baseutils.go_to_express_console(self)
        baseutils.login(self,config.new_user,config.password)
        baseutils.click_element_by_xpath(self,"//*[@id='domain_form_replacement']/a")
        baseutils.wait_element_present_by_id(self,"express_domain_namespace")
        _value=self.driver.find_element_by_id("express_domain_namespace").get_attribute("value")
        _newvalue=_value[:len(_value)-1]
        baseutils.input_by_id(self,"express_domain_namespace",_newvalue)
        baseutils.click_element_by_id_no_wait(self,"express_domain_submit")
        time.sleep(5)
#        baseutils.click_element_by_css_no_wait(self,"a.close > img")
        #baseutils.wait_element_not_displayed_by_id(self,"spinner")
        baseutils.assert_text_equal_by_css(self,"Congratulations! You successfully updated your domain","div.message.success")
        self.assert_app_url(self.exist_app)


    def test_create_bsame_appname_w_exist(self):
       # _appname=self.generate_app_name()
        self.create_application(self.exist_app,"php")
        _domain=self.get_domain_name()
        _error="An application named \'"+self.exist_app+"\' in namespace \'"+_domain+"\' already exists"
        baseutils.assert_text_equal_by_css(self,_error,"div.message.error")


    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
    #HTMLTestRunner.main()