'''
@author: c_caijie
'''

import fs_wrapper
import settings.common as SC
from case_utility import *
from logging_wrapper import log_test_case, save_fail_log, print_report_line
from test_case_base import TestCaseBase
from qrd_shared.case import *
from qrd_shared.mms.Mms import *



class test_suit_stress_test_camera1_case000016(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    "Procedure:
    Step1:Launch Camera;
    Step2:take snapshot for 200;
    Step3: tap thumbnail, and delete the snapshot by Tapping 'delete' icon;
    Verification: 
    ER3:delete successfully and no exception.    
    '''
    
    
    def test_case_main(self, case_results):
        
        
        global case_flag , TAG, testresult, success_flag, i, success_time
        case_flag = False
        testresult = []
        success_time = 0
        fail_time = 0
        iterationNum = 200
        TAG = "Dev-ci cases: Camera "
        log_test_framework(TAG, self.name+" -Start")
        
        """
        
        cases contents you need to add
        
        
        """
        if search_text("Close app", searchFlag=TEXT_CONTAINS):
            click_button_by_text("Close app", searchFlag=TEXT_CONTAINS)
            sleep(2) 
                    
        start_activity('org.codeaurora.snapcam','com.android.camera.CameraLauncher')
        if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 10):
            click_button_by_id('permission_allow_button')
        if wait_for_fun(lambda:search_text('OK'), True, 5):            
            click_textview_by_text('OK')
        if wait_for_fun(lambda:search_view_by_id('shutter_button'), True, 5):
            log_test_framework("step1:", "Launch camera pass")           
            for i in range(iterationNum):
                print_log_line('take snapshot iteration %d'%(i+1))
                camera.take_picture()
                if wait_for_fun(lambda:search_view_by_id('shutter_button'), True, 5):
                    log_test_framework("step2:", "take snapshot pass")
                else:
                    if search_text("Close app", searchFlag=TEXT_CONTAINS):
                        print_log(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], '%d.Popup Close app when take snapshot'%(i+1))
                        click_button_by_text("Close app", searchFlag=TEXT_CONTAINS)
                        sleep(2)
                        start_activity('org.codeaurora.snapcam','com.android.camera.CameraLauncher')                                                                
            if wait_for_fun(lambda:search_view_by_id('preview_thumb'), True, 5):
                click_imageview_by_id("preview_thumb")
                for i in range(iterationNum):
                    success_flag = False
                    print_log_line('This is iteration %d'%(i+1))
                    if wait_for_fun(lambda:search_view_by_id("photopage_bottom_control_delete"), True, 5):
                        click_imageview_by_id("photopage_bottom_control_delete")
                        if wait_for_fun(lambda:search_text("OK"), True, 5):
                            click_button_by_text("OK")
                            sleep(10)
                            log_test_framework("step3:", "tap thumbnail and delete the snapshot by Tapping delete icon pass")
                            success_flag = True
                            click(651, 792)                            
                    if success_flag == True:
                        testresult.append('%d.Pass'%(i+1))
                        success_time=success_time+1
                        print_log(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], '%d.Pass'%(i+1))
                    else:
                        testresult.append('%d.Fail'%(i+1))
                        take_screenshot()
                        fail_time=fail_time+1
                        print_log(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], '%d.Fail'%(i+1))
                        if search_text("Close app", searchFlag=TEXT_CONTAINS):
                            print_log(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], '%d.Popup Close app when delete snapshot'%(i+1))
                            click_button_by_text("Close app", searchFlag=TEXT_CONTAINS)
                            sleep(2)
                        start_activity('org.codeaurora.snapcam','com.android.camera.CameraLauncher')                        
                        if wait_for_fun(lambda:search_view_by_id('preview_thumb'), True, 5):
                            click_imageview_by_id("preview_thumb")                       
                if success_time == iterationNum:
                    case_flag = True        
        if search_text("isn't responding", searchFlag=TEXT_CONTAINS):
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs ANR")            
            take_screenshot()
            if search_text("Close app", searchFlag=TEXT_CONTAINS):
                click_button_by_text("Close app", searchFlag=TEXT_CONTAINS)
                sleep(2)
            if search_text("Close", searchFlag=TEXT_CONTAINS):
                click_button_by_text("Close")
                sleep(2)            
        elif search_text("Unfortunately", searchFlag=TEXT_CONTAINS):
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs crash")
            take_screenshot()
            if search_text("OK", searchFlag=TEXT_CONTAINS):
                click_button_by_text("OK")
                sleep(2)
            if search_text("Close", searchFlag=TEXT_CONTAINS):
                click_button_by_text("Close")
                sleep(2)            
        elif search_text("stopped", searchFlag=TEXT_CONTAINS):
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Popup has stopped")
            take_screenshot()
            if search_text("Close", searchFlag=TEXT_CONTAINS):
                click_button_by_text("Close")
                sleep(2)            
            if search_text("OK", searchFlag=TEXT_CONTAINS):
                click_button_by_text("OK")
                sleep(2)       
        elif search_text("Close app", searchFlag=TEXT_CONTAINS):
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Popup Close app error")
            take_screenshot()            
            click_button_by_text("Close app", searchFlag=TEXT_CONTAINS)
            sleep(2)
        send_key(KEY_BACK)
        sleep(1)
        send_key(KEY_BACK)
        sleep(1)
        send_key(KEY_HOME)
        sleep(1)
        print_log(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], 'success:%d fail:%d iteration:%d'%(success_time,fail_time,iterationNum))
        print_log(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], testresult)         
        if case_flag:
            qsst_log_case_status(STATUS_SUCCESS, "" , SEVERITY_HIGH)
        else:
            qsst_log_case_status(STATUS_FAILED, "", SEVERITY_HIGH)
        
        case_results.append((self.case_config_map[fs_wrapper.CASE_NAME_ATTR], case_flag))
        
        
    def test_case_end(self):
        '''
        record the case result

        '''
        log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], TAG + ' : end')
        if can_continue() and case_flag == True:
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], TAG + ' : case pass')
            print_report_line(self.case_config_map[fs_wrapper.CASE_NAME_ATTR] + TAG + ' : \tpass')
        else:
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], TAG + ' : case fail')
            print_report_line(self.case_config_map[fs_wrapper.CASE_NAME_ATTR] + TAG + ' : \tfail')
        save_fail_log()
            
