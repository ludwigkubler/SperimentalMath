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

def generate_cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), random.randint(1, n))]
        clauses.append(clause)
    return clauses

def symplectic_quotient_order(clauses):
    n = len(clauses[0])
    vectors = []
    for clause in clauses:
        vector = [0] * (2 * n)
        for literal in clause:
            var = abs(literal) - 1
            if literal > 0:
                vector[var] += 1
            else:
                vector[n + var] += 1
        vectors.append(vector)
    order = 0
    for i in range(n):
        for j in range(i + 1, n):
            if all(vectors[i][k] == vectors[j][k] for k in range(2 * n)):
                order += 1
    return order

def resolution_proof_width(clauses):
    stack = clauses[:]
    while True:
        new_clause = None
        for i in range(len(stack)):
            for j in range(i + 1, len(stack)):
                c1 = stack[i]
                c2 = stack[j]
                for literal in c1:
                    if -literal in c2:
                        new_clause = [l for l in c1 if l != literal] + [l for l in c2 if l != -literal]
                        break
                if new_clause:
                    break
            if new_clause:
                break
        if not new_clause:
            return len(stack)
        stack.append(new_clause)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        m = 2 * n
        clauses = generate_cnf(n, m)
        order = symplectic_quotient_order(clauses)
        width = resolution_proof_width(clauses)
        results.append((order, width))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    orders = [r[0] for r in results]
    widths = [r[1] for r in results]
    mean_order = sum(orders) / len(orders)
    mean_width = sum(widths) / len(widths)
    correlation = 0
    if len(orders) > 1:
        numerator = sum((orders[i] - mean_order) * (widths[i] - mean_width) for i in range(len(orders)))
        denominator = math.sqrt(sum((orders[i] - mean_order) ** 2 for i in range(len(orders))) * sum((widths[i] - mean_width) ** 2 for i in range(len(widths))))
        correlation = numerator / denominator
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and all(c >= 0.5 for c in [correlation] * 30),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 8)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")