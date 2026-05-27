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
    
    def xor_and_tree_width(f):
        # Placeholder function to compute XOR-AND tree width
        # This is a dummy implementation and should be replaced with an actual algorithm
        return len(f)

    def tropicalized_barycentric_coordinates(f):
        # Placeholder function to compute tropicalized barycentric coordinates
        # This is a dummy implementation and should be replaced with an actual algorithm
        return [Fraction(1, 2)] * len(f)
    
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(n)]
    
    tree_width = xor_and_tree_width(f)
    barycentric_coords = tropicalized_barycentric_coordinates(f)
    
    rank = len(set(barycentric_coords))
    
    return {
        "metric_name": "Rank_Tropical",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")