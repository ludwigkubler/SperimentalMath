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

def generate_noncrossing_partition(n):
    if n == 0:
        return [[]]
    partitions = []
    for k in range(1, n):
        for p in generate_noncrossing_partition(k):
            for q in generate_noncrossing_partition(n-k-1):
                partitions.append(p + [(x+k+1) for x in q])
    return partitions

def calculate_rank(partition):
    rank = 0
    for block in partition:
        rank += len(block)
    return rank

def calculate_communication_complexity(n, seed):
    random.seed(seed)
    A = [random.choice([0, 1]) for _ in range(n)]
    B = [random.choice([0, 1]) for _ in range(n)]
    count = 0
    for i in range(n):
        if A[i] != B[i]:
            count += 1
    return Fraction(count, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    partitions = generate_noncrossing_partition(n)
    ranks = [calculate_rank(p) for p in partitions]
    complexities = [calculate_communication_complexity(n, seed + i) for i in range(len(partitions))]
    
    if len(ranks) != len(complexities):
        return {
            "metric_name": "Spearman rank correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "Mismatch in number of ranks and complexities"
        }
    
    n = len(ranks)
    rank_pairs = sorted([(ranks[i], complexities[i]) for i in range(n)])
    sorted_ranks = [x[0] for x in rank_pairs]
    sorted_complexities = [x[1] for x in rank_pairs]
    
    rho_numerator = sum((sorted_ranks[i] - (n + 1) / 2) * (sorted_complexities[i] - (n + 1) / 2) for i in range(n))
    rho_denominator = math.sqrt(sum((sorted_ranks[i] - (n + 1) / 2) ** 2 for i in range(n))) * math.sqrt(sum((sorted_complexities[i] - (n + 1) / 2) ** 2 for i in range(n)))
    
    rho = rho_numerator / rho_denominator if rho_denominator != 0 else None
    
    return {
        "metric_name": "Spearman rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": n,
        "conjecture_holds": rho is not None and rho >= 0.7,
        "counterexample": "" if rho is not None and rho >= 0.7 else f"rho={rho}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho<{0.7}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")