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
    variables = list(range(1, 2 * w + 1))
    clauses = []
    
    for j in range(w):
        for k in range(j + 1, w):
            clause = [-variables[2 * w + j], -variables[2 * w + k], variables[j + k]]
            clauses.append(clause)
    
    return clauses

def generate_quandle_from_clauses(clauses):
    quandle = {}
    for clause in clauses:
        for literal in clause:
            if abs(literal) not in quandle:
                quandle[abs(literal)] = set()
            quandle[abs(literal)].add(literal)
    
    return quandle

def minimal_index_of_quandle_action(quandle):
    if not quandle:
        return 0
    
    elements = list(quandle.keys())
    n = len(elements)
    index = 1
    
    while True:
        generated_elements = set()
        for element in elements:
            new_elements = {quandle[element][i] % n for i in range(n)}
            if not new_elements.issubset(generated_elements):
                generated_elements.update(new_elements)
                index += 1
            else:
                break
        
        if len(generated_elements) == n:
            return index

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    w_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for w in w_values:
        clauses = generate_tseitin_formula(w)
        quandle = generate_quandle_from_clauses(clauses)
        index = minimal_index_of_quandle_action(quandle)
        
        results.append({
            "w": w,
            "index": index
        })
    
    metric_value = sum(result["index"] for result in results) / len(results)
    conjecture_holds = all(result["index"] >= 2 ** (math.ceil(math.log2(w))) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Index of Quandle Action",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")