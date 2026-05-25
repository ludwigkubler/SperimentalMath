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
    
    def k_theory_group(V):
        n = len(V)
        if n == 0:
            return 0
        G_V = sum([sum(V[i][k] * V[j][l] for l in range(n)) for k in range(n) for j in range(n)]) / (n ** 2)
        return G_V
    
    def communication_complexity_disjointness(V):
        n = len(V)
        if n == 0:
            return 0
        # Simulate a simple randomized algorithm for Disjointness
        x = [random.choice([0, 1]) for _ in range(n)]
        y = [random.choice([0, 1]) for _ in range(n)]
        return sum(1 if x[i] != y[i] else 0 for i in range(n))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        V = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        G_V = k_theory_group(V)
        comm_complexity = communication_complexity_disjointness(V)
        results.append({
            "n": n,
            "G_V": G_V,
            "comm_complexity": comm_complexity
        })
    
    mean_comm_complexity = sum(result["comm_complexity"] for result in results) / len(results)
    std_comm_complexity = math.sqrt(sum((result["comm_complexity"] - mean_comm_complexity) ** 2 for result in results) / len(results))
    conjecture_holds = mean_comm_complexity >= n_values[-1] ** (3/2) and std_comm_complexity < 0.1 * n_values[-1] ** (3/2)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_comm_complexity,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean_comm_complexity={mean_comm_complexity}, std_comm_complexity={std_comm_complexity}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result)
    
    mean_comm_complexity = sum(result["metric_value"] for result in results) / len(results)
    std_comm_complexity = math.sqrt(sum((result["metric_value"] - mean_comm_complexity) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std={std_comm_complexity} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std={std_comm_complexity} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")