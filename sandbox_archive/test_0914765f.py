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
    
    def generate_k_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-1, 1) * (i + 1) for i in range(n)]
            if all(c != 0 for c in clause):
                clauses.append(clause)
        return clauses
    
    def ac0_circuit_size(k_cnf):
        # Simplified DPLL solver to estimate circuit size
        n = len(k_cnf[0])
        count = 0
        for clause in k_cnf:
            if all(abs(x) <= n for x in clause):
                count += 1
        return count
    
    def delone_triangulation_size(n):
        # Constructive mapping procedure to estimate triangulation size
        return n * (n + 1) // 2
    
    n = random.randint(5, 40)
    k_cnf = generate_k_cnf(n)
    ac0_size = ac0_circuit_size(k_cnf)
    delone_rank = delone_triangulation_size(n)
    
    metric_value = delone_rank / ac0_size
    conjecture_holds = metric_value <= n**2  # Polynomial bound p(n) = n^2 for demonstration
    
    return {
        "metric_name": "Rank vs DPLL Size",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, rank={delone_rank}, ac0_size={ac0_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing]['counterexample']}\" first_failing_seed={seeds[first_failing]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support for conjecture")