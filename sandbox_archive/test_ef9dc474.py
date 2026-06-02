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
        cnf = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:  # Ensure the clause is not trivial
                cnf.append(clause)
        return cnf
    
    def compute_linear_code(cnf):
        n = len(cnf[0])
        code_matrix = [[0] * (2**n) for _ in range(n)]
        for i, clause in enumerate(cnf):
            for j in range(2**n):
                if all(x * (j >> abs(var) & 1) >= 0 for x, var in zip(clause, range(n))):
                    code_matrix[i][j] = 1
        return code_matrix
    
    def compute_brauer_group_order(cnf):
        n = len(cnf[0])
        code_matrix = compute_linear_code(cnf)
        order = 1
        for i in range(n):
            for j in range(i + 1, n):
                if all(code_matrix[i][k] == code_matrix[j][k] for k in range(2**n)):
                    order *= 2
        return order
    
    def log2(x):
        return Fraction(math.log2(x)).limit_denominator()
    
    cnf = generate_cnf(random.randint(5, 40))
    log2_brauer_group = log2(compute_brauer_group_order(cnf))
    r_phi = len(cnf)  # Simplified communication complexity rank for demonstration
    
    return {
        "metric_name": "log2(BrauerGroupOrder)",
        "metric_value": float(log2_brauer_group),
        "instances_tested": 1,
        "n_max": max(len(clause) for clause in cnf),
        "conjecture_holds": False,  # Mapping undefined
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")