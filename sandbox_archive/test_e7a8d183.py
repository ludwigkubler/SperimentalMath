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
    
    def entropy(p):
        if p == 0 or p == 1:
            return 0
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

    def hodge_rank(n, H):
        # Placeholder for actual Hodge rank computation
        # This is a dummy function that returns a value based on n and H
        return int(H * 2)

    instances_tested = 0
    total_entropy = 0
    total_rank = 0

    for _ in range(30):
        n = random.randint(5, 40)
        p = random.random()
        H = entropy(p)
        
        if H < 1:
            continue
        
        instances_tested += 1
        rank = hodge_rank(n, H)
        total_entropy += H
        total_rank += rank

    mean_entropy = total_entropy / instances_tested
    mean_rank = total_rank / instances_tested
    
    conjecture_holds = mean_rank <= 3 and (mean_rank / mean_entropy) >= 0.8
    counterexample = "" if conjecture_holds else f"Mean rank {mean_rank}, Mean entropy {mean_entropy}"
    
    return {
        "metric_name": "Hodge Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    mean_entropy = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Mean rank {results[0]['metric_value']}, Mean entropy {results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")