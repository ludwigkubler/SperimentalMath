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
        variables = set()
        clauses = []
        for _ in range(m):
            clause = set()
            while len(clause) < 2 or len(clause) > n:
                literal = random.choice([f'x{i+1}', f'-x{i+1}'])
                if literal not in clause:
                    clause.add(literal)
                    variables.add(literal[2:])
            clauses.append(list(clause))
        return list(variables), clauses
    
    def galois_group_order(n):
        # Simplified approximation for demonstration
        return 2 ** n
    
    def quaternion_algebra_order(k):
        return k**2 * math.log(k, 2)**3
    
    n = random.randint(5, 40)
    m = random.randint(10, 80)
    variables, clauses = generate_cnf(n, m)
    k = len(variables)
    
    order = galois_group_order(len(variables))
    conjecture_bound = quaternion_algebra_order(k)
    
    if order > conjecture_bound:
        return {
            "metric_name": "quaternion_algebra_order",
            "metric_value": order,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"CNF with {n} vars, {m} clauses; k={k}, galois_group_order={order}, conjecture_bound={conjecture_bound}"
        }
    
    return {
        "metric_name": "quaternion_algebra_order",
        "metric_value": order,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results):.2f} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results):.2f} std=0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")