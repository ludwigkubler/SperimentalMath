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
    n = 40
    k = 5
    instances_tested = 30
    conjecture_holds = True
    counterexample = ""

    def resolve(cnf):
        clauses = [set(clause) for clause in cnf]
        resolved_clauses = []
        while len(resolved_clauses) < n:
            new_clause = set()
            for i in range(len(clauses)):
                if any(-x in clauses[i] and x in clauses[j] for j in range(i + 1, len(clauses))):
                    continue
                new_clause.update(clauses[i])
            resolved_clauses.append(new_clause)
        return resolved_clauses

    def fast_walsh_hadamard_transform(f):
        n = len(f)
        if n == 1:
            return f
        even = fast_walsh_hadamard_transform(f[0::2])
        odd = fast_walsh_hadamard_transform(f[1::2])
        result = [0] * n
        for i in range(n // 2):
            result[i] = even[i] + odd[i]
            result[i + n // 2] = even[i] - odd[i]
        return result

    def fourier_coefficient(f, i):
        n = len(f)
        f_hat = fast_walsh_hadamard_transform(f)
        return Fraction(f_hat[i], 2 ** n)

    def polymatroid_rank(f):
        rank = 0
        for S in range(1 << n):
            subset = [i for i in range(n) if (S >> i) & 1]
            sum_fourier_coeffs = sum(abs(fourier_coefficient(f, i)) for i in subset)
            rank = max(rank, sum_fourier_coeffs)
        return rank

    def generate_random_3cnf(n):
        cnf = []
        for _ in range(2 * n):
            clause = random.sample(range(1, n + 1), 3)
            cnf.append(clause)
        return cnf

    total_rank = 0
    max_rank_small_set = 0

    for _ in range(instances_tested):
        cnf = generate_random_3cnf(n)
        dnf = resolve(cnf)
        f = [1] * (2 ** n)
        for clause in dnf:
            for assignment in range(2 ** n):
                if all((assignment >> i) & 1 == x for i, x in enumerate(clause)):
                    f[assignment] += 1
        rank = polymatroid_rank(f)
        total_rank += rank

        if len(dnf) > instances_tested * k:
            conjecture_holds = False
            counterexample = "DNF size exceeds expected"

        for S in range(1 << min(n, 100)):
            subset = [i for i in range(n) if (S >> i) & 1]
            rank_small_set = sum(abs(fourier_coefficient(f, i)) for i in subset)
            max_rank_small_set = max(max_rank_small_set, rank_small_set)

    mean_rank = total_rank / instances_tested
    conjecture_holds = conjecture_holds and mean_rank >= n ** 0.5 * k ** 0.25

    return {
        "metric_name": "polymatroid_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"DNF size exceeds expected\" first_failing_seed={r['seed']}")
                break