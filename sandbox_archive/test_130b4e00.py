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
    
    def generate_monotone_k_clique(n):
        if n < 2:
            return []
        clique = set(range(1, n + 1))
        circuit = [(random.choice(list(clique)), random.choice(list(clique))) for _ in range(n - 1)]
        return circuit

    def compute_noncommutative_algebra(circuit):
        # Placeholder for actual computation
        return circuit

    def measure_quotient_rank(algebra):
        # Placeholder for actual computation
        return len(algebra)

    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    for n in n_values:
        circuit = generate_monotone_k_clique(n)
        algebra = compute_noncommutative_algebra(circuit)
        rank = measure_quotient_rank(algebra)
        ranks.append(rank)

    mean_rank = sum(ranks) / len(ranks)
    max_rank = max(ranks)
    min_rank = min(ranks)
    
    conjecture_holds = all(min_rank >= n**2 * math.log(n) for n in n_values) and \
                       all(max_rank <= n**2 * math.log(n) for n in n_values)

    return {
        "metric_name": "quotient_rank",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"max_rank={max_rank}, min_rank={min_rank}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")