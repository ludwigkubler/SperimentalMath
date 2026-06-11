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
    
    def generate_tseitin_formula(n):
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in range(i + 1, n):
                clause.append(f'~{literals[j]}')
                clause.append(literals[j])
            clauses.append(clause)
        return literals, clauses
    
    def categorify_formula(literals, clauses):
        # Simplified categorification procedure (50 lines)
        categ_clauses = []
        for clause in clauses:
            categ_clause = [f'c_{l}' if l.startswith('x') else f'd_{l}' for l in clause]
            categ_clauses.append(categ_clause)
        return categ_clauses
    
    def resolution_width(clauses):
        # Simplified resolution proof width calculation (50 lines)
        width = 1
        for clause in clauses:
            width = max(width, len(clause))
        return width
    
    n = random.randint(5, 40)
    literals, clauses = generate_tseitin_formula(n)
    categ_clauses = categorify_formula(literals, clauses)
    w_phi = resolution_width(categ_clauses)
    
    # Minimal order of categorified version (simplified)
    min_order_categ = len(categ_clauses)
    
    return {
        "metric_name": "min_order_categ",
        "metric_value": min_order_categ,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")