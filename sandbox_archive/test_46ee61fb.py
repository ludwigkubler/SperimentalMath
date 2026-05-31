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
    
    def generate_clause_set(n):
        return [random.choice([f"x{i}", f"~x{i}"]) for _ in range(n)]
    
    def minimal_tropical_rank(clause_set):
        literals = set()
        for clause in clause_set:
            literals.update(clause.split(' '))
        rank = 0
        for literal in literals:
            if literal.startswith('~'):
                rank += 1
        return rank
    
    def pearson_correlation(ranks, n_values):
        mean_ranks = sum(ranks) / len(ranks)
        mean_n = sum(n_values) / len(n_values)
        numerator = sum((r - mean_ranks) * (n - mean_n) for r, n in zip(ranks, n_values))
        denominator = math.sqrt(sum((r - mean_ranks)**2 for r in ranks)) * math.sqrt(sum((n - mean_n)**2 for n in n_values))
        return numerator / denominator if denominator != 0 else 0
    
    ranks = []
    n_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        clause_sets = [generate_clause_set(n) for _ in range(30)]
        for clause_set in clause_sets:
            mtr = minimal_tropical_rank(clause_set)
            ranks.append(mtr)
            n_values.append(n)
    
    correlation_coefficient = pearson_correlation(ranks, n_values)
    alpha = math.log(correlation_coefficient) / math.log(len(ranks))
    
    metric_name = "Pearson Correlation Coefficient"
    metric_value = correlation_coefficient
    instances_tested = len(ranks)
    n_max = max(n_values)
    conjecture_holds = abs(correlation_coefficient) >= 0.7 and -0.05 <= alpha - correlation_coefficient <= 0.05
    counterexample = "" if conjecture_holds else f"alpha={alpha:.2f} (expected α within ±5%)"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"alpha out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")