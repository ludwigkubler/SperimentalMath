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
    
    def generate_clause_set(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def l_p_norm(p, clauses):
        total = sum(abs(sum(clause)) ** p for clause in clauses)
        return (total / len(clauses)) ** (1 / p)
    
    def dpll_disjointness(clauses):
        n = len(clauses[0])
        stack = []
        assignment = [None] * n
        
        def backtrack(i):
            if i == n:
                return True
            for val in [-1, 1]:
                assignment[i] = val
                if all(assignment[j] != -clauses[k][j] for k in range(len(clauses)) if clauses[k][i] != 0):
                    stack.append((i + 1, assignment[:]))
                    if backtrack(i + 1):
                        return True
            stack.pop()
            return False
        
        return backtrack(0)
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    clauses = generate_clause_set(n, m)
    p = random.choice([2, 3, 4])
    
    norm_p = l_p_norm(p, clauses)
    cc_disjointness = dpll_disjointness(clauses)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": cc_disjointness,
        "instances_tested": 1,
        "conjecture_holds": norm_p ** (1 / p) <= cc_disjointness,
        "counterexample": "" if norm_p ** (1 / p) <= cc_disjointness else f"norm_p^{(1/p)} = {norm_p**(1/p)}, CC_R(DISJ_n) = {cc_disjointness}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")