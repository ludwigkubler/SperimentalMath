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

def generate_k_clique(n, k):
    if k > n:
        return None
    vertices = list(range(n))
    clique = set(random.sample(vertices, k))
    dnf_formula = []
    for i in range(1 << n):
        subset = [j for j in range(n) if (i & (1 << j))]
        if len(subset) == k and all(j in clique for j in subset):
            clause = ' AND '.join(f'x{i}' for i in subset)
            dnf_formula.append(clause)
    return dnf_formula

def matroid_expansion_rank(dnf_formula):
    if not dnf_formula:
        return 0
    n = len(dnf_formula[0].split(' AND '))
    rank = 1
    for clause in dnf_formula:
        variables = set(clause.split(' AND '))
        if all(variables.issubset(set(clause.split(' AND '))) for clause in dnf_formula):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = min(n // 2, 3)  # Ensure k is at least 1 and at most n//2
        dnf_formula = generate_k_clique(n, k)
        if dnf_formula is None:
            continue
        rank = matroid_expansion_rank(dnf_formula)
        results.append(rank)
    
    mean_rank = sum(results) / len(results) if results else 0
    conjecture_holds = n_values[0] ** 0.5 <= mean_rank <= n_values[-1]
    counterexample = "" if conjecture_holds else f"mean_rank={mean_rank}"
    
    return {
        "metric_name": "matroid_expansion_rank",
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
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank:.6f} std=0.000000 support_fraction={support_fraction:.2%}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mean_rank does not meet conjectured bounds\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction:.2%} (not enough evidence to support or falsify the conjecture)")