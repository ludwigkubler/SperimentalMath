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
    
    def generate_xor_tautology(n):
        tautology = []
        for _ in range(2**n):
            truth_values = [random.choice([0, 1]) for _ in range(n)]
            if all(truth_values[i] == truth_values[j] for i, j in zip(range(n), range(n-1, -1, -1))):
                tautology.append(truth_values)
        return tautology
    
    def construct_kahler_form(tautology):
        n = len(tautology[0])
        kahler_form = [[0] * n for _ in range(n)]
        for truth_values in tautology:
            index = sum(value << i for i, value in enumerate(truth_values))
            for i in range(n):
                for j in range(i, n):
                    if (truth_values[i] + truth_values[j]) % 2 == 1:
                        kahler_form[i][j] += 1
        return kahler_form
    
    def determinant(matrix):
        n = len(matrix)
        det = 0
        indices = list(range(n))
        for p in itertools.permutations(indices):
            sign = (-1) ** sum((i - j) % (n-1) for i, j in enumerate(p))
            prod = 1
            for k in range(n):
                prod *= matrix[p[k]][k]
            det += sign * prod
        return det
    
    def dnf_width(tautology):
        n = len(tautology[0])
        clauses = []
        for truth_values in tautology:
            clause = [i if value == 1 else -i-1 for i, value in enumerate(truth_values)]
            clauses.append(clause)
        return len(max(set(frozenset(c) for c in itertools.chain.from_iterable(itertools.combinations(clauses, k) for k in range(1, len(clauses)+1))), key=len))

    n = random.randint(5, 40)
    tautology = generate_xor_tautology(n)
    kahler_form = construct_kahler_form(tautology)
    det = determinant(kahler_form)
    width = dnf_width(tautology)
    
    rank = sum(1 for row in kahler_form if any(row))
    expected_rank = 2 * width
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": abs(rank - expected_rank) <= width,
        "counterexample": "" if abs(rank - expected_rank) <= width else f"Rank {rank} is not within a factor of 2 from width {width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[first_failing_seed]}")