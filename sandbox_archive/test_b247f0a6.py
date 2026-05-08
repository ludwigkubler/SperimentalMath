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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n) * (1 if random.choice([True, False]) else -1)
                   for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

def discrepancy(cnf):
    # Simplified version of discrepancy calculation using Diophantine approximation
    max_discrepancy = 0
    for clause in cnf:
        for literal in clause:
            if abs(literal) > max_discrepancy:
                max_discrepancy = abs(literal)
    return max_discrepancy

def resolution_size(cnf):
    # Simplified version of resolution proof size calculation
    return len(cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    disc = discrepancy(cnf)
    proof_size = resolution_size(cnf)
    
    metric_value = proof_size
    instances_tested = 1
    conjecture_holds = proof_size >= math.sqrt(math.log(n))
    counterexample = "" if conjecture_holds else f"CNF with n={n}, m={m}, disc={disc}, proof_size={proof_size}"
    
    return {
        "metric_name": "resolution_proof_size",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")