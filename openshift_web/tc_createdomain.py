from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
import baseutils
import config
import random
import HTMLTestRunner


class CreateDomain(unittest.TestCase):
    def setUp(self):
        self.driver = ""
        self.base_url = ""
        self.profile = ""
        self.verificationErrors = []
        baseutils.initiate(self)
        self.domain=self.generate_domain_name()
        self.sshkey=self.ssh_key("id_rsa.pub")
        
    def generate_domain_name(self):
        i=random.uniform(1,10)
        domain_name="test"+str(i)[2:10]
        return domain_name

    def ssh_key(self,ssh_key_file):
        f = open(ssh_key_file, 'rb')
        ssh=f.read()
       # print ssh
        return ssh

  

    def create_domain(self,domain_name,ssh):
#        baseutils.go_to_home(self)
        baseutils.go_to_express(self)
        baseutils.go_to_signin(self)
        baseutils.login(self,config.new_user,config.password)
        baseutils.check_title(self,"OpenShift by Red Hat | Express")
        baseutils.go_to_express_console(self)
 #       baseutils.click_element_by_link_text(self,"Express Console")
        time.sleep(5)
        '''
        if config.proxy == 1:
            baseutils.click_element_by_link_text(self,"Looking for OpenShift Flex?")
            time.sleep(15)
            try: self.assertEqual("https://stg.openshift.redhat.com/flex/flex/index.html", self.driver.current_url())
            except AssertionError as e: self.verificationErrors.append(str(e))
            baseutils.go_back(self)
        else: baseutils.assert_element_present_by_link_text(self,"Looking for OpenShift Flex?")
        '''
        baseutils.assert_text_equal_by_css(self,"CONTROL PANEL","section.main > header > h1")
       # baseutils.assert_text_equal_by_xpath(self,"Desired domain name*","//li[@id='express_domain_namespace_input']/label")
        baseutils.wait_element_present_by_id(self,"express_domain_namespace")
        baseutils.input_by_id(self,"express_domain_namespace",domain_name)
        baseutils.input_by_id(self,"express_domain_ssh",ssh)
        self.driver.execute_script("window.scrollTo(0, 0);")
        baseutils.click_element_by_id_no_wait(self,"express_domain_submit")

    def test_a_create_domain_no_domain_name(self):
        self.create_domain("",self.sshkey)
        baseutils.assert_contain_text_by_xpath(self,"This field is required.",".//*[@id='express_domain_namespace_input']/label[2]")

        
    def test_b_create_domain_no_ssh_key(self):
        self.create_domain(self.domain,"")
        baseutils.assert_text_equal_by_css(self,"This field is required.","#express_domain_ssh_input > label.error")

    def test_c_create_domain_with_blacklist(self):
        self.create_domain("jboss",self.sshkey)
        baseutils.assert_text_equal_by_xpath(self,"Namespace jboss is not permitted","//div[@id='flash']/div/p")

    def test_d_create_domain_with_nonalpha(self):
        self.create_domain("test_55",self.sshkey)
        baseutils.assert_text_equal_by_css(self,"Only letters and numbers are allowed","label.error")

    def test_e_create_domain_with_over16charater(self):
#        baseutils.go_to_home(self)
        baseutils.go_to_express(self)
        baseutils.go_to_signin(self)
        baseutils.login(self,config.new_user,config.password)
        baseutils.check_title(self,"OpenShift by Red Hat | Express")
        baseutils.go_to_express_console(self)
#        baseutils.click_element_by_link_text(self,"Express Console")
        baseutils.assert_text_equal_by_css(self,"CONTROL PANEL","section.main > header > h1")
       # baseutils.assert_text_equal_by_xpath(self,"Desired domain name*","//li[@id='express_domain_namespace_input']/label")
        baseutils.wait_element_present_by_id(self,"express_domain_namespace")
        baseutils.input_by_id(self,"express_domain_namespace","abcdefg1234567890")
        baseutils.input_by_id(self,"express_domain_ssh",self.sshkey)
        baseutils.assert_value_equal_by_id(self,"abcdefg123456789","express_domain_namespace")

    def test_f_create_domain_with_existing_name(self):
        self.create_domain(config.exist_domain,self.sshkey)
        baseutils.assert_text_equal_by_xpath(self,"A namespace with name \'"+config.exist_domain+"\' already exists","//div[@id='flash']/div/p")

    def test_g_create_domain_normally(self):
        self.create_domain(self.domain,self.sshkey)
        baseutils.assert_text_equal_by_xpath(self,"Congratulations! You successfully created your domain","//div[@id='flash']/div/p")

    def test_h_change_domain_name(self):
 #       baseutils.go_to_home(self)
        baseutils.go_to_express(self)
        baseutils.go_to_signin(self)
        baseutils.login(self,config.new_user,config.password)
        baseutils.check_title(self,"OpenShift by Red Hat | Express")
        baseutils.go_to_express_console(self)
#        baseutils.click_element_by_link_text(self,"Express Console")
        time.sleep(2)
        baseutils.click_element_by_xpath(self,".//*[@id='domain_form_replacement']/a")
        while self.driver.current_url not in [self.base_url+"/app/dashboard",self.base_url+"/app/control_panel"]:
           baseutils.go_to_express_console(self)             
        try:
           while (not baseutils.assert_element_present_by_id("express_domain_namespace")):
               baseutils.click_element_by_xpath(self,".//*[@id='domain_form_replacement']/a")
        except:pass
        _value=self.driver.find_element_by_id("express_domain_namespace").get_attribute("value")
        _newvalue=_value[:len(_value)-1]
        baseutils.input_by_id(self,"express_domain_namespace",_newvalue)
        baseutils.click_element_by_id_no_wait(self,"express_domain_submit")
        baseutils.assert_text_equal_by_css(self,"Congratulations! You successfully updated your domain","div.message.success")
        

    def test_i_change_domain_sshkey(self):
 #       baseutils.go_to_home(self)
        baseutils.go_to_express(self)
        baseutils.go_to_signin(self)
        baseutils.login(self,config.new_user,config.password)
        baseutils.check_title(self,"OpenShift by Red Hat | Express")
        baseutils.go_to_express_console(self)
        time.sleep(2)
        baseutils.click_element_by_xpath(self,".//*[@id='domain_form_replacement']/a")
        _newssh=self.ssh_key("id2_rsa.pub")
        while self.driver.current_url not in [self.base_url+"/app/dashboard",self.base_url+"/app/control_panel"]:
           baseutils.go_to_express_console(self)  
        try:
           while (not baseutils.assert_element_present_by_id("express_domain_ssh")):
               baseutils.click_element_by_xpath(self,".//*[@id='domain_form_replacement']/a")
        except:pass
        baseutils.wait_element_present_by_id(self,"express_domain_ssh")
        baseutils.input_by_id(self,"express_domain_ssh",_newssh)
        baseutils.click_element_by_id_no_wait(self,"express_domain_submit")
        baseutils.assert_text_equal_by_css(self,"Congratulations! You successfully updated your domain","div.message.success")

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
   # HTMLTestRunner.main() 
