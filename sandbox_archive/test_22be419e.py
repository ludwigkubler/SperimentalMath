# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def compute_minterms(clauses):
        minterms = set()
        for assignment in itertools.product([0, 1], repeat=n):
            if all(all(assignment[var - 1] == clause[var - 1] for var in clause) for clause in clauses):
                minterm = tuple(assignment)
                minterms.add(minterm)
        return minterms
    
    def compute_clause_subset_entropy(n, m):
        total_subsets = 2 ** n
        non_empty_subsets = total_subsets - 1
        entropy = sum(Fraction(1, non_empty_subsets) * (n + 1) for _ in range(m))
        return float(entropy)
    
    def min_order_free_monoid(minterms):
        m = len(minterms)
        if m == 0:
            return 0
        order = 1
        while True:
            found = False
            for i in range(m):
                for j in range(i + 1, m):
                    new_minterm = tuple((x ^ y) % 2 for x, y in zip(minterms[i], minterms[j]))
                    if new_minterm not in minterms:
                        minterms.add(new_minterm)
                        found = True
            if not found:
                break
            order += 1
        return order
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(1, n * (n + 1) // 2)
            clauses = generate_cnf(n, m)
            minterms = compute_minterms(clauses)
            h_n = compute_clause_subset_entropy(n, m)
            order = min_order_free_monoid(minterms)
            
            if order > Fraction(3, 2) * h_n:
                return {
                    "metric_name": "order_vs_entropy",
                    "metric_value": order,
                    "instances_tested": 1,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, m={m}, |S_m|={len(minterms)}, h(n)={h_n}"
                }
    
    return {
        "metric_name": "order_vs_entropy",
        "metric_value": sum(order for _, order in results) / len(results),
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r > Fraction(3, 2) * compute_clause_subset_entropy(n_values[-1], random.randint(1, n_values[-1] * (n_values[-1] + 1) // 2))) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r > Fraction(3, 2) * compute_clause_subset_entropy(n_values[-1], random.randint(1, n_values[-1] * (n_values[-1] + 1) // 2)) for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"order exceeds entropy\" first_failing_seed={seeds[results.index(max(results))]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")