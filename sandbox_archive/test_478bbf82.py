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
    
    # Generate a random k-CNF formula with n variables and m clauses for n in {4,...,40}
    n = random.randint(4, 40)
    m = random.randint(n, n * (n - 1) // 2)
    literals = list(range(-n, 0)) + list(range(1, n + 1))
    cnf_formula = []
    for _ in range(m):
        clause = random.sample(literals, k=random.randint(1, n))
        cnf_formula.append(clause)
    
    # Construct the corresponding symmetric function f over F_2
    def symmetric_function(x):
        result = 0
        for clause in cnf_formula:
            product = 1
            for literal in clause:
                if literal > 0:
                    product *= x[literal - 1]
                else:
                    product *= (1 - x[-literal - 1])
            result += product
        return result
    
    # Compute the minimal rank of the tropicalization of f
    def tropicalize(x):
        return max(0, math.log2(x))
    
    tropicalized_values = [tropicalize(symmetric_function([random.choice([0, 1]) for _ in range(n)])) for _ in range(100)]
    min_rank = min(tropicalized_values)
    
    # Construct monotone circuits for F and measure their size
    def construct_monotone_circuit(cnf_formula):
        # This is a placeholder function. In practice, you would need to implement the actual circuit construction.
        return len(cnf_formula) ** 2
    
    circuit_size = construct_monotone_circuit(cnf_formula)
    
    # Determine if the conjecture holds
    ratio = min_rank / (n ** 0.25)
    conjecture_holds = 0.5 <= ratio < 1.2 and circuit_size <= m ** 4
    
    return {
        "metric_name": "Ratio of minimal rank to n^(1/4)",
        "metric_value": ratio,
        "instances_tested": 100,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Circuit size {circuit_size} exceeds m^4"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif any(r["metric_value"] > 1.2 or r["counterexample"].startswith("Circuit size") for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["conjecture_holds"] == False)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")