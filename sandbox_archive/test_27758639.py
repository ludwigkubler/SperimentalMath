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
    
    def communication_complexity_rank(F):
        n = len(next(iter(F.values())))
        rank = 0
        for i in range(2**n):
            x = [i >> j & 1 for j in range(n)]
            y = F[tuple(x)]
            if y not in F:
                return float('inf')
            rank += 1
        return rank

    def min_quandle_representations(F):
        n = len(next(iter(F.values())))
        representations = []
        for i in range(2**n):
            x = [i >> j & 1 for j in range(n)]
            y = F[tuple(x)]
            representation = {tuple(x): y}
            if all(representation[(x[j], y)] == F[tuple(x[:j] + (y,) + x[j+1:])] for j in range(n)):
                representations.append(representation)
        return len(representations)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        F = {tuple(random.randint(0, 1) for _ in range(n)): random.choice([0, 1]) for _ in range(2**n)}
        rank = communication_complexity_rank(F)
        min_representations = min_quandle_representations(F)
        results.append((n, rank, min_representations))
    
    if not results:
        return {
            "metric_name": "min_quandle_representations",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for _, _, _ in results)
    if n_max < 16:
        return {
            "metric_name": "min_quandle_representations",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_low"
        }
    
    min_representations = [r for _, _, r in results]
    rank_squared = [r**2 for _, r, _ in results]
    
    mean_ratio = sum(min_representations) / sum(rank_squared)
    if mean_ratio > 1.5:
        return {
            "metric_name": "min_quandle_representations",
            "metric_value": mean_ratio,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"mean_ratio={mean_ratio}"
        }
    
    return {
        "metric_name": "min_quandle_representations",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        sys.exit("RESULT: INCONCLUSIVE no_trials_run")
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")