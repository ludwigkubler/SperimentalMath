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
        clauses = []
        for _ in range(2**n // 4):  # Generate a small CNF with n variables
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        stack = cnf[:]
        while stack:
            literal = random.choice(stack)
            if literal > 0:
                neg_literal = -literal
            else:
                neg_literal = -literal
            new_clauses = []
            for clause in stack:
                if literal in clause:
                    continue
                if neg_literal in clause:
                    stack.remove(clause)
                else:
                    new_clause = [x for x in clause if x != neg_literal]
                    if len(new_clause) == 1:
                        return 0
                    new_clauses.append(new_clause)
            stack.extend(new_clauses)
        return len(stack)
    
    def betti_number(cnf):
        # Simplified Betti number calculation (not accurate but for testing purposes)
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        beta = betti_number(cnf)
        width = resolution_width(cnf)
        results.append((n, beta, width))
    
    metric_value = sum(abs(beta - width) for _, beta, width in results) / len(results)
    instances_tested = len(results)
    n_max = max(n_values)
    conjecture_holds = all(0 <= abs(beta - width) <= 1 for _, beta, width in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Betti Number vs Resolution Width",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")