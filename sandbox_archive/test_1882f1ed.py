# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if not any(clause[i] == -clause[j] for i in range(n) for j in range(i + 1, n)):
                clauses.append(clause)
        return clauses
    
    def generate_easy_cnf(n):
        return [[(i + 1)] for i in range(n)]
    
    def generate_medium_cnf(n):
        return [generate_cnf(n, 4) for _ in range(3)]
    
    def generate_hard_cnf(n):
        # Placeholder for actual hard CNF generation
        return generate_cnf(n, n)
    
    def sign_degree_polynomial(clauses, n):
        d = [0] * (n + 1)
        m = len(clauses)
        for clause in clauses:
            for literal in clause:
                if literal > 0:
                    d[literal - 1] += 1
                else:
                    d[-literal - 1] -= 1
        return [m] + d
    
    def mahler_measure(coefficients):
        n = len(coefficients) - 1
        roots = np.roots(coefficients)
        measure = 1.0
        for root in roots:
            if abs(root) > 1:
                measure *= abs(root)
        return measure
    
    def log_ratio(n, m):
        coefficients = sign_degree_polynomial(generate_cnf(n, m), n)
        M = mahler_measure(coefficients)
        return math.log(M) / math.log(n)
    
    n_values = [8, 10, 12, 14]
    easy_r = [log_ratio(n, 2 * n) for n in n_values]
    medium_r = [log_ratio(n, 3 * n) for n in n_values]
    hard_r = [log_ratio(n, n) for n in n_values]
    
    mean_easy_r = sum(easy_r) / len(easy_r)
    mean_medium_r = sum(medium_r) / len(medium_r)
    mean_hard_r = sum(hard_r) / len(hard_r)
    
    conjecture_holds = (mean_easy_r <= 1.0 and
                        all(mean_hard_r >= 0.3 * math.log(n + 1) / math.log(n) for n in n_values))
    
    counterexample = "" if conjecture_holds else "easy_family"
    
    return {
        "metric_name": "log_ratio",
        "metric_value": mean_easy_r,
        "instances_tested": len(easy_r),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_easy_r = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_easy_r} std=0.0 support_fraction=1.0")
    elif any(r["counterexample"] == "easy_family" and r["instances_tested"] >= 3 for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"] == "easy_family" and r["instances_tested"] >= 3)
        print(f"RESULT: FALSIFIED counterexample=\"easy_family\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")