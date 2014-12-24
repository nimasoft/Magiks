# HEADER
'''   
@file:          log_manager.py
@brief:    	    This module provides classes containing data structure for IK test log data
@author:        Nima Ramezani Taghiabadi
                PhD Researcher
                Faculty of Engineering and Information Technology
                University of Technology Sydney
                Broadway, Ultimo, NSW 2007
                Room No.: CB10.03.512
                Phone:    02 9514 4621
                Mobile:   04 5027 4611
                Email(1): Nima.RamezaniTaghiabadi@student.uts.edu.au 
                Email(2): nima.ramezani@gmail.com
                Email(3): nima_ramezani@yahoo.com
                Email(4): ramezanitn@alum.sharif.edu
@version:	    2.0
Last Revision:  16 December 2014
'''
# BODY

import math, pickle

key_dic = {
    # Forward:
    # For Eval_Log_Data_Single():
    
    'TPN'   : 'Target Pose Number',
    'S'     : 'Success',
    'NSPT'  : 'Number of Starting Point Trials',
    'NI'    : 'Number of Iterations',
    'NS'    : 'Number of Success', 
    'RT'    : 'Running Time (ms)',
    'TRT'   : 'Total Running Time (ms)',
    'ART'   : 'Average Running Time (ms)', 
    'TNI'   : 'Total Number of Iterations', 
    'ANI'   : 'Average Number of Iterations',
    'PS'    : 'Percentage of Success',  # percentage of success until now (This field exists in Eval_Log_Data_Statistics() and contains per.Suc. for all runs
    'IC'    : 'Initial Configuration',
    'FC'    : 'Final Configuration',
    'IP'    : 'Initial Pose',
    'FP'    : 'Final Pose',

    # For Eval_Log_Data_Statistics():
    'NRun'  : 'Number of Runs',
    'NSRun' : 'Number of Successful Runs',
    'NI-tot': 'Number of Iterations-Total',
    'NI-max': 'Number of Iterations-Maximum',
    'NI-min': 'Number of Iterations-Minimum',
    'NI-avr': 'Number of Iterations-Average',
    'NI-sdv': 'Number of Iterations-Standard Deviation',
    'NI-mse': 'Number of Iterations-Mean Standard Error',
    'NT-max': 'Number of Trials-Maximum',
    'NT-min': 'Number of Trials-Minimum',
    'NT-avr': 'Number of Trials-Average',
    'RT-tot': 'Running Time-Total (ms)',
    'RT-max': 'Running Time-Maximum (ms)',
    'RT-min': 'Running Time-Minimum (ms)',
    'RT-avr': 'Running Time-Average (ms)',
    'RT-sdv': 'Running Time-Standard Deviation (ms)', 
    'RT-mse': 'Running Time-Mean Standard Error',

    #Inverse:

    # For Eval_Log_Data_Single():
    'Target Pose Number'                        : 'TPN',
    'Success'                                   : 'SUC',
    'Number of Starting Point Trials'           : 'NSPT',
    'Number of Iterations'                      : 'NI',
    'Number of Success'                         : 'NS', 
    'Running Time (ms)'                         : 'RT',
    'Total Running Time (ms)'                   : 'TRT',
    'Average Running Time (ms)'                 : 'ART', 
    'Total Number of Iterations'                : 'TNI', 
    'Average Number of Iterations'              : 'ANI',
    'Percentage of Success'                     : 'PS',
    'Initial Configuration'                     : 'IC',
    'Final Configuration'                       : 'FC',
    # For Eval_Log_Data_Statistics():

    'Number of Iterations-Total'                : 'NI-tot',
    'Number of Iterations-Maximum'              : 'NI-max',
    'Number of Iterations-Minimum'              : 'NI-min',
    'Number of Iterations-Average'              : 'NI-avr',
    'Number of Iterations-Standard Deviation'   : 'NI-sdv',
    'Number of Iterations-Mean Standard Error'  : 'NI-mse',
    'Number of Trials-Maximum'                  : 'NT-max',
    'Number of Trials-Minimum'                  : 'NT-min',
    'Number of Trials-Average'                  : 'NT-avr',
    'Running Time-Total (ms)'                   : 'RT-tot',
    'Running Time-Maximum (ms)'                 : 'RT-max',
    'Running Time-Minimum (ms)'                 : 'RT-min',
    'Running Time-Average (ms)'                 : 'RT-avr',
    'Running Time-Standard Deviation (ms)'      : 'RT-sdv', 
    'Running Time-Mean Standard Error'          : 'RT-mse'
    }

