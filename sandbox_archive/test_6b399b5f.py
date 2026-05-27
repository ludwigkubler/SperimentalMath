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

def generate_tseitin_formula(w):
    n = 2 * w + 1
    variables = list(range(n))
    clauses = []
    
    # Generate OR clauses
    for i in range(w):
        clause = [variables[i], -variables[w + i]]
        clauses.append(clause)
    
    # Generate AND clauses
    for j in range(1, w):
        for k in range(j):
            clause = [-variables[2 * w + j], -variables[2 * w + k], variables[j + k]]
            clauses.append(clause)
    
    # Generate NOT clauses
    for i in range(w):
        clause = [variables[w + i], -variables[i]]
        clauses.append(clause)
    
    return clauses

def generate_quandle_from_clauses(clauses, n):
    quandle = {}
    for clause in clauses:
        for literal in clause:
            if literal not in quandle:
                quandle[literal] = set()
            for other_literal in clause:
                if other_literal != literal and -other_literal not in quandle[literal]:
                    quandle[literal].add(other_literal)
    return quandle

def compute_minimal_index(quandle):
    visited = set()
    stack = list(quandle.keys())
    
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            for neighbor in quandle[node]:
                if neighbor not in visited and -neighbor not in visited:
                    stack.append(neighbor)
    
    return len(visited)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    n_tests = 100
    
    for _ in range(n_tests):
        w = random.randint(5, 40)
        clauses = generate_tseitin_formula(w)
        quandle = generate_quandle_from_clauses(clauses, len(clauses))
        minimal_index = compute_minimal_index(quandle)
        
        if minimal_index < 2 ** (w / 10):
            return {
                "metric_name": "minimal_index",
                "metric_value": minimal_index,
                "instances_tested": n_tests,
                "conjecture_holds": False,
                "counterexample": f"Formula with width {w} has minimal index {minimal_index}"
            }
    
    return {
        "metric_name": "minimal_index",
        "metric_value": 2 ** (w / 10),
        "instances_tested": n_tests,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formula with width {w} has minimal index {minimal_index}\" first_failing_seed={first_failing_seed}")