#!/bin/bash

python run.py --browser=ie --url=https://openshifttest.redhat.com
python tc_home.py -v
python tc_register.py RegisterPage.test_register_with_mismatch_pwd
python tc_register.py RegisterPage.test_register_withless_length_pwd
python tc_register.py RegisterPage.test_register_without_pwd
python tc_register.py RegisterPage.test_register_without_email
python tc_register.py RegisterPage.test_register_without_captcha
python tc_register.py RegisterPage.test_register_invalid_email
python tc_login.py  LoginPage.test_check_login_form
python tc_login.py  LoginPage.test_login_invalid_user
python tc_login.py  LoginPage.test_login_without_user
python tc_login.py  LoginPage.test_login_without_pwd
python tc_login.py  LoginPage.test_login_sql_bypass
python tc_partner.py -v
python tc_platformoverview.py PlatformOverview.test_check_platform_a_overview_never_signin
python tc_platformoverview.py PlatformOverview.test_check_platform_b_overview_videos_links
python tc_express.py Express.test_check_express_about
python tc_express.py Express.test_check_express_videos
python tc_express.py Express.test_check_express_navi
python tc_flex.py Flex.test_check_flex_about
python tc_flex.py Flex.test_check_flex_videos
python tc_flex.py Flex.test_check_flex_navi 
