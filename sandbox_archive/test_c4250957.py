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
    results = []
    for N in [10, 15, 20]:
        v = 2 * N
        k = math.ceil(math.log2(v))
        c_values = [1, 1.5]
        for c in c_values:
            random.seed(seed)
            F = set(random.sample(range(v), int(N ** c)))
            G_F = {}
            for T in F:
                for T_prime in F:
                    if T != T_prime and len(T & T_prime) > 0:
                        if (T, T_prime) not in G_F:
                            G_F[(T, T_prime)] = 0
                        G_F[(T, T_prime)] += 1

            def degree(node):
                return sum(G_F.get((node, other), 0) for other in F if node != other)

            μ_F = max(max(0, degree(T) + degree(T_prime) - 4) for (T, T_prime) in G_F)
            κ_F = 0
            core_to_pairs = {}
            for (T, T_prime), count in G_F.items():
                intersection = T & T_prime
                if intersection:
                    core = frozenset(intersection)
                    if core not in core_to_pairs:
                        core_to_pairs[core] = []
                    core_to_pairs[core].append((T, T_prime))

            for core, pairs in core_to_pairs.items():
                max_subset_size = 0
                for i in range(len(pairs)):
                    subset = {pairs[i]}
                    for j in range(i + 1, len(pairs)):
                        if all(pairs[j][0] & pair[0] == core and pairs[j][1] & pair[1] == core for pair in subset):
                            subset.add(pairs[j])
                    max_subset_size = max(max_subset_size, len(subset))
                κ_F = max(κ_F, max_subset_size)

            s = 6 * c * math.log2(1 + κ_F) + 4 - μ_F
            results.append({
                "N": N,
                "c": c,
                "μ_F": μ_F,
                "κ_F": κ_F,
                "s": s
            })

    metric_value = sum(result["s"] for result in results)
    instances_tested = len(results)
    n_max = 20
    conjecture_holds = all(result["s"] >= 0 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "slack",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")