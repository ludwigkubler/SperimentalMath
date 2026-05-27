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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return [row[:n-1] for row in A]

    def rank(A):
        return len(gaussian_elimination(A))

    def random_dnf_formula(n, k):
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(k):
            clause = random.sample(variables, 2)
            clause.append(random.choice([-1, 1]))
            clauses.append(clause)
        return clauses

    def tropical_grothendieck_witt_class(dnf_formula):
        n = len(dnf_formula[0]) - 1
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in dnf_formula:
            for i in range(1, n+1):
                if i in clause:
                    A[i][i] += 1
                else:
                    A[i][i] -= 1
        return rank(A)

    def min_rank(dnf_formula):
        return min(tropical_grothendieck_witt_class(clause) for clause in dnf_formula)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = random.randint(1, n)
        dnf_formula = random_dnf_formula(n, k)
        min_rank_value = min_rank(dnf_formula)
        results.append({
            "n": n,
            "k": k,
            "min_rank": min_rank_value
        })

    mean_min_rank = sum(result["min_rank"] for result in results) / len(results)
    conjecture_holds = all(result["min_rank"] >= math.sqrt(n) for result in results)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_min_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "n={n}, k={k}, min_rank={min_rank}".format(**results[0])
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print("TRIAL: {seed} {trial_result}".format(seed=seed, trial_result=trial_result))
        results.append(trial_result)

    mean_min_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print("RESULT: SUPPORTED mean={mean} std=0.0 support_fraction={support}".format(
            mean=mean_min_rank, support=support_fraction
        ))
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"n={n}, k={k}, min_rank={min_rank}\" first_failing_seed={first_failing_seed}".format(
            n=results[0]["n"], k=results[0]["k"], min_rank=results[0]["min_rank"], first_failing_seed=first_failing_seed
        ))
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")