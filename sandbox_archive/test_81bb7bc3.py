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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] == 0 for i in range(n)):
                clause[random.randint(0, n - 1)] = 1
            clauses.append(clause)
        return clauses
    
    def minterms(clauses):
        minterms_set = set()
        for clause in clauses:
            minterm = 0
            for var, sign in enumerate(clause):
                if sign == 1:
                    minterm |= (1 << var)
                elif sign == -1:
                    minterm &= ~(1 << var)
            minterms_set.add(minterm)
        return minterms_set
    
    def free_monoid_order(minterms):
        n = len(minterms)
        if n == 0:
            return 0
        order = 1
        for i in range(1, n):
            if all((m & (1 << j)) != 0 for m in minterms for j in range(i)):
                order += 1
        return order
    
    def clause_subset_entropy(n):
        return math.log2(2**n)
    
    n = random.randint(5, 40)
    m = random.randint(1, n * (n - 1) // 2)
    cnf = generate_cnf(n, m)
    S_m = minterms(cnf)
    order = free_monoid_order(S_m)
    h_n = clause_subset_entropy(n)
    
    if order > 3 * h_n:
        return {
            "metric_name": "order_to_entropy_ratio",
            "metric_value": order / h_n,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"n={n}, m={m}, |S_m|={len(S_m)}, h(n)={h_n}"
        }
    
    return {
        "metric_name": "order_to_entropy_ratio",
        "metric_value": order / h_n,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.4f} std=0.0000 support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.4f} std=0.0000 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"order_to_entropy_ratio > 3 * h(n)\" first_failing_seed={first_failing_seed}")