class Log_Success(): 
    '''
    Contains data structure for evaluation test results for a single target pose pertaining the success 
    '''    
    
    def __init__(self, n_suc = 0, suc = False):
        # Number of successful attempts until now   
        self.num_suc_til_now     = n_suc                        
        # Boolean property indicating if the implementation was successful or not
        self.success             = suc
    
class Log_Num_Iter() : 
    '''
    Contains data structure for evaluation test results for a single target pose pertaining number of iterations
    '''    
    def __init__(self, number_of_steps = 0, n_iters_total = 0):
        # Number of iterations for this target pose
        self.num_iter            = number_of_steps              
        # Total number of iterations until now
        self.num_iter_til_now    = n_iters_total                
    
class Log_Run_Time() : 
    '''
    Contains data structure for evaluation test results for a single target pose pertaining running time
    '''    
    def __init__(self, elapsed_kinematic_inversion = 0.0, time_total = 0.0, average_step_time = 0.0):
        # Running time for this configuration
        self.run_time            = elapsed_kinematic_inversion  
        # Total running time until now
        self.run_time_til_now    = time_total                   
        # Average running time for one iteration
        self.mean_stp_time       = average_step_time            

class Eval_Log_Data_Single():
    '''
    Contains data structure for evaluation test results for a single target pose
    Including:
        Initial Status (Configuration, Endeffector Pose, Values of error functions)
        Final   Status (Configuration, Endeffector Pose, Values of error functions)
    '''    
        
    def __init__(self, cnt, num_trial = 0, log_success = Log_Success(), log_run_time = Log_Run_Time(), log_num_iter = Log_Num_Iter(), start_config_str = '', final_config_str = '', start_pose_str = '', final_pose_str = ''):
        
        # Index of target pose in the target pose workspace 
        self.target_pose_num     = cnt                          
        # Number of starting point trials for this target pose
        self.num_trial           = num_trial
        
        self.success_log         = log_success        
        self.run_time_log        = log_run_time
        self.num_iter_log        = log_num_iter
        
        self.start_config_str    = start_config_str
        self.final_config_str    = final_config_str        
        self.start_pose_str      = start_pose_str
        self.final_pose_str      = final_pose_str
        self.str_parameter_set   = ['TPN', 'S', 'NSPT', 'NI', 'RT','NS', 'TRT', 'ART', 'TNI', 'ANI','PS', 'IC', 'FC', 'IP', 'FP']
        self.csv_parameter_set   = ['TPN', 'S', 'NSPT', 'NI', 'RT','NS', 'TRT', 'ART', 'TNI', 'ANI', 'PS']

    def parameter_value(self, parameter):
        if parameter == 'TPN':
            return str(self.target_pose_num)
        elif parameter == 'S':
            return str(self.success_log.success)
        elif parameter == 'NSPT':
            return str(self.num_trial)
        elif parameter == 'NI':
            return str(self.num_iter_log.num_iter)
        elif parameter == 'RT':
            return str(1000*self.run_time_log.run_time)
        elif parameter == 'NS':
            return str(self.success_log.num_suc_til_now)
        elif parameter == 'TRT':
            return str(1000*self.run_time_log.run_time_til_now)
        elif parameter == 'ART':
            return str(1000*self.run_time_log.run_time_til_now/(self.target_pose_num + 1))
        elif parameter == 'TNI':
            return str(self.num_iter_log.num_iter_til_now)
        elif parameter == 'ANI':
            return str(self.num_iter_log.num_iter_til_now/(self.target_pose_num + 1))
        elif parameter == 'PS':
            return str(100.00*self.success_log.num_suc_til_now/(self.target_pose_num + 1))
        elif parameter == 'IC':
            return self.start_config_str
        elif parameter == 'FC':
            return self.final_config_str
        elif parameter == 'IP':
            return '\n' + '------------' + '\n' + self.start_pose_str
        elif parameter == 'FP':
            return '\n' + '------------' + '\n' + self.final_pose_str

    def __str__(self, parameter_set = None):
        if parameter_set == None:
            parameter_set = self.str_parameter_set
        s =   '\n'
        s  += 'Test Result:' + '\n\n'
        for p in parameter_set:
            value = self.parameter_value(p)
            param = key_dic[p]
            s +=  param + " "*(32-len(param)) +': ' + value + '\n'

        s += '\n' + '______________________________________________________________________________________________________________________________'
        
        return s

    def csv(self, header = True, parameter_set = None):
        if parameter_set == None:
            parameter_set = self.csv_parameter_set

        if header:
            s  = 'Parameter' + ',' + 'Value' +'\n'
        else:
            s = ''
        for p in parameter_set:
            value = self.parameter_value(p)
            s += key_dic[p] + "," + value + '\n'
        return s

    def csv_horizontal_header(self, parameter_set = None):
        if parameter_set == None:
            parameter_set = self.csv_parameter_set
        s = ''
        for p in parameter_set:
            s += key_dic[p] + ","
        s  = s[0:len(s) - 1]
        return s

    def csv_horizontal(self, parameter_set = None):
        if parameter_set == None:
            parameter_set = self.csv_parameter_set
        s = ''
        for p in parameter_set:
            s += self.parameter_value(p) + ','
        s  = s[0:len(s) - 1]

        return s

    def write_csv(self, filename):
        print 'Eval_Log_Data_Single(): Writing csv file started ...'
        CSV_FILE_HANDLE = open(filename, "w")
        CSV_FILE_HANDLE.write(self.csv())
        print 'Eval_Log_Data_Single(): Writing csv file ended.'
        
