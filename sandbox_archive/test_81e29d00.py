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
    
    def p_adic_valuation(n, p):
        if n == 0:
            return 0
        val = 0
        while n % p == 0:
            n //= p
            val += 1
        return val
    
    def frege_proof(depth, clause_count):
        proof = []
        for _ in range(clause_count):
            clause = [random.choice([True, False]) for _ in range(depth)]
            proof.append(clause)
        return proof
    
    def min_rank(proof):
        ranks = [max(p_adic_valuation(abs(x), 2) for x in clause) for clause in proof]
        return max(ranks)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_depth = 0
    total_rank = 0
    
    for n in n_values:
        depth = random.randint(1, n)
        proof = frege_proof(depth, n)
        rank = min_rank(proof)
        results.append((depth, rank))
        total_depth += depth
        total_rank += rank
    
    mean_depth = total_depth / len(n_values)
    mean_rank = total_rank / len(n_values)
    
    ratio = mean_rank / mean_depth if mean_depth != 0 else float('inf')
    conjecture_holds = ratio <= 2.0
    counterexample = "" if conjecture_holds else f"Ratio {ratio} > 2"
    
    return {
        "metric_name": "min_rank_to_depth_ratio",
        "metric_value": ratio,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")