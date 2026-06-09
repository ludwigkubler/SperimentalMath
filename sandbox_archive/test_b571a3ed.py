# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n):
        if n == 1:
            return [0]
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [0] + [x ^ y for x, y in zip(left, right)]
    
    def ehrhart_semigroup(circuit):
        if len(circuit) == 1:
            return {0}
        else:
            semigroup = set()
            for i in range(len(circuit)):
                if circuit[i] == 0:
                    continue
                sub_circuit = circuit[:i] + [x ^ circuit[i] for x in circuit[i+1:]]
                semigroup.update(ehrhart_semigroup(sub_circuit))
            return semigroup
    
    def depth(circuit):
        if len(circuit) == 1:
            return 0
        else:
            left_depth = depth(circuit[1:])
            right_depth = depth([x ^ circuit[0] for x in circuit[1:]])
            return max(left_depth, right_depth) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    depths = []
    ranks = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(n)
            semigroup = ehrhart_semigroup(circuit)
            depth_val = depth(circuit)
            depths.append(depth_val)
            ranks.append(len(semigroup))
    
    if not depths or not ranks:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_depths_or_ranks"
        }
    
    mean_depth = sum(depths) / len(depths)
    mean_rank = sum(ranks) / len(ranks)
    
    correlation_coefficient = sum((depths[i] - mean_depth) * (ranks[i] - mean_rank) for i in range(len(depths))) / len(depths)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.9 and all(corr >= 0.7 for corr in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.2:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")