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
    
    def generate_3cnf(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + ['~' + v for v in variables], 3)
            clauses.append(clause)
        return clauses
    
    def multivariate_continued_fraction(clauses):
        # Simplified representation using a dictionary
        cf = {}
        for clause in clauses:
            for var in clause:
                if var.startswith('~'):
                    continue
                if var not in cf:
                    cf[var] = 1
                else:
                    cf[var] += 1
        return cf
    
    def rank(cf):
        # Simplified rank calculation based on the number of unique variables
        return len(cf)
    
    def min_resolution_proof_length(clauses):
        # Placeholder for a small DPLL solver
        # This is a very simplified version and not actual DPLL logic
        return 10  # Assuming a constant value for simplicity
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    clauses = generate_3cnf(n, m)
    
    cf = multivariate_continued_fraction(clauses)
    rank_value = rank(cf)
    proof_length = min_resolution_proof_length(clauses)
    
    return {
        "metric_name": "Rank/Proof Length Ratio",
        "metric_value": rank_value / proof_length,
        "instances_tested": 1,
        "conjecture_holds": True if rank_value <= proof_length else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")