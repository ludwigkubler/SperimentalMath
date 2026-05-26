# auto-injected by SEC sandbox
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
import math
from itertools import product

def braid_monodromy_representation(tree):
    if isinstance(tree, int):
        return [[1]]
    left_rep = braid_monodromy_representation(tree[0])
    right_rep = braid_monodromy_representation(tree[1])
    new_rep = []
    for l in left_rep:
        for r in right_rep:
            new_row = [l[i] * r[i] for i in range(len(l))]
            new_rep.append(new_row)
    return new_rep

def minimal_rank(matrix):
    n = len(matrix)
    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        k = random.randint(1, n)
        xor_and_tree = tuple(random.sample(range(n), n))
        braid_rep = braid_monodromy_representation(xor_and_tree)
        rank = minimal_rank(braid_rep)
        results.append(rank)
    mean_rank = sum(results) / len(results)
    conjecture_holds = math.isclose(mean_rank, k * math.log2(n)**2, rel_tol=0.1)
    counterexample = "" if conjecture_holds else f"n={n}, k={k}, rank={mean_rank}"
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")