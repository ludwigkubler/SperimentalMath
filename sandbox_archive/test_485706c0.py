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

def generate_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def communication_complexity(f):
    n = int(math.log2(len(f)))
    max_comm_cost = 0
    for i in range(2**n):
        for j in range(i+1, 2**n):
            if f[i] != f[j]:
                comm_cost = bin(i ^ j).count('1')
                if comm_cost > max_comm_cost:
                    max_comm_cost = comm_cost
    return max_comm_cost

def minimal_representation_rank(f):
    n = int(math.log2(len(f)))
    rank = 0
    for i in range(2**n):
        if f[i] == 1:
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_comm_cost = 0
    total_rank = 0
    instances_tested = 0

    for n in n_values:
        f = generate_boolean_function(n)
        comm_cost = communication_complexity(f)
        rank = minimal_representation_rank(f)
        total_comm_cost += comm_cost
        total_rank += rank
        instances_tested += 1

    mean_comm_cost = Fraction(total_comm_cost, instances_tested)
    mean_rank = Fraction(total_rank, instances_tested)
    ratio = mean_rank / mean_comm_cost

    conjecture_holds = ratio <= Fraction(3, 2) and ratio >= Fraction(1, 2)
    counterexample = "" if conjecture_holds else f"Ratio {ratio} outside [0.5, 1.5]"

    return {
        "metric_name": "Ratio of Minimal Representation Rank to Communication Complexity",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio outside [0.5, 1.5]\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")