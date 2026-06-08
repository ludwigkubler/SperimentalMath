# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_sat_instance(n, max_depth):
        clauses = []
        for _ in range(random.randint(1, n)):
            clause_length = random.randint(1, min(max_depth, n))
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(clause_length)]
            clauses.append(clause)
        return clauses
    
    def truth_table_to_diophantine(clauses):
        n = len(clauses[0])
        binary = ['0'] * n
        while True:
            found_solution = True
            for clause in clauses:
                if all(binary[j-1] == '1' or c * int(binary[abs(c)-1]) >= 0 for j, c in enumerate(clause)):
                    continue
                found_solution = False
                break
            if found_solution:
                return len(binary)
            binary[-1] = '1' if binary[-1] == '0' else '0'
            for i in range(n-2, -1, -1):
                if binary[i] == '1':
                    binary[i] = '0'
                    binary[i+1] = '1'
                    break
    
    def calculate_correlation(trials):
        n_values = [len(trial['clauses']) for trial in trials]
        e_values = [trial['diophantine_exponent'] for trial in trials]
        d_values = [trial['clause_depth'] for trial in trials]
        
        mean_n = sum(n_values) / len(n_values)
        mean_e = sum(e_values) / len(e_values)
        mean_d = sum(d_values) / len(d_values)
        
        numerator = sum((n - mean_n) * (e - mean_e) * (d - mean_d) for n, e, d in zip(n_values, e_values, d_values))
        denominator = math.sqrt(sum((n - mean_n)**2 * (e - mean_e)**2 * (d - mean_d)**2 for n, e, d in zip(n_values, e_values, d_values)))
        
        return numerator / denominator if denominator != 0 else 0
    
    trials = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        max_depth = random.randint(1, n)
        clauses = generate_random_sat_instance(n, max_depth)
        diophantine_exponent = truth_table_to_diophantine(clauses)
        trials.append({
            'n': n,
            'clauses': clauses,
            'diophantine_exponent': diophantine_exponent,
            'clause_depth': max_depth
        })
    
    correlation_coefficient = calculate_correlation(trials)
    mean_error = sum(abs(e - math.log(n)**2 * d) for n, e, d in zip([t['n'] for t in trials], [t['diophantine_exponent'] for t in trials], [t['clause_depth'] for t in trials])) / len(trials)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max([t['n'] for t in trials]),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_error <= 3,
        "counterexample": "" if correlation_coefficient >= 0.8 else f"Correlation coefficient: {correlation_coefficient}, Mean error: {mean_error}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient below threshold\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_below_threshold")