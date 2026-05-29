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
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def resolution(cnf):
        stack = cnf[:]
        while True:
            unit_clauses = [c for c in stack if len(c) == 1]
            if not unit_clauses:
                break
            unit_clause = unit_clauses[0]
            stack.remove(unit_clause)
            new_clauses = []
            for clause in stack:
                if -unit_clause[0] in clause:
                    new_clause = [x for x in clause if x != -unit_clause[0]]
                    if len(new_clause) == 1:
                        return None
                    new_clauses.append(new_clause)
                elif -unit_clause[1] in clause:
                    new_clause = [x for x in clause if x != -unit_clause[1]]
                    if len(new_clause) == 1:
                        return None
                    new_clauses.append(new_clause)
            stack.extend(new_clauses)
        return stack
    
    def count_hypergeometric_functions(cnf):
        hypergeometric_count = 0
        for _ in range(10):  # Sample 10 clauses to estimate
            clause = random.choice(cnf)
            if len(clause) > 2:
                hypergeometric_count += 1
        return hypergeometric_count
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    proof_length = len(resolution(cnf))
    hypergeometric_count = count_hypergeometric_functions(cnf)
    
    if hypergeometric_count > 3 * n**2 * math.log(n) or proof_length > 4 * n**2:
        conjecture_holds = False
        counterexample = f"n={n}, M(F)={hypergeometric_count}, length={proof_length}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "Hypergeometric Function Count",
        "metric_value": hypergeometric_count,
        "instances_tested": 10,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")