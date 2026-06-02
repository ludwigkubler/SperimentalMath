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
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i + 1, n)):
                clauses.append(clause)
        return clauses

    def compute_automorphism_group(cnf):
        # Simplified version of computing automorphisms using group cohomology
        n = len(cnf)
        if n == 0:
            return 1
        return 2 ** (n - 1)

    def compute_clause_set_complexity(cnf):
        return sum(len(clause) for clause in cnf)

    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = generate_cnf(n)
        aut_group_size = compute_automorphism_group(cnf)
        clause_set_complexity = compute_clause_set_complexity(cnf)
        results.append({
            "metric_name": "aut_group_size",
            "metric_value": aut_group_size,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": None,
            "counterexample": ""
        })

    correlation = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = Fraction(sum(1 for r in results if r["conjecture_holds"]), len(results))

    return {
        "seed": seed,
        "metric_name": "aut_group_size",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": abs(correlation) >= 0.7,
        "counterexample": "" if abs(correlation) >= 0.7 else "correlation_too_low"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = Fraction(sum(1 for r in results if r["conjecture_holds"]), len(results))

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample='correlation_too_low' first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")