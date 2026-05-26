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
    
    def generate_random_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_tropical_motive(truth_table):
        n = len(truth_table)
        motive = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if truth_table[i] == 1 and truth_table[j] == 1:
                    motive[i][j] = 1
                    motive[j][i] = 1
        return motive
    
    def min_rank(motive):
        n = len(motive)
        rank = 0
        for i in range(n):
            if any(motive[i][j] != 0 for j in range(i, n)):
                rank += 1
                for j in range(n):
                    if motive[j][i] != 0:
                        for k in range(n):
                            motive[j][k] -= motive[i][k]
        return rank
    
    def randomized_communication_complexity(truth_table):
        n = len(truth_table)
        min_bits = float('inf')
        for _ in range(10):  # Sample multiple times to get a good estimate
            bits = 0
            for i in range(n):
                if truth_table[i] == 1:
                    bits += random.randint(1, math.ceil(math.log2(n)))
            min_bits = min(min_bits, bits)
        return min_bits
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_function(n)
        cc_r = randomized_communication_complexity(f)
        M_f = compute_tropical_motive(f)
        rank = min_rank(M_f)
        
        results.append({
            "n": n,
            "cc_r": cc_r,
            "rank": rank
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["rank"] >= math.log2(result["cc_r"])) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")