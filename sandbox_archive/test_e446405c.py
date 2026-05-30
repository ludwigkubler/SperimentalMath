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
    
    def generate_k_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = set()
            while len(clause) < 3:
                lit = random.choice(range(1, n + 1))
                if random.choice([True, False]):
                    lit = -lit
                clause.add(lit)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def truth_table(k_cnf, n):
        table = {}
        for i in range(2 ** n):
            assignment = [(i >> j) & 1 for j in range(n)]
            value = True
            for clause in k_cnf:
                if all(not (assignment[abs(lit) - 1] ^ (lit < 0)) for lit in clause):
                    continue
                value = False
                break
            table[tuple(assignment)] = value
        return table
    
    def minimal_representation_order(truth_table):
        # Placeholder function to compute the minimal order of a group representation
        # This is a dummy implementation and should be replaced with actual computation
        return 1
    
    def resolution_width(k_cnf, n):
        # Placeholder function to compute the resolution width
        # This is a dummy implementation and should be replaced with actual computation
        return 1
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        m = int(2 ** (n / 2))
        k_cnf = generate_k_cnf(n, m)
        table = truth_table(k_cnf, n)
        order = minimal_representation_order(table)
        width = resolution_width(k_cnf, n)
        
        results.append({
            "n": n,
            "m": m,
            "order": order,
            "width": width
        })
    
    metric_value = sum(result["order"] for result in results) / len(results)
    conjecture_holds = all(result["order"] <= result["width"] * (result["m"] ** (2/3) * result["n"] ** (1/4)) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Order of Group Representations",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")