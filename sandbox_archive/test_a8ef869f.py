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
    n = 30  # Fixed size for simplicity, can be adjusted if needed
    instances_tested = 0
    total_rank = 0
    conjecture_holds = True
    counterexample = ""

    def generate_disjointness_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]

    def compute_partial_order(f):
        n = len(f)
        poset = [[False] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == 1 and f[j] == 0:
                    poset[i][j] = True
        return poset

    def compute_quandle_representation(poset):
        n = len(poset)
        quandle = {}
        for i in range(n):
            for j in range(i+1, n):
                if poset[i][j]:
                    quandle[(i, j)] = (j, i)
        return quandle

    def compute_minimal_rank(quandle):
        if not quandle:
            return 0
        rank = 1
        while True:
            new_quandle = {}
            for (a, b), (c, d) in quandle.items():
                if c != a and d != b:
                    new_quandle[(a, b)] = (c, d)
            if not new_quandle:
                break
            rank += 1
            quandle = new_quandle
        return rank

    for _ in range(30):
        f = generate_disjointness_function(n)
        poset = compute_partial_order(f)
        quandle = compute_quandle_representation(poset)
        rank = compute_minimal_rank(quandle)
        total_rank += rank
        instances_tested += 1

    average_rank = total_rank / instances_tested
    if average_rank < n:
        conjecture_holds = False
        counterexample = f"Average minimal rank {average_rank} is less than Ω(n)={n}"

    return {
        "metric_name": "Minimal Rank",
        "metric_value": average_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(result["conjecture_holds"] for result in results):
        mean_rank = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")