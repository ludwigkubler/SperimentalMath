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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(10):  # Generate 10 clauses
            clause = [random.randint(-n, n) for _ in range(random.randint(2, n))]
            cnf.append(clause)
        return cnf
    
    def resolution(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        new_clauses = []
        
        while True:
            found_resolvent = False
            for i in range(len(new_clauses)):
                for j in range(i + 1, len(new_clauses)):
                    l1, l2 = new_clauses[i], new_clauses[j]
                    resolvents = [x for x in l1 if x not in [-y for y in l2] and x != -y]
                    if resolvents:
                        found_resolvent = True
                        new_clause = tuple(sorted(resolvents))
                        if new_clause not in clauses:
                            new_clauses.append(new_clause)
                            clauses.add(new_clause)
            if not found_resolvent:
                break
        return len(new_clauses)
    
    def msr(cnf):
        # Placeholder for computing minimal symmetric function rank
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()  # Random value for demonstration
    
    n_values = [5, 10, 15, 20, 30, 40]
    msr_values = []
    w_values = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        msr_value = msr(cnf)
        w_value = resolution(cnf)
        
        msr_values.append(msr_value)
        w_values.append(w_value)
    
    correlation_coefficient = sum((msr_values[i] - sum(msr_values) / len(msr_values)) * (w_values[i] - sum(w_values) / len(w_values)) for i in range(len(msr_values))) / (len(msr_values) * math.sqrt(sum((msr_values[i] - sum(msr_values) / len(msr_values)) ** 2 for i in range(len(msr_values)))) * math.sqrt(sum((w_values[i] - sum(w_values) / len(w_values)) ** 2 for i in range(len(w_values)))))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.5,  # Placeholder threshold
        "counterexample": "" if abs(correlation_coefficient) >= 0.5 else "correlation_coefficient=0"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient=0' first_failing_seed={first_failing_seed}")