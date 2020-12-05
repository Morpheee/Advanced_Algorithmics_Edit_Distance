import sys

#TODO define parameters
"""
parameters:
    string_a: first string to compare
    string_b: second string to compare
    cost: the carried cost so far, starts as 0, when first call
    bound: the maximum cost allowed
    operations: the carried out operations.

returns:
    cost: incurred cost of the performed operations
    operations: array (in order) of the performed operations. It's assumed operations are on string_b

Heuristic:
    Assumed cost of skipping letters or length difference.

"""
def branch_bound_len_ed(string_a, string_b, cost=0, bound=0, operations=[]):
    
    #Recursive calls count
    calls=0
    
    #Reused variables
    len_a = len(string_a)
    len_b = len(string_b)
    
    #Setting bound if not existing
    if bound==0:
        bound = max(len_a,len_b)
    
    #Handling edge cases first
    
    #Both empty strings
    #No added cost from any operation
    if len_a == 0 and len_b == 0:
        return {'ed':cost, 'operations': operations, 'calls':calls+1}
    
    #String a is empty
    #Added cost and operations for deleting characters in string b
    if len_a == 0 and len_b > 0:
        return {'ed':cost+len_b, 'operations': operations + [{'del': x} for x in string_b], 'calls':calls+1}

    #String b is empty
    #Added cost and operations for inserting characters in string b
    if len_b == 0 and len_a > 0:
        return {'ed':cost+len_a, 'operations': operations + [{'ins': x} for x in string_a], 'calls':calls+1}
    
    #Handling recursive case

    #Heuristics:
    weight_substitution = abs(len_b - len_a) + cost #Assumed equal string, except for the difference
    weight_deletion = abs(len_b - len_a - 1) + cost #Assumed cost of skipping a letter in word b
    weight_insertion = abs(len_a - len_b - 1) + cost #Assumed cost of skipping a letter in word a
    
    #Substitution branch
    if weight_substitution <= bound:
        #Current characters are equal, so no operation needed
        if string_a[0] == string_b[0]:
            sub_branch = branch_bound_len_ed(string_a[1:], string_b[1:], cost, bound, operations + [{'skp': string_a[0]}])
        else:
            sub_branch = branch_bound_len_ed(string_a[1:], string_b[1:], cost+1, bound, operations + [{'sub': string_a[0]}])
        sub_cost = sub_branch['ed']
        calls += 1 + sub_branch['calls']
        bound =  min(sub_cost,bound)
    else:
        sub_cost = sys.maxsize
    
    #Deletion branch
    if weight_deletion <= bound:
        del_branch = branch_bound_len_ed(string_a, string_b[1:], cost+1, bound, operations + [{'del': string_b[0]}])
        del_cost = del_branch['ed']
        calls += 1 + del_branch['calls']
        bound =  min(del_cost,bound)
    else:
        del_cost = sys.maxsize

    #Insertion branch
    if weight_insertion <= bound:
        ins_branch = branch_bound_len_ed(string_a[1:], string_b, cost+1, bound, operations + [{'ins': string_a[0]}])
        ins_cost = ins_branch['ed']
        calls += 1 + ins_branch['calls']
        bound =  min(ins_cost,bound)
    else:
        ins_cost = sys.maxsize

    #Selecting between the 3 branches
    min_cost = min(del_cost,ins_cost,sub_cost)
    
    #Return min branch, or nothing if all branches were ignored
    if min_cost == sys.maxsize:
        return {'ed':sys.maxsize, 'operations': operations, 'calls':calls}
    elif sub_cost == min_cost:
        sub_branch['calls'] = calls
        return sub_branch
    elif del_cost == min_cost:
        del_branch['calls'] = calls
        return del_branch
    elif ins_cost == min_cost:
        ins_branch['calls'] = calls
        return ins_branch




