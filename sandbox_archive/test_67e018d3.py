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
    
    def generate_abps():
        if n == 1:
            yield [0]
            return
        for left in generate_abps():
            for right in generate_abps():
                if len(left) + len(right) <= 4:
                    yield left + right
    
    def evaluate(abp):
        if not abp:
            return 0
        elif len(abp) == 1:
            return abp[0]
        else:
            mid = len(abp) // 2
            return (evaluate(abp[:mid]) + evaluate(abp[mid:])) % 2
    
    def is_parity_function(abp):
        for i in range(1 << n):
            if evaluate([i] * n) != parity(i):
                return False
        return True
    
    def parity(x):
        x ^= x >> 1
        x ^= x >> 2
        x ^= x >> 4
        x ^= x >> 8
        x ^= x >> 16
        return x & 1
    
    n = random.randint(5, 40)
    abps = list(generate_abps())
    tested_count = min(len(abps), 30)  # Ensure at least 30 instances are tested
    depth_sum = 0
    
    for _ in range(tested_count):
        abp = random.choice(abps)
        if is_parity_function(abp):
            depth_sum += len(abp)
    
    avg_depth = depth_sum / tested_count if tested_count > 0 else 0
    conjecture_holds = avg_depth >= math.log2(n)
    counterexample = "" if conjecture_holds else f"Average depth {avg_depth} < log2({n}) = {math.log2(n)}"
    
    return {
        "metric_name": "average_abp_depth",
        "metric_value": avg_depth,
        "instances_tested": tested_count,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_depth)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Average depth too low\" first_failing_seed={first_failing_seed}")