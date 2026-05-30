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

def generate_cnf(n, seed):
    random.seed(seed)
    cnf = []
    for _ in range(random.randint(5, 10)):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        cnf.append(clause)
    return cnf

def diophantine_exponent(cnf):
    n = len(cnf[0])
    Z_d = list(range(1, 2*n))
    d = 1
    while True:
        if all(any(lit % d == Z_d[var-1] for lit in clause) for clause in cnf):
            return d
        d += 1

def dpll_refutation_time(cnf):
    n = len(cnf[0])
    clauses = [set(clause) for clause in cnf]
    literals = set(range(1, n+1)) | {-i for i in range(1, n+1)}
    
    def solve(state):
        if not clauses:
            return True
        literal = next(lit for lit in literals if lit not in state and -lit not in state)
        for val in [True, False]:
            new_state = state.copy()
            new_state[literal] = val
            if all(not clause.intersection(new_state) for clause in clauses):
                if solve(new_state):
                    return True
        return False
    
    start_time = time.time()
    solve({})
    end_time = time.time()
    return end_time - start_time

def run_trial(seed: int) -> dict:
    n_max = 40
    instances_tested = 0
    metric_value_total = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        cnf = generate_cnf(n, seed)
        d = diophantine_exponent(cnf)
        refutation_time = dpll_refutation_time(cnf)
        if refutation_time == 0:
            continue
        ratio = (n**d * math.log(n)) / refutation_time
        metric_value_total += ratio
        instances_tested += 1
        
        if ratio > 3:
            conjecture_holds = False
            counterexample = f"n={n}, d={d}, refutation_time={refutation_time}"
    
    metric_name = "Ratio of n^d * log(n) to DPLL refutation time"
    metric_value = metric_value_total / instances_tested if instances_tested > 0 else 0.0
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")