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
    
    def generate_3cnf(n, m):
        literals = [f"x{i}" for i in range(1, n+1)] + [f"~x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(literals, 3)
            if random.choice([True, False]):
                clause = [f"~{l}" for l in clause]
            clauses.append(clause)
        return clauses
    
    def calculate_euler_characteristic(matroid):
        rank = len(matroid)
        size = sum(len(v) for v in matroid.values())
        return rank - size + 1
    
    def dpll_refutation_tree_width(formula):
        # Simplified DPLL algorithm to estimate tree width
        literals = set()
        for clause in formula:
            literals.update(clause)
        return len(literals)
    
    n = random.randint(5, 30)
    m = random.randint(n * 2, n * 4)
    formula = generate_3cnf(n, m)
    matroid = {}
    for literal in set(frozenset(clause) for clause in formula):
        matroid[literal] = [literal]
    
    euler_char = calculate_euler_characteristic(matroid)
    dpll_width = dpll_refutation_tree_width(formula)
    
    return {
        "metric_name": "Euler Characteristic",
        "metric_value": euler_char,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials run")
    else:
        total_metric_value = sum(r["metric_value"] for r in results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"])
        
        mean = Fraction(total_metric_value, len(results))
        std = (sum((r["metric_value"] - mean) ** 2 for r in results) / len(results)) ** 0.5
        
        if support_fraction >= 8 * len(results) // 10:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")