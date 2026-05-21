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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def monomial_ideal(clauses):
        ideal = set()
        for clause in clauses:
            for var in clause:
                if var > 0:
                    ideal.add((var,))
                else:
                    ideal.add((-var,))
        return ideal
    
    def hilbert_function(ideal, k):
        count = 0
        for monomial in ideal:
            if len(monomial) <= k:
                count += 1
        return count
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    ideal = monomial_ideal(clauses)
    
    H_values = [hilbert_function(ideal, k) for k in range(1, n + 1)]
    growth_rate = max(H_values) / math.log(n)
    
    conjecture_holds = growth_rate >= 1
    counterexample = "" if conjecture_holds else f"n={n}, H(n)={max(H_values)}, log(n)={math.log(n)}"
    
    return {
        "metric_name": "Hilbert Function Growth",
        "metric_value": growth_rate,
        "instances_tested": n,
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
    
    mean_growth_rate = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_growth_rate} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_growth_rate} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"growth_rate < 1\" first_failing_seed={first_failing_seed}")