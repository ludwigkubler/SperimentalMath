# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    instances_tested = 30
    
    def gowers_norm(f):
        norm = 0
        for i in range(2**n):
            sum_val = 0
            for j in range(2**n):
                sum_val += f[i] * f[j] * (-1)**bin(i^j).count('1')
            norm += sum_val**2
        return math.sqrt(norm / (2**(2*n)))
    
    def dpll_circuit_minimization(f):
        # Simplified DPLL-based heuristic for circuit minimization
        clauses = []
        for i in range(2**n):
            if f[i] != 0:
                clause = [i]
                for j in range(n):
                    if (i >> j) & 1 == 0:
                        clause.append(-j-1)
                clauses.append(clause)
        # Recursive partitioning with clause learning
        def learn_clause(clause):
            return clause
        
        learned_clauses = []
        while True:
            new_clause = learn_clause(random.choice(clauses))
            if new_clause not in learned_clauses:
                learned_clauses.append(new_clause)
            else:
                break
        return len(learned_clauses)
    
    def boolean_function():
        return [random.randint(0, 1) for _ in range(2**n)]
    
    metric_value = 0
    conjecture_holds = True
    
    for _ in range(instances_tested):
        f = boolean_function()
        norm = gowers_norm(f)
        size = dpll_circuit_minimization(f)
        if norm * size < 1 / math.sqrt(n):
            conjecture_holds = False
            counterexample = "Gowers norm * circuit size < 1/√n"
            break
    
    return {
        "metric_name": "gowers_norm * circuit_size",
        "metric_value": norm * size,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131]
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")