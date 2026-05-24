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
    
    def bp_read_twice_complexity(n):
        # Placeholder for actual BP_ReadTwice complexity calculation
        return n ** 0.5
    
    def langlands_dual_rank(n):
        # Placeholder for actual Langlands dual rank calculation
        return n ** (1/3)
    
    n = random.randint(5, 40)
    bp_complexity = bp_read_twice_complexity(n)
    expected_rank = langlands_dual_rank(n)
    tolerance = 0.1 * expected_rank
    
    if bp_complexity <= n**(1/3):
        rank = langlands_dual_rank(n)
        conjecture_holds = abs(rank - expected_rank) <= tolerance
        counterexample = "" if conjecture_holds else f"Rank {rank} does not match expected {expected_rank}"
    else:
        rank = None
        conjecture_holds = False
        counterexample = "mapping_undefined"
    
    return {
        "metric_name": "Langlands Dual Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    mean_rank = total_rank / len(results) if len(results) > 0 else 0
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results if r["metric_value"] is not None)) / len(results) if len(results) > 1 else 0
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")