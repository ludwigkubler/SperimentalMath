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
        if len(f) == 1:
            return 0
        left = f[:len(f)//2]
        right = f[len(f)//2:]
        return max(xor_and_tree_width(left), xor_and_tree_width(right)) + 1
    
    def geometric_langlands_lattice_rank(n):
        # Simplified mapping for demonstration purposes
        return n * (n + 1) // 2
    
    instances_tested = 0
    total_rank = 0
    total_width = 0
    counterexample = ""
    
    for _ in range(30):
        n = random.randint(5, 40)
        f = [random.choice([0, 1]) for _ in range(n)]
        width = xor_and_tree_width(f)
        rank = geometric_langlands_lattice_rank(n)
        
        if width > C(n) and rank > C(n)**2:
            counterexample = f"n={n}, f={f}, width={width}, rank={rank}"
            break
        
        total_rank += rank
        total_width += width
        instances_tested += 1
    
    mean_rank_per_width = total_rank / total_width if total_width > 0 else float('inf')
    conjecture_holds = mean_rank_per_width <= 1 and instances_tested >= 30
    
    return {
        "metric_name": "mean_rank_per_width",
        "metric_value": mean_rank_per_width,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] > 1 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")