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

def generate_bp(n, is_read_twice):
    bp = []
    for _ in range(n):
        if not bp:
            bp.append(random.choice([0, 1]))
        else:
            if is_read_twice:
                bp.append(bp[-1])
            else:
                bp.append(1 - bp[-1])
    return bp

def tensor_product(bp1, bp2):
    n = len(bp1)
    m = len(bp2)
    result = [[0] * (m * n) for _ in range(n * m)]
    for i in range(n):
        for j in range(m):
            for k in range(n):
                for l in range(m):
                    result[i * m + k][j * n + l] = bp1[i] * bp2[j]
    return result

def gaussian_elimination(M):
    rows, cols = len(M), len(M[0])
    rank = 0
    for j in range(cols):
        i_max = -1
        for i in range(rank, rows):
            if M[i][j]:
                i_max = i
                break
        if i_max == -1:
            continue
        M[rank], M[i_max] = M[i_max], M[rank]
        for k in range(j + 1, cols):
            M[rank][k] /= M[rank][j]
        for i in range(rows):
            if i != rank and M[i][j]:
                for k in range(j + 1, cols):
                    M[i][k] -= M[rank][k] * M[i][j]
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20
    read_once_bp = generate_bp(n, False)
    read_twice_bp = generate_bp(n, True)

    M_read_once = tensor_product(read_once_bp, read_once_bp)
    M_read_twice = tensor_product(read_twice_bp, read_twice_bp)

    rank_read_once = gaussian_elimination(M_read_once)
    rank_read_twice = gaussian_elimination(M_read_twice)

    metric_value_read_once = Fraction(rank_read_once, n)
    metric_value_read_twice = Fraction(rank_read_twice, n)

    conjecture_holds_read_once = metric_value_read_once >= Fraction(1, 2) * math.log(n, 2)
    conjecture_holds_read_twice = metric_value_read_twice <= Fraction(1, 4) * math.log(n, 2)

    return {
        "metric_name": "noncommutative_rank",
        "metric_value_read_once": metric_value_read_once,
        "metric_value_read_twice": metric_value_read_twice,
        "instances_tested": n,
        "conjecture_holds_read_once": conjecture_holds_read_once,
        "counterexample_read_once": "" if conjecture_holds_read_once else f"Read-once BP with rank {rank_read_once}",
        "conjecture_holds_read_twice": conjecture_holds_read_twice,
        "counterexample_read_twice": "" if conjecture_holds_read_twice else f"Read-twice BP with rank {rank_read_twice}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_value_read_once\": {result['metric_value_read_once']}, \"metric_value_read_twice\": {result['metric_value_read_twice']}, \"conjecture_holds_read_once\": {result['conjecture_holds_read_once']}, \"counterexample_read_once\": \"{result['counterexample_read_once']}\", \"conjecture_holds_read_twice\": {result['conjecture_holds_read_twice']}, \"counterexample_read_twice\": \"{result['counterexample_read_twice']}\"}}")

        if not result["conjecture_holds_read_once"] or not result["conjecture_holds_read_twice"]:
            results.append(result)

    mean_read_once = sum(r["metric_value_read_once"] for r in results) / len(results)
    std_read_once = math.sqrt(sum((r["metric_value_read_once"] - mean_read_once) ** 2 for r in results) / len(results))
    support_fraction_read_once = sum(1 for r in results if r["conjecture_holds_read_once"]) / len(results)

    mean_read_twice = sum(r["metric_value_read_twice"] for r in results) / len(results)
    std_read_twice = math.sqrt(sum((r["metric_value_read_twice"] - mean_read_twice) ** 2 for r in results) / len(results))
    support_fraction_read_twice = sum(1 for r in results if r["conjecture_holds_read_twice"]) / len(results)

    if support_fraction_read_once >= 0.8 and support_fraction_read_twice >= 0.8:
        print(f"RESULT: SUPPORTED mean_read_once={mean_read_once} std_read_once={std_read_once} support_fraction_read_once={support_fraction_read_once}")
    elif any(not r["conjecture_holds_read_once"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds_read_once"])
        print(f"RESULT: FALSIFIED counterexample_read_once=\"{result['counterexample_read_once']}\" first_failing_seed={first_failing_seed}")
    elif any(not r["conjecture_holds_read_twice"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds_read_twice"])
        print(f"RESULT: FALSIFIED counterexample_read_twice=\"{result['counterexample_read_twice']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")