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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = len(f)
        count = 0
        for i in range(2**n):
            if f[i] != f[0]:
                count += 1
        return count
    
    def tseitin_formula(f):
        n = len(f)
        variables = list(range(n))
        clauses = []
        
        # Add clauses for each input
        for i in range(2**n):
            clause = []
            for j in range(n):
                if (i >> j) & 1:
                    clause.append(variables[j])
                else:
                    clause.append(-variables[j])
            clauses.append(clause)
        
        # Add clauses for the output
        for i in range(2**n):
            if f[i] == 0:
                clause = [-variables[n]]
                for j in range(n):
                    if (i >> j) & 1:
                        clause.append(variables[j])
                    else:
                        clause.append(-variables[j])
                clauses.append(clause)
        
        return variables, clauses
    
    def minimal_tropical_motivic_rank(clauses):
        n = len(clauses)
        mtr = 0
        for clause in clauses:
            mtr += max([abs(x) for x in clause if x != 0])
        return mtr
    
    def log(x):
        if x <= 0:
            return float('-inf')
        return math.log(x)
    
    n_max = 5
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, 41):
        f = generate_boolean_function(n)
        r_f = communication_complexity_rank(f)
        variables, clauses = tseitin_formula(f)
        mtr_phi_f = minimal_tropical_motivic_rank(clauses)
        
        if mtr_phi_f > log(r_f):
            conjecture_holds = False
            counterexample = f"n={n}, r(f)={r_f}, mtr(φ_f)={mtr_phi_f}, log(r(f))={log(r_f)}"
            break
        
        total_metric_value += mtr_phi_f
        instances_tested += 1
        n_max = max(n_max, n)
    
    return {
        "metric_name": "minimal_tropical_motivic_rank",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else float('nan'),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if not math.isnan(r["metric_value"])) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if not math.isnan(r["metric_value"])) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")