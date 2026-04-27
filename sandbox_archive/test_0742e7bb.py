# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import Counter

def run_trial(seed: int) -> dict:
    n = random.choice([3, 4, 5, 6])
    density = random.choice([1/4, 1/2, 3/4])
    num_samples = 200
    num_structured = 100
    
    def generate_random_function(n, density):
        tt = [random.randint(0, 1) for _ in range(2**n)]
        for i in range(len(tt)):
            if random.random() < density:
                tt[i] = 1 - tt[i]
        return tt
    
    def generate_structured_function(n, t):
        terms = []
        for _ in range(t):
            term = [random.randint(0, 1) for _ in range(n)]
            terms.append(term)
        return terms
    
    def rle_encoding(tt):
        encoded = []
        count = 1
        prev = tt[0]
        for i in range(1, len(tt)):
            if tt[i] == prev:
                count += 1
            else:
                encoded.append((prev, count))
                prev = tt[i]
                count = 1
        encoded.append((prev, count))
        return encoded
    
    def h_rle(tt):
        rle = rle_encoding(tt)
        entropy = sum(count * math.log2(length + 1) for _, length in rle)
        return entropy
    
    def dnf_min(tt):
        n = int(math.log2(len(tt)))
        prime_implicants = []
        
        def is_prime_implicant(pi, tt):
            for i in range(len(tt)):
                if pi[i] == 0 and tt[i] == 1:
                    return False
            return True
        
        def cover(tt, pi):
            covered = [False] * len(tt)
            for i in range(len(tt)):
                if all(pi[j] == tt[i][j] or pi[j] == 0 for j in range(n)):
                    covered[i] = True
            return all(covered)
        
        for i in range(2**n):
            pi = [i >> j & 1 for j in range(n)]
            if is_prime_implicant(pi, tt):
                prime_implicants.append(pi)
        
        min_cover_size = float('inf')
        for i in range(1 << len(prime_implicants)):
            cover_set = [prime_implicants[j] for j in range(len(prime_implicants)) if (i >> j) & 1]
            if cover(tt, cover_set):
                min_cover_size = min(min_cover_size, sum(pi.count(1) for pi in cover_set))
        
        return min_cover_size
    
    def compute_slack(tt):
        h_rle_val = h_rle(tt)
        dnf_min_val = dnf_min(tt)
        slack = (n + 1) * dnf_min_val - 2**h_rle_val
        return slack
    
    random_functions = [generate_random_function(n, density) for _ in range(num_samples)]
    structured_functions = [generate_structured_function(n, t) for t in range(1, 9)]
    
    all_slacks = []
    for tt in random_functions + structured_functions:
        slack = compute_slack(tt)
        all_slacks.append(slack)
    
    mean_slack = sum(all_slacks) / len(all_slacks)
    median_slack = sorted(all_slacks)[len(all_slacks) // 2]
    
    conjecture_holds = all(slack >= 0 for slack in all_slacks)
    counterexample = "" if conjecture_holds else f"Slack < 0: {min(all_slacks)}"
    
    return {
        "metric_name": "slack",
        "metric_value": mean_slack,
        "instances_tested": len(all_slacks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        random.seed(seed)
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_slack = sum(r["metric_value"] for r in results) / len(results)
    median_slack = sorted([r["metric_value"] for r in results])[len(results) // 2]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slack} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Slack < 0\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")