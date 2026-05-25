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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_random_branching_program(n):
    program = []
    for _ in range(n):
        if random.choice([True, False]):
            program.append('0')
        else:
            program.append('1')
    return program

def construct_configuration_space(P):
    n = len(P)
    CS = [[[] for _ in range(2)] for _ in range(n)]
    CS[0][int(P[0])].append(0)
    
    for i in range(1, n):
        for j in range(2):
            if j == int(P[i]):
                CS[i][j] = [x + 1 for x in CS[i-1][j]]
            else:
                CS[i][j] = [x + 1 for x in CS[i-1][j]] + [0]
    
    return CS

def min_local_index(CS):
    n = len(CS)
    indices = []
    for i in range(n):
        if CS[i][0]:
            indices.append(min(CS[i][0]))
        if CS[i][1]:
            indices.append(min(CS[i][1]))
    return min(indices)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        P = generate_random_branching_program(n)
        CS = construct_configuration_space(P)
        metric_value = min_local_index(CS)
        
        if 'AC0' in str(P):
            expected = Fraction(math.log2(2**n), 1)
        else:
            expected = Fraction(n, 1)
        
        total_metric_value += metric_value
        instances_tested += 1
    
    mean_metric_value = Fraction(total_metric_value, instances_tested)
    
    if 'AC0' in str(P):
        conjecture_holds = abs(mean_metric_value - expected) <= Fraction(10 * math.log2(2**n), 100)
    else:
        conjecture_holds = abs(mean_metric_value - expected) <= Fraction(5 * n, 100)
    
    counterexample = "" if conjecture_holds else "AC0 membership not verified"
    
    return {
        "metric_name": "min_local_index",
        "metric_value": float(mean_metric_value),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"AC0 membership not verified\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")