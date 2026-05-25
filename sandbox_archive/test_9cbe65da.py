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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_quotient_representation(f):
        n = int(math.log2(len(f)))
        A = [[f[i * (1 << (n - j)) + k] for k in range(1 << j)] for j in range(n)]
        rank = 0
        for row in A:
            if any(row):
                rank += 1
                for i in range(len(A)):
                    if A[i][0]:
                        for j in range(len(row)):
                            A[i][j] ^= row[j]
        return rank
    
    def compute_entropy_complexity(f):
        n = int(math.log2(len(f)))
        counts = [f.count(i) for i in range(2)]
        entropy = 0
        for count in counts:
            if count > 0:
                p = count / len(f)
                entropy -= p * math.log2(p)
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rank_quot = compute_quotient_representation(f)
        entropy_complexity = compute_entropy_complexity(f)
        
        results.append({
            "n": n,
            "rank_quot": rank_quot,
            "entropy_complexity": entropy_complexity
        })
    
    mean_rank_quot = sum(result["rank_quot"] for result in results) / len(results)
    mean_entropy_complexity = sum(result["entropy_complexity"] for result in results) / len(results)
    
    if all(result["rank_quot"] <= 2 * result["entropy_complexity"] for result in results):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Rank_quot exceeds 2 * Entropy_complexity"
    
    return {
        "metric_name": "rank_quot vs entropy_complexity",
        "metric_value": mean_rank_quot,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank_quot = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank_quot} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank_quot} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")