"""
parameters:
    string_a: first string to compare
    string_b: second string to compare
    cost: the carried cost so far, starts as 0, when first call
    bound: the maximum cost allowed
    operations: the carried out operations.
returns:
    cost: incurred cost of the performed operations
    operations: array (in order) of the performed operations. It's assumed operations are on string_b

Heuristic:
    Assumed cost of not using common letter instead of removing them

"""
def branch_bound_cnt_ed(string_a, string_b, cost=0, bound=0, operations=[], freq = {}):
    
    #Recursive calls count
    calls=0
    
    #Reused variables
    len_a = len(string_a)
    len_b = len(string_b)
    
    #Setting bound if not existing
    if bound==0:
        bound = max(len_a,len_b)
        freq_a = {}
        for i in string_a: 
            if i in freq_a: 
                freq_a[i] += 1
            else: 
                freq_a[i] = 1
        freq_b = {}
        for i in string_b: 
            if i in freq_b: 
                freq_b[i] += 1
            else: 
                freq_b[i] = 1
        freq = {}
        for key in freq_a:
            if key in freq_b: 
                freq[key] = min(freq_a[key],freq_b[key])
            
    #Handling edge cases first
    
    #Both empty strings
    #No added cost from any operation
    if len_a == 0 and len_b == 0:
        return {'ed':cost, 'operations': operations, 'calls':calls+1}
    
    #String a is empty
    #Added cost and operations for deleting characters in string b
    if len_a == 0 and len_b > 0:
        return {'ed':cost+len_b, 'operations': operations + [{'del': x} for x in string_b], 'calls':calls+1}

    #String b is empty
    #Added cost and operations for inserting characters in string b
    if len_b == 0 and len_a > 0:
        return {'ed':cost+len_a, 'operations': operations + [{'ins': x} for x in string_a], 'calls':calls+1}
    
    #Handling recursive case

    #Heuristics:
    #Max amount of remaining strings to edit + carried cost - common letters carried
    freq_cost = max(len_a,len_b) + cost - sum(freq.values())
    
    weight_substitution = freq_cost + (1 if string_a[0]!=string_b[0] and (string_a[0] in freq or string_b[0] in freq) else 0)
    weight_deletion = freq_cost + (1 if string_b[0] in freq else 0)
    weight_insertion = freq_cost + (1 if string_a[0] in freq else 0)
    
    #Substitution branch
    if weight_substitution <= bound:
        #Current characters are equal, so no operation needed
        freq_sub = freq.copy()
        if string_a[0] == string_b[0]:
            if string_a[0] in freq_sub:
                freq_sub[string_a[0]] -= 1
                if freq_sub[string_a[0]] == 0:
                    freq_sub.pop(string_a[0])
            sub_branch = branch_bound_cnt_ed(string_a[1:], string_b[1:], cost, bound, operations + [{'skp': string_a[0]}], freq_sub)
        else:
            if string_a[0] in freq_sub:
                freq_sub[string_a[0]] -= 1
                if freq_sub[string_a[0]] == 0:
                    freq_sub.pop(string_a[0])
            elif string_b[0] in freq_sub:
                freq_sub[string_b[0]] -= 1
                if freq_sub[string_b[0]] <= 0:
                    freq_sub.pop(string_b[0])
            sub_branch = branch_bound_cnt_ed(string_a[1:], string_b[1:], cost+1, bound, operations + [{'sub': string_a[0]}], freq_sub)
        sub_cost = sub_branch['ed']
        calls += 1 + sub_branch['calls']
        bound =  min(sub_cost,bound)
    else:
        sub_cost = sys.maxsize
    
    #Deletion branch
    if weight_deletion <= bound:
        freq_del = freq.copy()
        if string_b[0] in freq_del:
            freq_del[string_b[0]] -= 1
            if freq_del[string_b[0]] <= 0:
                freq_del.pop(string_b[0])
        del_branch = branch_bound_cnt_ed(string_a, string_b[1:], cost+1, bound, operations + [{'del': string_b[0]}], freq_del)
        del_cost = del_branch['ed']
        calls += 1 + del_branch['calls']
        bound =  min(del_cost,bound)
    else:
        del_cost = sys.maxsize

    #Insertion branch
    if weight_insertion <= bound:
        freq_ins = freq.copy()
        if string_a[0] in freq_ins:
            freq_ins[string_a[0]] -= 1
            if freq_ins[string_a[0]] <= 0:
                freq_ins.pop(string_a[0])
        ins_branch = branch_bound_cnt_ed(string_a[1:], string_b, cost+1, bound, operations + [{'ins': string_a[0]}], freq_ins)
        ins_cost = ins_branch['ed']
        calls += 1 + ins_branch['calls']
        bound =  min(ins_cost,bound)
    else:
        ins_cost = sys.maxsize

    #Selecting between the 3 branches
    min_cost = min(del_cost,ins_cost,sub_cost)
    
    #Return min branch, or nothing if all branches were ignored
    if min_cost == sys.maxsize:
        return {'ed':sys.maxsize, 'operations': operations, 'calls':calls}
    elif sub_cost == min_cost:
        sub_branch['calls'] = calls
        return sub_branch
    elif del_cost == min_cost:
        del_branch['calls'] = calls
        return del_branch
    elif ins_cost == min_cost:
        ins_branch['calls'] = calls
        return ins_branch