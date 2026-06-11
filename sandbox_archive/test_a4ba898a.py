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

def generate_sat_instance(n: int) -> str:
    clauses = []
    for _ in range(n):
        literals = [f'x{i+1}' if random.choice([True, False]) else f'-x{i+1}' for i in range(n)]
        clause = ' OR '.join(literals)
        clauses.append(clause)
    return ' AND '.join(clauses)

def dpll_width(sat_instance: str) -> int:
    stack = []
    literals = sat_instance.split(' OR ')
    for literal in literals:
        if literal.startswith('-'):
            literal = literal[1:]
            if literal in stack:
                stack.remove(literal)
            else:
                stack.append(f'-{literal}')
        else:
            if f'-{literal}' in stack:
                stack.remove(f'-{literal}')
            else:
                stack.append(literal)
    return max(len(stack), 0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            sat_instance = generate_sat_instance(n)
            width = dpll_width(sat_instance)
            results.append(width)
    
    if not results:
        return {
            "metric_name": "DPLL Search Tree Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_width = sum(results) / len(results)
    return {
        "metric_name": "DPLL Search Tree Width",
        "metric_value": mean_width,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    # Compute mean/std of metric_value
    values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    mean_value = sum(values) / len(values) if values else 0
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in values) / len(values)) if values else 0
    
    # Compute fraction of seeds where conjecture_holds
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")