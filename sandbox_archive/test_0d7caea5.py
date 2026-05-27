# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_entangled_state(n):
        return [1 / math.sqrt(2)] * n + [-1 / math.sqrt(2)] * n
    
    def algebraic_hologram(state):
        n = len(state)
        hologram = []
        for i in range(n):
            for j in range(i+1, n):
                hologram.append((i, j, state[i] * state[j]))
        return hologram
    
    def min_rank(hologram):
        if not hologram:
            return 0
        rank = 0
        rows = []
        for i, (r1, r2, val) in enumerate(hologram):
            row = [val]
            for j, (s1, s2, v) in enumerate(hologram):
                if i != j:
                    row.append(v * state[s1] * state[s2])
            rows.append(row)
        while rows:
            max_row_index = 0
            max_val = abs(rows[0][0])
            for i, row in enumerate(rows):
                if abs(row[0]) > max_val:
                    max_row_index = i
                    max_val = abs(row[0])
            pivot_row = rows.pop(max_row_index)
            rank += 1
            for i, row in enumerate(rows):
                factor = -row[0] / pivot_row[0]
                rows[i] = [pivot_row[j] + factor * row[j] for j in range(len(pivot_row))]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        state = generate_entangled_state(n)
        hologram = algebraic_hologram(state)
        rank = min_rank(hologram)
        ranks.append(rank)
    
    metric_value = sum(ranks) / len(ranks)
    conjecture_holds = all(rank >= 0.5 * math.log(n, 2) for n, rank in zip(n_values, ranks))
    counterexample = "" if conjecture_holds else "minimal_rank_less_than_half_log_n"
    
    return {
        "metric_name": "min_rank",
        "metric_value": metric_value,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: FALSIFIED counterexample=minimal_rank_less_than_half_log_n first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")