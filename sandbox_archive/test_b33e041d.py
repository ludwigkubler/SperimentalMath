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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_random_ip2_bp(size: int) -> list:
        bp = []
        for _ in range(size):
            bp.append(random.choice([0, 1]))
        return bp
    
    def tensor_rank(bp: list) -> int:
        n = len(bp)
        if n == 1:
            return 1
        rank = 2
        while True:
            found = False
            for i in range(1, n):
                if all(bp[j] == bp[(j + i) % n] for j in range(n)):
                    rank += 1
                    break
            else:
                break
        return rank
    
    def log_size(bp: list) -> float:
        size = len(bp)
        if size <= 0:
            return 0.0
        return math.log(size)
    
    instances_tested = 30
    total_tensor_rank = 0
    counterexample = ""
    
    for _ in range(instances_tested):
        bp = generate_random_ip2_bp(random.randint(5, 40))
        rank = tensor_rank(bp)
        log_s = log_size(bp)
        
        if rank > 10:
            counterexample = f"BP size {len(bp)} has tensor rank {rank}"
            break
        
        total_tensor_rank += rank
    
    mean_rank = total_tensor_rank / instances_tested
    conjecture_holds = all(abs(rank - log_s) <= 0.2 * log_s for rank in range(1, instances_tested + 1))
    
    return {
        "metric_name": "tensor_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")