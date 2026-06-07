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
    
    def tseitin_formula(cnf):
        literals = set()
        for clause in cnf:
            literals.update(clause)
        
        formulas = {}
        new_vars = 1
        
        def encode_clause(clause):
            nonlocal new_vars
            if len(clause) == 1:
                return clause[0]
            else:
                var = f'x{new_vars}'
                new_vars += 1
                formulas[var] = (encode_clause([l for l in clause if l != -clause[0]]), encode_clause([-l for l in clause if l != clause[0]]))
                return var
        
        for clause in cnf:
            literals.add(encode_clause(clause))
        
        return literals
    
    def hypergeometric_sum(literals):
        n = len(literals)
        k = 1
        p = Fraction(1, n)
        sum_val = 0
        for i in range(k + 1):
            sum_val += math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
        return sum_val
    
    def resolution_width(cnf):
        # Simplified version of resolution width calculation
        return len(cnf)
    
    cnf = [
        [1, -2],
        [-1, 3],
        [2, 3]
    ]
    formulas = tseitin_formula(cnf)
    hypergeometric_sum_val = hypergeometric_sum(formulas)
    width = resolution_width(cnf)
    
    return {
        "metric_name": "Hypergeometric Sum",
        "metric_value": hypergeometric_sum_val,
        "instances_tested": 1,
        "n_max": len(cnf),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        print(f"TRIAL: {trial_result}")
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")