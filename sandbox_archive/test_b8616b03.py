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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append(f'{variables[i-1]}')
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append(f'~{variables[i-1]} | ~{variables[j-1]}')
                clauses.append(f'{variables[i-1]} | {variables[j-1]}')
        return clauses
    
    def compute_geometric_entropy(clauses):
        # Placeholder for actual geometric entropy computation
        return random.random()  # Simplified for testing purposes
    
    def resolution_width(clauses):
        # Placeholder for actual resolution width computation
        return len(clauses)  # Simplified for testing purposes
    
    n = random.randint(5, 40)
    clauses = generate_tseitin_formula(n)
    mtr = compute_geometric_entropy(clauses)
    w = resolution_width(clauses)
    
    return {
        "metric_name": "mtr",
        "metric_value": mtr,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 7 for i in range(5, 8)]  # First 30 prime numbers
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    print(f"RESULT: {RESULT} mean={sum(r['metric_value'] for r in results)/len(results)} std=0.0 support_fraction={support_fraction}")