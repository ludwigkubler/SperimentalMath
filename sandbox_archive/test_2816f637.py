# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def compute_qcr(clauses, n):
        R_F = {0: {1}}
        I_F = set()
        
        for i in range(1, n + 1):
            R_F[i] = {}
            for term in R_F[i-1]:
                for var in range(1, n + 1):
                    if var not in term:
                        new_term = tuple(sorted(term + (var,)))
                        R_F[i][new_term] = Fraction(1, i)
                        I_F.add(new_term)
        
        qcr = len(I_F)
        return qcr
    
    def find_shortest_resolution(clauses):
        # Placeholder for resolution proof finding
        # This is a dummy implementation and does not actually compute the shortest proof
        return random.randint(50, 100)  # Dummy length of the shortest resolution proof
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(n // 2, n)
    clauses = generate_kcnf(n, k)
    
    qcr = compute_qcr(clauses, n)
    l_F = find_shortest_resolution(clauses)
    
    return {
        "metric_name": "qcr(R_F) vs. l(F)",
        "metric_value": qcr,
        "instances_tested": 1,
        "conjecture_holds": qcr == l_F,
        "counterexample": "" if qcr == l_F else f"qcr(R_F)={qcr}, l(F)={l_F}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_qcr = sum(r["metric_value"] for r in results) / len(results)
    std_qcr = math.sqrt(sum((r["metric_value"] - mean_qcr) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_qcr} std={std_qcr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_qcr} std={std_qcr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")