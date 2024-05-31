import unittest, time, re
import tc_home,tc_register,tc_confirm_email
import tc_login,tc_express,tc_flex
import tc_createdomain
import tc_createapp,tc_passwordmanage
import tc_platformoverview,tc_userlanding,tc_partner
import baseutils
import config
import HTMLTestRunner
import sys
import re
from optparse import OptionParser 
import commands
import subprocess


def fullsuite():
    full_suite=unittest.TestSuite()
    home_suite=unittest.TestSuite()
    register_suite=unittest.TestSuite()
    confirm_suite=unittest.TestSuite()
    login_suite=unittest.TestSuite()
    partner_suite=unittest.TestSuite()
    userlanding_suite=unittest.TestSuite()
    express_suite=unittest.TestSuite()
    flex_suite=unittest.TestSuite()
    platform_suite=unittest.TestSuite()
    password_manage_suite=unittest.TestSuite()
    home_suite=unittest.TestLoader().loadTestsFromTestCase(tc_home.HomePage)
    register_suite=unittest.TestLoader().loadTestsFromTestCase(tc_register.RegisterPage)
    confirm_suite=unittest.TestLoader().loadTestsFromTestCase(tc_confirm_email.EmailConfirm)
    login_suite=unittest.TestLoader().loadTestsFromTestCase(tc_login.LoginPage)
    platform_suite=unittest.TestLoader().loadTestsFromTestCase(tc_platformoverview.PlatformOverview)
    userlanding_suite=unittest.TestLoader().loadTestsFromTestCase(tc_userlanding.UserLanding)
    password_manage_suite=unittest.TestLoader().loadTestsFromTestCase(tc_passwordmanage.ManagePassword)
    express_suite=unittest.TestLoader().loadTestsFromTestCase(tc_express.Express)
    flex_suite=unittest.TestLoader().loadTestsFromTestCase(tc_flex.Flex)
    createdomain_suite=unittest.TestLoader().loadTestsFromTestCase(tc_createdomain.CreateDomain)
    createapp_suite=unittest.TestLoader().loadTestsFromTestCase(tc_createapp.CreateApplication)
    partner_suite=unittest.TestLoader().loadTestsFromTestCase(tc_partner.Partner)
    full_suite= unittest.TestSuite([home_suite,register_suite,confirm_suite,login_suite,partner_suite,platform_suite,express_suite,flex_suite,password_manage_suite,createdomain_suite,createapp_suite])
    return full_suite


if __name__ == "__main__":
    i=random.uniform(1,10)
    generate_new_user="libra-test+stage"+str(i)[3:10]+"@redhat.com"
    baseutils.update_config_file('environment','new_user',generate_new_user)
    if len(sys.argv) < 2:
        print """usage: --url=<url>  --browser=<browser> --new_user=<new_user>  --resultfile=<resultfilename> --title=<title> --description=<decription>  --all=<all>"""
        sys.exit(1)
    else:
        parser = OptionParser()
        parser.add_option("--url", dest="url",default="https://openshifttest.redhat.com",
                   help="url link")
        parser.add_option("--browser", dest="browser",default="firefox",
                   help="browser name")
        parser.add_option("--browserpath", dest="browserpath",default=0,
                   help="browser path")
        parser.add_option("--proxy", dest="proxy",default=False,
                   help="True or False")
        parser.add_option("--new_user", dest="new_user",
                   help="new user")
        parser.add_option("--resultfile", dest="resultfile",default="OpenShift.WebTestResult.html",
                   help="result file name")
        parser.add_option("--title", dest="title",default="OpenShift Web Test Report",
                   help="result file title")
        parser.add_option("--description", dest="description",default="This is OpenShift Web Test Result",
                   help="result file description")
        parser.add_option("--all", dest="all",default=False,
                   help="true or false")
        (options, args) = parser.parse_args()
        if options.url != None: baseutils.update_config_file('environment','url', options.url)
        if options.browser != None:baseutils.update_config_file('environment','browser', options.browser)
        if options.browserpath != None:baseutils.update_config_file('environment','browserpath',options.browserpath)
        if options.proxy != None: baseutils.update_config_file('environment', 'proxy', options.proxy)
        if options.new_user != None:baseutils.update_config_file('environment','new_user',options.new_user)
        if config.proxy:baseutils.update_config_file('environment','libra_server',"stg.rhcloud.com")
        else:baseutils.update_config_file('environment','libra_server',"dev.rhcloud.com")
        if options.resultfile != None: baseutils.update_config_file('output','resultfile',options.resultfile)
        if options.title != None:baseutils.update_config_file('output','title',options.title)
        if options.description != None:baseutils.update_config_file('output','description',options.description)
        if options.all:
            fp =file(config.resultfile,'wb')
            runner = HTMLTestRunner.HTMLTestRunner(stream=fp,verbosity=2,title=config.title,description=config.description)
            ret=runner.run(fullsuite())
            sys.exit(ret)
        
    

    
     