class Eval_Log_Data_Statistics():
    '''
    Contains structure for statistical data of evaluation test results for a set of target poses
    Including:
        Initial Status (Configuration, Endeffector Pose, Values of error functions)
        Final   Status (Configuration, Endeffector Pose, Values of error functions)
            
    '''    
    def __init__(self):
        
        self.num_success                = 0
        self.num_run                    = 0

        self.sum_num_iter               = 0              # Total number of iterations for all target poses
        self.max_num_iter               = 0              # Maximum number of iterations
        self.max_num_iter_pose_number   = 0              # Pose number corresponding to maximum number of iterations
        self.min_num_iter               = 1000000        # Minimum number of iterations
        self.min_num_iter_pose_number   = 0              # Pose number corresponding to minimum number of iterations
        
        self.sum_num_trial              = 0              # Total number of trials for all target poses
        self.max_num_trial              = 0              # Maximum number of trials
        self.max_num_trial_pose_number  = 0              # Pose number corresponding to maximum number of trials
        self.min_num_trial              = 1000000        # Minimum number of trials
        self.min_num_trial_pose_number  = 0              # Pose number corresponding to minimum number of trials
        
        self.max_run_time               = 0.0
        self.max_run_time_pose_number   = 0              # Pose number corresponding to maximum running time
        self.min_run_time               = 1000000.00
        self.min_run_time_pose_number   = 0              # Pose number corresponding to minimum running time
        self.sum_run_time               = 0.0
        
        self.mean_num_iter              = 0.0
        self.mean_num_trial             = 0.0
        self.mean_run_time              = 0.0
        self.mean_stp_time              = 0.0
        self.sd_num_iter                = 0.0
        self.sd_run_time                = 0.0
        self.mse_num_iter               = 0.0
        self.mse_run_time               = 0.0
        
        self.str_parameter_set = ['NRun','NSRun','PS','NI-tot', 'NI-max', 'NI-min', 'NI-avr','NI-sdv','NI-mse', 
                                  'NT-max', 'NT-min','NT-avr', 'RT-tot', 'RT-max', 'RT-min', 'RT-avr', 'RT-mse']
        self.csv_parameter_set = ['PS', 'NI-avr','NI-mse', 'RT-max', 'RT-min', 'RT-avr', 'RT-mse']

    def parameter_value(self, parameter):
        if parameter == 'NRun':
            return str(self.num_run)
        elif parameter == 'NSRun':
            return str(self.num_success)
        elif parameter == 'PS':
            return str(100*self.num_success/float(self.num_run))
        elif parameter == 'NI-tot':
            return str(self.sum_num_iter)
        elif parameter == 'NI-max':
            # return str(self.max_num_iter) + " for target pose number: " + str(self.max_num_iter_pose_number)
            return str(self.max_num_iter)
        elif parameter == 'NI-min':
            # return str(self.min_num_iter) + " for target pose number: " + str(self.min_num_iter_pose_number)
            return str(self.min_num_iter)
        elif parameter == 'NI-avr':
            return str(self.mean_num_iter)
        elif parameter == 'NI-sdv':
            return str(self.sd_num_iter)
        elif parameter == 'NI-mse':
            return str(self.mse_num_iter)
        elif parameter == 'NT-max':
            # return str(self.max_num_trial) + ' for target pose number: ' + str(self.max_num_trial_pose_number)
            return str(self.max_num_trial)
        elif parameter == 'NT-min':
            # return str(self.min_num_trial) + ' for target pose number: ' + str(self.min_num_trial_pose_number)
            return str(self.min_num_trial)
        elif parameter == 'NT-avr':
            return str(self.mean_num_trial)
        elif parameter == 'RT-tot':
            return str(1000*self.sum_run_time)
        elif parameter == 'RT-max':
            # return str(1000*self.max_run_time)+ ' for target pose number: ' + str(self.max_run_time_pose_number) 
            return str(1000*self.max_run_time)
        elif parameter == 'RT-min':
            # return str(1000*self.min_run_time)+ ' for target pose number: ' + str(self.min_run_time_pose_number)
            return str(1000*self.min_run_time)
        elif parameter == 'RT-avr':
            return str(1000*self.mean_run_time)
        elif parameter == 'RT-sdv':
            return str(1000*self.sd_run_time)
        elif parameter == 'RT-mse':
            return str(1000*self.mse_run_time)
        else:
            assert False, "Error from Eval_Log_Data_Statistics().parameter_value(): " + parameter + " is unknown"

    def __str__(self, parameter_set = None):
        if parameter_set == None:
            parameter_set = self.str_parameter_set
        s =   '\n'
        s  += 'Test Statistics:' + '\n\n'
        for p in parameter_set:
            value = self.parameter_value(p)
            param = key_dic[p]
            s +=  param + " "*(40-len(param)) +': ' + value + '\n'

        s += '\n' + '______________________________________________________________________________________________________________________________'
        
        return s

    def csv(self, header = True, parameter_set = None):
        if parameter_set == None:
            parameter_set = self.csv_parameter_set
        if header:
            s  = 'Parameter' + ',' + 'Value' +'\n'
        else:
            s = ''
        for p in parameter_set:
            value = self.parameter_value(p)
            s += key_dic[p] + "," + value + '\n'
        return s

    def csv_horizontal_header(self, parameter_set = None):
        if parameter_set == None:
            parameter_set = self.csv_parameter_set
        s = ''
        for p in parameter_set:
            s += key_dic[p] + ","
        s  = s[0:len(s) - 1]
        return s

    def csv_horizontal(self, parameter_set = None):
        if parameter_set == None:
            parameter_set = self.csv_parameter_set
        s = ''
        for p in parameter_set:
            s += self.parameter_value(p) + ','
        s  = s[0:len(s) - 1]
        return s

    def write_csv(self, filename):
        print 'Eval_Log_Data_Statistics(): Writing csv file started ...'
        CSV_FILE_HANDLE = open(filename, "w")
        CSV_FILE_HANDLE.write(self.csv())
        print 'Eval_Log_Data_Statistics(): Writing csv file ended.'
        
    def calculate_statistics(self, body):   

        self.__init__()
        sum_stp_time = 0.0
        
        self.num_run = len(body)

        for i in range(0, self.num_run):
            
            self.sum_num_iter   += body[i].num_iter_log.num_iter
            self.sum_num_trial  += body[i].num_trial
            self.sum_run_time   += body[i].run_time_log.run_time
            sum_stp_time        += body[i].run_time_log.mean_stp_time
            
            if body[i].num_iter_log.num_iter > self.max_num_iter:
                self.max_num_iter = body[i].num_iter_log.num_iter
                self.max_num_iter_pose_number = i
            if body[i].num_iter_log.num_iter < self.min_num_iter:
                self.min_num_iter = body[i].num_iter_log.num_iter
                self.min_num_iter_pose_number = i

            if body[i].num_trial > self.max_num_trial:
                self.max_num_trial = body[i].num_trial
                self.max_num_trial_pose_number = i
            if body[i].num_trial < self.min_num_trial:
                self.min_num_trial = body[i].num_trial
                self.min_num_trial_pose_number = i

            if body[i].run_time_log.run_time > self.max_run_time:
                self.max_run_time = body[i].run_time_log.run_time
                self.max_run_time_pose_number = i
            if body[i].run_time_log.run_time < self.min_run_time:
                self.min_run_time = body[i].run_time_log.run_time
                self.min_run_time_pose_number = i

        assert self.sum_run_time == body[self.num_run - 1].run_time_log.run_time_til_now
        assert self.sum_num_iter == body[self.num_run - 1].num_iter_log.num_iter_til_now
    
        self.mean_num_iter  = float(self.sum_num_iter) / self.num_run
        self.mean_num_trial = float(self.sum_num_trial) / self.num_run
        self.mean_run_time  = self.sum_run_time / self.num_run
        self.mean_stp_time  = sum_stp_time / self.num_run

        sum_var_num_iter  = 0
        sum_var_run_time  = 0
    
        for i in range(0, self.num_run):
            
            sum_var_num_iter += (float(body[i].num_iter_log.num_iter) - self.mean_num_iter) ** 2
            sum_var_run_time += (      body[i].run_time_log.run_time  - self.mean_run_time) ** 2
        
        if self.num_run > 1:
            den = self.num_run - 1
        else:
            den = 1

        var_num_iter = sum_var_num_iter / den
        var_run_time = sum_var_run_time / den
        
        self.sd_num_iter   = math.sqrt(var_num_iter)
        self.sd_run_time   = math.sqrt(var_run_time)
        self.mse_num_iter  = self.sd_num_iter / math.sqrt(den)
        self.mse_run_time  = self.sd_run_time / math.sqrt(den)

        self.num_success  = body[self.num_run - 1].success_log.num_suc_til_now
        
