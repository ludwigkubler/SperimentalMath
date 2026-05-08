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

def generate_read_twice_branching_program(n):
    program = []
    for i in range(2**n):
        if i % 2 == 0:
            program.append((i, (random.choice([0, 1]), random.choice([0, 1]))))
        else:
            program.append((i, (random.choice([0, 1]), random.choice([0, 1]))))
    return program

def generate_read_once_branching_program(n):
    program = []
    for i in range(2**n):
        if i % 2 == 0:
            program.append((i, random.choice([0, 1])))
        else:
            program.append((i, random.choice([0, 1])))
    return program

def inner_product_mod_2(n, x):
    result = 0
    for i in range(n):
        result += x[i]
    return result % 2

def fourier_coefficient_sum(program, n):
    sum_abs_coeffs = 0
    for state, (a, b) in program:
        if a == b:
            sum_abs_coeffs += 1
        else:
            sum_abs_coeffs -= 1
    return abs(sum_abs_coeffs)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    ip_2_program = generate_read_twice_branching_program(n)
    ro_program = generate_read_once_branching_program(n)
    
    ip_2_sum_coeffs = fourier_coefficient_sum(ip_2_program, n)
    ro_sum_coeffs = fourier_coefficient_sum(ro_program, n)
    
    metric_name = "Fourier Coefficient Sum"
    metric_value_ip_2 = ip_2_sum_coeffs
    metric_value_ro = ro_sum_coeffs
    
    instances_tested = 1
    conjecture_holds = (metric_value_ip_2 >= math.sqrt(n)) and (metric_value_ro <= math.log(n))
    counterexample = ""
    
    if not conjecture_holds:
        counterexample = "IP_2 sum does not meet Ω(√n) or RO sum does not meet O(log n)"
    
    return {
        "metric_name": metric_name,
        "metric_value_ip_2": metric_value_ip_2,
        "metric_value_ro": metric_value_ro,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value_ip_2\": {result['metric_value_ip_2']}, \"metric_value_ro\": {result['metric_value_ro']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ip_2 = sum(r['metric_value_ip_2'] for r in results) / len(results)
    std_ip_2 = math.sqrt(sum((r['metric_value_ip_2'] - mean_ip_2)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ip_2} std={std_ip_2} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")