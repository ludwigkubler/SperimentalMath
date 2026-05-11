# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def run_trial(seed: int) -> dict:
    def generate_random_formula(n, c):
        clauses = []
        for _ in range(c):
            clause = [random.randint(1, n), random.randint(1, n), random.randint(1, n)]
            while len(set(clause)) != 3:
                clause = [random.randint(1, n), random.randint(1, n), random.randint(1, n)]
            clauses.append(tuple(sorted(clause)))
        return clauses

    def is_disjoint(S):
        for i in range(len(S)):
            for j in range(i + 1, len(S)):
                if set(S[i]) & set(S[j]):
                    return False
        return True

    def matroid_rank(clauses):
        rank = 0
        for k in range(1, len(clauses) + 1):
            for S in combinations(clauses, k):
                if is_disjoint(S):
                    rank = max(rank, k)
        return rank

    n = random.randint(5, 40)
    c = int(n ** 2.3)  # Ensure circuit size ≤ n^c
    formula = generate_random_formula(n, c)

    matroid_ranks = [matroid_rank(formula) for _ in range(50)]
    avg_rank = sum(matroid_ranks) / len(matroid_ranks)
    support_fraction = sum(1 for r in matroid_ranks if r <= 5 * math.log(n)) / len(matroid_ranks)

    return {
        "metric_name": "matroid_rank",
        "metric_value": avg_rank,
        "instances_tested": len(matroid_ranks),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []

    for seed in seeds:
        random.seed(seed)
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    avg_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=??? support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[0]}")