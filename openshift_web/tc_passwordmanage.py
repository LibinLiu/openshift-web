from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
import baseutils
import config
import HTMLTestRunner

class ManagePassword(unittest.TestCase):

    def setUp(self):
        self.driver = ""
        self.base_url = ""
        self.profile = ""
        self.verificationErrors = []
        baseutils.initiate(self)

    def test_reset_pwd_with_blank_email(self):
        baseutils.reset_password(self,"")
        baseutils.assert_text_equal_by_css(self,"This field is required.","label.error")
        

   
    def test_reset_pwd_with_invalid_email(self):
        baseutils.reset_password(self,"1234567")
        baseutils.assert_text_equal_by_css(self,"Please enter a valid email address.","label.error")



    def test_reset_pwd_with_existing_account(self):
        baseutils.reset_password(self,"xtian+test94@redhat.com")
        baseutils.assert_text_equal_by_css(self,"The information you have requested has been emailed to you at xtian+test94@redhat.com.","div.message.success")


    def test_reset_pwd_with_non_existing_account(self):
        baseutils.reset_password(self,"xtian+94test@redhat.com")
        baseutils.assert_text_equal_by_css(self,"The information you have requested has been emailed to you at xtian+94test@redhat.com.","div.message.success")

    
    def test_change_pwd_w_incorrect_oldpwd(self):
        baseutils.change_password(self,config.tochangepwduser[0],"654321",config.tochangepwduser[2],config.tochangepwduser[2])
        baseutils.assert_text_equal_by_css(self,"Your old password was incorrect","div.message.error")

    def test_change_pwd_w_invalid_newpwd(self):
        baseutils.change_password(self,config.tochangepwduser[0],config.tochangepwduser[1],"12345","12345")
        baseutils.assert_text_equal_by_css(self,"Please enter at least 6 characters.","fieldset.confirm > label.error")

    def test_change_pwd_w_mismatch_newpwd(self):
        baseutils.change_password(self,config.tochangepwduser[0],config.tochangepwduser[1],"123456","1234567")
        baseutils.assert_text_equal_by_css(self,"Please enter the same value again.","fieldset.confirm > label.error")


    def test_change_pwd_w_blank_oldpwd(self):
        baseutils.change_password(self,config.tochangepwduser[0],"","123456","123456")
        baseutils.assert_text_equal_by_css(self,"This field is required.","fieldset.confirm > label.error")

    def test_change_pwd_normally(self):
        baseutils.change_password(self,config.tochangepwduser[0],config.tochangepwduser[1],config.tochangepwduser[2],config.tochangepwduser[2])
        baseutils.assert_text_equal_by_css(self,"Your password has been successfully changed","div.message.success")
      
    def test_z_login_with_changed_pwd(self):
        baseutils.go_to_home(self)
        baseutils.go_to_signin(self)
        baseutils.login(self,config.tochangepwduser[0],config.tochangepwduser[2])
        time.sleep(5)
        baseutils.check_title(self,"OpenShift by Red Hat | Cloud Platform")
        baseutils.assert_element_present_by_link_text(self,"Sign out") 
        _greetings=baseutils.generate_greetings(config.tochangepwduser[0])
        baseutils.assert_element_present_by_link_text(self,_greetings)
    
    def tearDown(self):
        self.driver.quit()
        if len(self.verificationErrors)==1:
           self.assertEqual([''], self.verificationErrors)
        else:self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()