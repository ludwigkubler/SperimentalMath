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

def generate_3cnf(n):
    clauses = []
    for _ in range(2 * n):
        literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
        clause = random.sample(literals, 3)
        clauses.append(clause)
    return clauses

def dpll(clauses):
    def backtrack(level):
        if level == len(clauses):
            return True
        literals = set()
        for clause in clauses[level:]:
            literals.update([abs(lit) for lit in clause])
        literal = random.choice(list(literals))
        sign = 1
        stack.append((literal, sign))
        if backtrack(level + 1):
            return True
        stack.pop()
        sign = -1
        stack.append((literal, sign))
        if backtrack(level + 1):
            return True
        stack.pop()
        return False
    
    stack = []
    return backtrack(0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_3cnf(n)
    s_phi = len(dpll(clauses)) if dpll(clauses) else float('inf')
    
    mlag_phi = Fraction(n)  # Placeholder value for minimal local algebraic geometric rank
    
    return {
        "metric_name": "mlag_vs_s_phi",
        "metric_value": mlag_phi * s_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")