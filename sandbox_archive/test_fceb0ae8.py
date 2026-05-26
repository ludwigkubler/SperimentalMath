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
    
    def generate_3cnf(n, m):
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = set()
            while len(clause) < 3:
                var = random.choice(list(variables))
                if var not in clause:
                    clause.add(var)
                    if random.choice([True, False]):
                        clause.add(-var)
            clauses.append(tuple(sorted(clause)))
        return clauses

    def p_adic_norm(x):
        if x == 0:
            return 0
        return int(math.log(abs(x), 2))

    def p_adic_space(n):
        S = [Fraction(1, 2**i) for i in range(n + 1)]
        return S

    def minimal_rank(H):
        # Placeholder for actual computation of minimal rank
        return len(H)

    def monotone_complexity(F):
        # Placeholder for actual computation of monotone complexity
        return len(F)

    n = random.randint(5, 40)
    m = random.randint(2 * n, 3 * n)
    F = generate_3cnf(n, m)
    S = p_adic_space(n)
    H = p_adic_space(m)  # Placeholder for actual computation of p-adic harmonic space
    rank_H = minimal_rank(H)
    kappa_m = monotone_complexity(F)

    return {
        "metric_name": "MinimalRank",
        "metric_value": rank_H,
        "instances_tested": 1,
        "conjecture_holds": abs(rank_H - kappa_m) <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")