class Eval_Log_Data_Multiple():
    '''
    Contains data structure for evaluation test results for multiple target poses (
    Including:
        Header:
            Test Settings (An instance of "Kinematic_Manager_Settings")
        Body:
            Log data for each configuration (A list of instances of "Eval_Log_Data_Single")
        Footer
            Statistic Data (An instance of "Eval_Log_Data_Statistics")
            
    '''    
    def __init__(self, km_settings ):
        self.header = km_settings
        self.body   = [] # should be an array of instances of Eval_Log_Data_Single()
        self.footer = Eval_Log_Data_Statistics()

    def write_log(self, filename):
        print 'Eval_Log_Data_Multiple(): Writing log file started ...'
        LOG_FILE_HANDLE = open(filename, "w")
        LOG_FILE_HANDLE.write(str(self.header))
        LOG_FILE_HANDLE.write("\n" + "--------------------------------------------------------------------------------" + "\n")
        for body_log in self.body:
            LOG_FILE_HANDLE.write(str(body_log))
        LOG_FILE_HANDLE.write("\n" + "--------------------------------------------------------------------------------" + "\n")
        LOG_FILE_HANDLE.write(str(self.footer))
        print 'Eval_Log_Data_Multiple(): Writing log file ended.'

    def write_self(self, filename):
        print 'Eval_Log_Data_Multiple(): Writing self file started ...'
        SELF_FILE_HANDLE = open(filename, "w")
        pickle.dump(self, SELF_FILE_HANDLE)
        print 'Eval_Log_Data_Multiple(): Writing self file ended.'

    def write_csv(self, filename):
        print 'Eval_Log_Data_Multiple(): Writing csv file started ...'
        CSV_FILE_HANDLE = open(filename, "w")
        x = self.body[0]
        CSV_FILE_HANDLE.write(x.csv_horizontal_header() + '\n')
        for x in self.body:
            CSV_FILE_HANDLE.write(x.csv_horizontal() + '\n')
        print 'Eval_Log_Data_Multiple(): Writing csv file ended.'

