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
    
    def generate_random_cnf(n):
        clauses = []
        for _ in range(random.randint(2, n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def p_adic_order(poly):
        order = 0
        for coeff in poly:
            if coeff != 0:
                order = max(order, len(bin(coeff)) - 2)
        return order
    
    def circuit_depth(cnf):
        # Simplified DPLL solver to estimate circuit depth
        stack = []
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        for lit in literals:
            if all(lit not in clause and -lit not in clause for clause in cnf):
                return 1
            stack.append((lit, 1))
        while stack:
            lit, depth = stack.pop()
            if lit > 0:
                for clause in cnf:
                    if lit in clause:
                        new_clause = [l for l in clause if l != lit]
                        if all(l not in new_clause and -l not in new_clause for l in literals):
                            return depth + 1
                        stack.append((-lit, depth + 1))
            else:
                for clause in cnf:
                    if -lit in clause:
                        new_clause = [l for l in clause if l != -lit]
                        if all(l not in new_clause and -l not in new_clause for l in literals):
                            return depth + 1
                        stack.append((lit, depth + 1))
        return float('inf')
    
    n = random.randint(5, 40)
    cnf = generate_random_cnf(n)
    negation_poly = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
    order = p_adic_order(negation_poly)
    depth = circuit_depth(cnf)
    
    return {
        "metric_name": "p-adic Order",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": order <= n * math.log2(n) * n ** (1/3),
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
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
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='falsified' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")