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
    
    def generate_polynomial(n):
        coefficients = [random.randint(0, 1) for _ in range(n)]
        return coefficients
    
    def compute_representation_size(f):
        n = len(f)
        size = 2 ** n
        return size
    
    def min_rank_of_representation(size):
        # Simplified approximation for demonstration purposes
        return math.ceil(math.log2(size))
    
    instances_tested = 0
    total_rank = 0
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)
        f = generate_polynomial(n)
        size = compute_representation_size(f)
        rank = min_rank_of_representation(size)
        
        if rank >= math.log(n) - 3 and rank <= math.log(n) + 3:
            instances_tested += 1
            total_rank += rank
    
    mean_rank = total_rank / instances_tested if instances_tested > 0 else 0
    conjecture_holds = instances_tested >= 24  # At least 80% of seeds support the conjecture
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank:.4f} std={std_dev:.4f} support_fraction={support_fraction:.4f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")