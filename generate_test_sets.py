import random
import string
import pandas as pd


#Generates a random string
def get_random_string(length=10, alphabet=string.ascii_lowercase):
    return ''.join(random.choice(alphabet) for i in range(length))


#Generates a pair of strings for testing
def get_pair_strings(pair_type, length, alphabet):
    if pair_type == 'samepair':
        rand_string = get_random_string(length,alphabet)
        return rand_string, rand_string
    if pair_type == 'atmost20':
        changes = int(length /5)
        rand_string_1 = get_random_string(length,alphabet)
        rand_string_2 = list(rand_string_1)
        for _ in range(0,changes):
            rand_string_2[random.randint(0,length-1)] = random.choice(alphabet)
        return rand_string_1, ''.join(rand_string_2)
    elif pair_type == 'randompair': #Random pairs
        return get_random_string(size,alphabet), get_random_string(length,alphabet)



#To keep consistency between runs
random.seed(4269)

#List of desired alphabets
alphabets = ['01',string.octdigits, string.hexdigits, string.digits, string.ascii_lowercase,string.ascii_letters]
#Number of samples per size
n = 10
#Place to output csv
destination_folder = 'datasets'


#To be used with all
#List of desired sizes (1-15, 20-100)
sizes = [x for x in range(1,16)]
for pair_type in ['samepair','atmost20','randompair']:
    for alphabet in alphabets:
        rows = []
        for size in sizes:
            for _ in range(0,n):
                string_1, string_2 = get_pair_strings(pair_type, size, alphabet)
                rows.append({'string_1':string_1,
                             'string_2':string_2})
        df = pd.DataFrame(rows)
        df.to_csv(destination_folder+'/set_'+str(alphabet)+'_'+pair_type+'_'+str(max(sizes))+'.csv', index=False)


#NOT to be used with pure recursion or branch and bound
#List of desired sizes (5-200, steps of 5)
sizes = [5*x for x in range(1,41)]
for pair_type in ['samepair','atmost20','randompair']:
    for alphabet in alphabets:
        rows = []
        for size in sizes:
            for _ in range(0,n):
                string_1, string_2 = get_pair_strings(pair_type, size, alphabet)
                rows.append({'string_1':string_1,
                             'string_2':string_2})
        df = pd.DataFrame(rows)
        df.to_csv('datasets/set_'+str(alphabet)+'_'+pair_type+'_'+str(max(sizes))+'.csv', index=False)