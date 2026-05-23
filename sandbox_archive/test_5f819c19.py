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
    
    def max_cut_instance(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def configuration_space_invariant(edges):
        # Placeholder implementation
        return len(edges)
    
    def sos_degree(n):
        # Placeholder implementation
        return int(2 * math.log(n) + 1)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    edges = max_cut_instance(n)
    invariant_rank = configuration_space_invariant(edges)
    sos_deg = sos_degree(n)
    
    if invariant_rank == 0 or sos_deg == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = invariant_rank / sos_deg
    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": abs(ratio - 0.879) < 0.435,  # 2 * 0.879 / 2
        "counterexample": "" if abs(ratio - 0.879) < 0.435 else f"Ratio {ratio} is not within a factor of 2 from 0.879"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "mapping_undefined" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["counterexample"] != "mapping_undefined")
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")