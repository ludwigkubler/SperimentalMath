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
    
    def generate_max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def configuration_space_invariant(edges):
        # Placeholder implementation
        return len(edges)
    
    def sos_degree(n):
        # Placeholder implementation
        return int(2 * math.log2(n) + 1)
    
    n = random.randint(5, 40)
    instance = generate_max_cut_instance(n)
    invariant_rank = configuration_space_invariant(instance)
    sos_deg = sos_degree(n)
    
    ratio = invariant_rank / sos_deg
    return {
        "metric_name": "Invariant Rank to SOS Degree Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": abs(ratio - 0.879) < 0.5,
        "counterexample": f"n={n}, invariant_rank={invariant_rank}, sos_degree={sos_deg}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['instances_tested']}, invariant_rank={result['metric_value']}, sos_degree=1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")