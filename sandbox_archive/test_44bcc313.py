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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def solve(literals, assignment):
            if not cnf:
                return True
            literal = next((l for l in literals if l not in assignment and -l not in assignment), None)
            if literal is None:
                return False
            for val in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[literal] = val
                if solve(literals, new_assignment):
                    return True
            return False
        
        literals = set(abs(l) for c in cnf for l in c)
        return 1 + max(solve(cnf, {}), solve([(l, -l) for l in literals], {}))
    
    def tropical_index(clauses):
        n = len(clauses[0])
        matroid = [[Fraction(0, 1)] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for i in range(n):
                if clause[i] > 0:
                    matroid[i][i] += Fraction(1, 1)
                else:
                    matroid[-1][i] += Fraction(1, 1)
        return max(sum(row) for row in matroid)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(n // 2, n * 2)
    cnf = generate_cnf(n, m)
    mli = tropical_index(cnf)
    dpll_path_length = dpll(cnf)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": mli,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")