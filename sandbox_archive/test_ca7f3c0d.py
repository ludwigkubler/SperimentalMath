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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def dpll(cnf):
        if not cnf:
            return True
        literal = next((l for l in set([abs(l) for c in cnf for l in c]) if all(l not in clause and -l not in clause for clause in cnf)), None)
        if literal is None:
            return False
        def dpll_helper(cnf, assignment):
            if not cnf:
                return True
            for i, clause in enumerate(cnf):
                if any(l in assignment for l in clause) and all(-l not in assignment for l in clause):
                    continue
                new_cnf = [c for j, c in enumerate(cnf) if j != i]
                if literal > 0:
                    new_assignment = assignment | {literal}
                else:
                    new_assignment = assignment | {-literal}
                if dpll_helper(new_cnf, new_assignment):
                    return True
            return False
        return dpll_helper(cnf, set())

    def delone_triangulation_size(n):
        # Placeholder for Delone triangulation size calculation
        return n * (n + 1) // 2

    def ac0_circuit_size(cnf):
        return len(cnf)

    n = random.randint(5, 40)
    k = random.randint(1, min(3, n))
    cnf = generate_kcnf(n, k)
    dpll_size = dpll(cnf)
    triangulation_size = delone_triangulation_size(n)
    
    if dpll_size == 0:
        return {
            "metric_name": "Rank vs DPLL Size",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "AC0 circuit size is zero, cannot compute ratio"
        }
    
    ratio = triangulation_size / dpll_size
    return {
        "metric_name": "Rank vs DPLL Size",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True if ratio <= n**2 else False,  # Placeholder polynomial bound
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [random.randint(100, 997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "Ratio exceeds polynomial bound"
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)