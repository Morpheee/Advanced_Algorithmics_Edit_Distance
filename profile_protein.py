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
    timeout_time = 60

    try:
        datasets_path = sys.argv[1]
    except:
        datasets_path = 'protein_dataset'

    results_path = 'protein_results'

    file_list = [f for f in listdir(datasets_path) if isfile(join(datasets_path, f))]

    with Pool(processes=1) as pool:
        for file_name in file_list:
            if file_name.startswith('protein_'):
                print('Working on '+file_name)
                df = pd.read_csv(datasets_path+'/'+file_name, dtype=str)
                rows_list = []
                for index,row in df.iterrows():
                    string_length = max(len(str(row['protein_1'])),len(str(row['protein_2'])))

                    #Greedy approach
                    algorithm = 'greedy_approach'
                    results, duration_time, duration_clock = meassure_single_call_timeout(edit_distance_greedy,(row['protein_1'],row['protein_2']),timeout_time, pool)
                    if isinstance(results, int):
                        ed = results
                    else:
                        ed = results['ed']
                    rows_list.append({'algorithm':algorithm, 'len':string_length, 'ed':ed, 'time':duration_time,'clock_time':duration_clock, 'calls':1})

                    #Divide and conquer
                    algorithm = 'divide_and_conquer'
                    results, duration_time, duration_clock = meassure_single_call_timeout(divide_and_conquer_ed,(row['protein_1'],row['protein_2']),timeout_time, pool)
                    if isinstance(results, int):
                        ed = results
                    else:
                        ed = results['ed']
                    rows_list.append({'algorithm':algorithm, 'len':string_length, 'ed':ed, 'time':duration_time,'clock_time':duration_clock, 'calls':1})

                    #Dinamic Programming
                    algorithm = 'dinamic_programming'
                    results, duration_time, duration_clock = meassure_single_call_timeout(editDistanceDP,(row['protein_1'],row['protein_2']),timeout_time, pool)
                    if isinstance(results, int):
                        ed = results
                    else:
                        ed = results['ed']
                    rows_list.append({'algorithm':algorithm, 'len':string_length, 'ed':ed, 'time':duration_time,'clock_time':duration_clock, 'calls':1})

                    #Dinamic Programming
                    algorithm = 'dinamic_programming_2'
                    results, duration_time, duration_clock = meassure_single_call_timeout(ed_dp,(row['protein_1'],row['protein_2']),timeout_time, pool)
                    if isinstance(results, int):
                        ed = results
                    else:
                        ed = results['ed']
                    rows_list.append({'algorithm':algorithm, 'len':string_length, 'ed':ed, 'time':duration_time,'clock_time':duration_clock, 'calls':1})

                result_df = pd.DataFrame(rows_list)
                result_df.to_csv(results_path+'/'+file_name,index=False)
