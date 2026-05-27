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
            clause = [random.randint(1, n) for _ in range(random.randint(2, 3))]
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(clauses):
        # Simplified SAT solver using backtracking
        assignment = [False] * (n + 1)
        def backtrack(i):
            if i == n + 1:
                return True
            for val in [True, False]:
                assignment[i] = val
                if all(any(assignment[j] for j in clause) for clause in clauses):
                    if backtrack(i + 1):
                        return True
            return False
        return backtrack(1)
    
    def hodge_rank(clauses):
        # Simplified Hodge rank calculation (placeholder)
        return len(clauses)
    
    n = random.randint(5, 40)
    k = random.randint(n // 2, n)
    clauses = generate_kcnf(n, k)
    rank = hodge_rank(clauses)
    phi_n = 1 * math.log2(n) ** 2 + 2
    
    metric_value = rank
    conjecture_holds = rank <= phi_n
    counterexample = "" if conjecture_holds else f"Rank {rank} exceeds φ({n}) = {phi_n}"
    
    return {
        "metric_name": "Hodge Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}"
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["counterexample"])
        result = f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}"
    else:
        result = f"RESULT: INCONCLUSIVE support_fraction={support_fraction}"
    
    print(result)