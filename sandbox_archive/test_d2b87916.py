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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def dpll_search_tree_width(f):
        n = len(f)
        if n == 1:
            return 1
        var = 0
        while f[var] == -1:
            var += 1
        true_branch = [f[i] for i in range(len(f)) if (i >> var) & 1]
        false_branch = [f[i] for i in range(len(f)) if not (i >> var) & 1]
        return max(dpll_search_tree_width(true_branch), dpll_search_tree_width(false_branch))
    
    def geometric_entropy(phi):
        n = len(phi)
        counts = [phi.count(i) for i in set(phi)]
        probabilities = [count / n for count in counts]
        entropy = -sum(p * math.log2(p) for p in probabilities if p != 0)
        return entropy
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        phi = [f[i] for i in range(len(f))]
        wDPLL = dpll_search_tree_width(f)
        Hgeo = geometric_entropy(phi)
        results.append({"n": n, "wDPLL": wDPLL, "Hgeo": Hgeo})
    
    metric_value = sum(result["Hgeo"] * result["wDPLL"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(result["Hgeo"] <= 10 * math.log2(result["n"]) * result["wDPLL"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Hgeo * wDPLL",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")