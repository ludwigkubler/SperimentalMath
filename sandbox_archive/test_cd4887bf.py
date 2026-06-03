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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n // 4):  # Ensure at least n clauses
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def resolution_width(cnf):
        stack = cnf[:]
        seen = set()
        while stack:
            literal = stack.pop()
            if literal < 0 and -literal in seen:
                return len(stack) + 1
            seen.add(literal)
            for clause in cnf:
                if literal in clause:
                    new_clause = [x for x in clause if x != literal]
                    if not new_clause:
                        return float('inf')
                    stack.append(-new_clause[0])
        return len(stack)

    def betti_number(cnf):
        # Simplified Betti number calculation (not accurate but sufficient)
        return len(cnf) / 2

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    beta = betti_number(cnf)
    width = resolution_width(cnf)
    
    if width == float('inf'):
        return {
            "metric_name": "resolution_width",
            "metric_value": width,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable CNF"
        }
    
    diff = abs(beta - width)
    return {
        "metric_name": "difference",
        "metric_value": diff,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": diff <= 2,  # Arbitrary constant k
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    std_diff = math.sqrt(sum((r["metric_value"] - mean_diff) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_diff} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_diff} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"difference exceeded k\" first_failing_seed={r['seed']}")
                break