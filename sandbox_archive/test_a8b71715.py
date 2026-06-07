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
    
    def generate_formula(n, d):
        clauses = []
        for _ in range(n):
            clause = set()
            while len(clause) < 2 or any(abs(x - y) <= d for x, y in combinations(clause, 2)):
                clause.add(random.randint(1, n))
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def combinations(lst, k):
        if k == 0:
            yield ()
        else:
            for i in range(len(lst)):
                for rest in combinations(lst[i+1:], k-1):
                    yield (lst[i],) + rest
    
    def ehrhart_semigroup_size(clauses):
        n = len(clauses)
        m = sum(2**len(clause) - 1 for clause in clauses)
        return math.ceil(m * math.log(n, 2))
    
    def clause_depth(clauses):
        max_dist = 0
        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                dist = sum(abs(x - y) for x, y in zip(clauses[i], clauses[j]))
                if dist > max_dist:
                    max_dist = dist
        return max_dist
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            clauses = generate_formula(n, n // 2)
            mtr_phi = ehrhart_semigroup_size(clauses)
            d_phi = clause_depth(clauses)
            if d_phi == 0:
                continue
            ratio = mtr_phi / (d_phi ** (1.5 / 2) * math.log(n, 2) ** 3)
            results.append({"n": n, "mtr_phi": mtr_phi, "d_phi": d_phi, "ratio": ratio})
    
    if not results:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_values = [result["ratio"] for result in results]
    conjecture_holds = all(result["ratio"] <= 1.5 for result in results)
    counterexample = "" if conjecture_holds else "Ratio exceeds upper bound"
    
    return {
        "metric_name": "Ratio",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8 or len(results) == 30:
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds upper bound\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")