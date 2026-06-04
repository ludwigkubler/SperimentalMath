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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for i in range(1, n + 1):
            clause = [random.choice([-1, 1]) * j for j in range(1, n + 1)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        stack = cnf[:]
        visited = set()
        while stack:
            clause = stack.pop()
            if not any(abs(lit) in visited for lit in clause):
                visited.update(abs(lit) for lit in clause)
                new_clauses = []
                for c in stack:
                    if any(abs(lit) == abs(clause[0]) and lit != clause[0] for lit in c):
                        new_clause = [l for l in c if abs(l) != abs(clause[0])]
                        if new_clause not in new_clauses:
                            new_clauses.append(new_clause)
                stack.extend(new_clauses)
        return len(visited)
    
    def brauer_group_index(cnf):
        n = len(cnf)
        dual_basis = [[i + 1, -i - 1] for i in range(n)]
        ring = {}
        for i in range(n):
            for j in range(n):
                if i != j:
                    ring[(dual_basis[i][0], dual_basis[j][0])] = (dual_basis[i][1], dual_basis[j][1])
        index = 1
        for key, value in ring.items():
            if key[0] == value[1]:
                index *= -1
        return abs(index)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_index = 0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            width = resolution_width(cnf)
            index = brauer_group_index(cnf)
            if width == 0 or index == 0:
                continue
            instances_tested += 1
            total_index += index
            max_n = max(max_n, n)
    
    mean_index = Fraction(total_index, instances_tested) if instances_tested > 0 else 0
    
    conjecture_holds = all(mean_index <= (1 + epsilon) * width for width in [resolution_width(generate_cnf(n)) for n in n_values])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Brauer Group Index",
        "metric_value": float(mean_index),
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")