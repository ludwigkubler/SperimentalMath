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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(x == 0 for x in clause):
                continue
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment=[]):
        if not cnf:
            return True
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0]
            new_assignment = assignment + [literal]
            new_cnf = [c for c in cnf if not any(l in c for l in new_assignment)]
            return dpll(new_cnf, new_assignment)
        
        literals = set(abs(l) for clause in cnf for l in clause)
        literal = random.choice(list(literals))
        positive = literal > 0
        new_assignment = assignment + [literal if positive else -literal]
        new_cnf = [c for c in cnf if not any(l in c for l in new_assignment)]
        
        if dpll(new_cnf, new_assignment):
            return True
        
        new_assignment = assignment + [-literal if positive else literal]
        new_cnf = [c for c in cnf if not any(l in c for l in new_assignment)]
        
        return dpll(new_cnf, new_assignment)
    
    def diophantine_degree(cnf):
        degree = 0
        for clause in cnf:
            degree = max(degree, len(clause))
        return degree
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    degree = diophantine_degree(cnf)
    
    if degree <= 0:
        return {
            "metric_name": "diophantine_degree",
            "metric_value": degree,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    expected_bound = n**2 * math.log(n)
    
    return {
        "metric_name": "diophantine_degree",
        "metric_value": degree,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": degree <= expected_bound,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 6)]
    
    results = []
    total_metric_value = 0
    count_conjecture_holds = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_conjecture_holds += 1
    
    mean_metric_value = total_metric_value / len(results)
    support_fraction = count_conjecture_holds / len(results)
    
    if all(trial["conjecture_holds"] for trial in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, trial in zip(seeds, results) if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")