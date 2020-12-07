import pandas as pd
from os import listdir
from os.path import isfile, join
import time
from multiprocessing import Pool, TimeoutError
import numpy as np

from algorithms.branch_and_bound import *
from algorithms.dynamic_programming import *
from algorithms.ed_dp_2_mat import *
from algorithms.ed_greedy import *
from algorithms.edit_distance_dp_dnc_lin_space import *
from algorithms.pure_recursion import *


def meassure_single_call(function, args):
    
    start_time = time.time()
    start_clock = time.clock()
        
    results = function(*args)
    
    end_clock = time.clock()
    end_time = time.time()
    
    duration_time = end_time - start_time
    duration_clock = end_clock - start_clock
    
    return results, duration_time, duration_clock

def meassure_single_call_timeout(function, args, timeout_time, pool, timeout_value=-1):
    try:
        res = pool.apply_async(meassure_single_call, args=(function, args))
        return res.get(timeout=timeout_time)
    except TimeoutError:
        return (timeout_value,timeout_time,timeout_time)



if __name__ == '__main__':

    #5 sec of timeout
    timeout_time = 30

    try:
        datasets_path = sys.argv[1]
    except:
        datasets_path = 'bnb_datasets'

    results_path = 'bnb_run_results'

    file_list = [f for f in listdir(datasets_path) if isfile(join(datasets_path, f))]

    with Pool(processes=1) as pool:
        for file_name in file_list:
            print('Working on '+file_name)
            df = pd.read_csv(datasets_path+'/'+file_name, dtype=str)
            rows_list = []
            for index,row in df.iterrows():
                string_length = len(str(row['string_1']))

                #Dinamic Programming
                algorithm = 'dinamic_programming'
                results, duration_time, duration_clock = meassure_single_call_timeout(editDistanceDP,(row['string_1'],row['string_2']),timeout_time, pool)
                if isinstance(results, int):
                    ed = results
                else:
                    ed = results['ed']
                rows_list.append({'algorithm':algorithm, 'len':string_length, 'ed':ed, 'time':duration_time,'clock_time':duration_clock, 'calls':1})

                if not file_name.endswith('_200.csv'):
                    #Branch and bound (len)
                    algorithm = 'branch_and_bound_len'
                    results, duration_time, duration_clock = meassure_single_call_timeout(branch_bound_len_ed,(row['string_1'],row['string_2']),timeout_time, pool)
                    if isinstance(results, int):
                        ed = results
                        calls = -1
                    else:
                        ed = results['ed']
                        calls = results['calls']
                    rows_list.append({'algorithm':algorithm, 'len':string_length, 'ed':ed, 'time':duration_time,'clock_time':duration_clock, 'calls':calls})

                    #Branch and bound (count)
                    algorithm = 'branch_and_bound_cnt'
                    results, duration_time, duration_clock = meassure_single_call_timeout(branch_bound_cnt_ed,(row['string_1'],row['string_2']),timeout_time, pool)
                    if isinstance(results, int):
                        ed = results
                        calls = -1
                    else:
                        ed = results['ed']
                        calls = results['calls']
                    rows_list.append({'algorithm':algorithm, 'len':string_length, 'ed':ed, 'time':duration_time,'clock_time':duration_clock, 'calls':calls})

                print(index)

            result_df = pd.DataFrame(rows_list)
            result_df.to_csv(results_path+'/'+file_name,index=False)
