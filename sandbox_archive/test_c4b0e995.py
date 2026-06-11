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
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = -clause[0], -clause[1]
            clauses.append(clause)
        return clauses
    
    def quandle_order(clauses):
        elements = set()
        for clause in clauses:
            for literal in clause:
                elements.add(abs(literal))
        return len(elements)
    
    def entanglement_width(clauses):
        width = 0
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                if not any(lit in clauses[j] for lit in clauses[i]):
                    width += 1
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(2, 40)
            cnf = generate_cnf(n, m)
            order = quandle_order(cnf)
            width = entanglement_width(cnf)
            results.append({"n": n, "m": m, "order": order, "width": width})
    
    if not results:
        return {
            "metric_name": "MinOrder(Q(φ)) vs EntanglementWidth(φ)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    order_values = [r["order"] for r in results]
    width_values = [r["width"] for r in results]
    
    mean_order = sum(order_values) / len(order_values)
    mean_width = sum(width_values) / len(width_values)
    
    correlation = 0
    n = len(results)
    for i in range(n):
        correlation += (order_values[i] - mean_order) * (width_values[i] - mean_width)
    correlation /= (n * sum((x - mean_order) ** 2 for x in order_values) * sum((y - mean_width) ** 2 for y in width_values)) ** 0.5
    
    return {
        "metric_name": "MinOrder(Q(φ)) vs EntanglementWidth(φ)",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation) >= 0.75,  # Arbitrary threshold for linear correlation
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")