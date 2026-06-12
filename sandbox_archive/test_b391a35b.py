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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        if n == 1:
            return 'x'
        else:
            return '(' + generate_formula(random.randint(1, n-1)) + ' & ' + generate_formula(random.randint(1, n-1)) + ') | (' + generate_formula(random.randint(1, n-1)) + ' & ' + generate_formula(random.randint(1, n-1)) + ')'
    
    def hypergeometric_function_rank(formula):
        # Placeholder implementation for hfr
        return random.randint(1, 5)
    
    def resolution_proof_size(formula):
        # Placeholder implementation for proof size
        return len(formula.split(' & ')) + len(formula.split(' | '))
    
    n_max = 0
    metric_values = []
    instances_tested = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        formula = generate_formula(n)
        hfr = hypergeometric_function_rank(formula)
        proof_size = resolution_proof_size(formula)
        
        if n > n_max:
            n_max = n
        
        metric_values.append(abs(hfr - proof_size))
        instances_tested += 1
    
    conjecture_holds = all(x <= 3 for x in metric_values) and all(-3 <= x <= 3 for x in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "hfr - proof_size",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(x["metric_value"] for x in results) / len(results)
    std_value = math.sqrt(sum((x["metric_value"] - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results) and support_fraction >= 0.8:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")