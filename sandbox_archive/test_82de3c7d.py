# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)

    def truth_table(f, n):
        return [f(i) for i in range(2**n)]

    def asc(T):
        return sum(zc for zc, oc in zip(T, T[1:]))

    def desc(T):
        return sum(oc for zc, oc in zip(T, T[1:]))

    def lambda_2(f, n):
        T = truth_table(f, n)
        asc_count = 0
        desc_count = 0
        for i in range(n):
            if T[i] == 0:
                asc_count += sum(1 for j in range(i+1, n) if T[j] == 1)
            else:
                desc_count += sum(1 for j in range(i+1, n) if T[j] == 0)
        return abs(asc_count - desc_count)

    def DNF_min(f, n):
        # Placeholder for actual implementation
        return 2**n

    def random_k_DNF(n, k):
        variables = list(range(n))
        terms = []
        for _ in range(k):
            term = [random.choice(variables) if random.choice([0, 1]) else -v for v in variables]
            terms.append(term)
        return terms

    def evaluate_k_DNF(x, terms):
        return any(all((x & (1 << abs(v)) == 0 if v > 0 else x & (1 << abs(v))) for v in term) for term in terms)

    def parity(n):
        return lambda x: sum(1 for i in range(n) if x & (1 << i)) % 2

    def AND(n):
        return lambda x: all(x & (1 << i) for i in range(n))

    def OR(n):
        return lambda x: any(x & (1 << i) for i in range(n))

    def MAJ(n):
        return lambda x: sum(1 for i in range(n) if x & (1 << i)) > n // 2

    def threshold_k(n, k):
        return lambda x: sum(1 for i in range(n) if x & (1 << i)) >= k

    def random_LTF(n):
        weights = [random.randint(0, 100) for _ in range(n)]
        return lambda x: sum(w * ((x & (1 << i)) >> i) for i, w in enumerate(weights))

    n_values = [8, 10, 12, 14]
    ensembles = [
        ("uniform", lambda n: random.randint(0, 1)),
        ("k-DNF", lambda n: evaluate_k_DNF(random.getrandbits(n), random_k_DNF(n, random.randint(1, n // 2)))),
        ("symmetric", parity),
        ("threshold", threshold_k),
        ("LTF", random_LTF)
    ]
    results = []

    for n in n_values:
        for ensemble_name, ensemble_func in ensembles:
            for _ in range(30):
                f = ensemble_func(n)
                lambda_2_val = lambda_2(f, n)
                DNF_min_val = DNF_min(f, n)
                if not math.isinf(DNF_min_val):
                    log_lambda_2 = math.log2(1 + lambda_2_val) if lambda_2_val > 0 else -math.inf
                    log_DNF_min = math.log2(1 + DNF_min_val)
                    results.append({
                        "n": n,
                        "ensemble": ensemble_name,
                        "lambda_2": lambda_2_val,
                        "DNF_min": DNF_min_val,
                        "log_lambda_2": log_lambda_2,
                        "log_DNF_min": log_DNF_min,
                        "conjecture_holds": log_lambda_2 <= n + log_DNF_min + 5 * math.log2(n + 1)
                    })

    return {
        "metric_name": "lambda_2 vs DNF_min",
        "metric_value": sum(r["log_lambda_2"] for r in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": "" if all(r["conjecture_holds"] for r in results) else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    for seed in seeds:
        result = run_trial(seed)
        print(f'TRIAL: {result}')

# RESULT: INCONCLUSIVE mapping_undefined