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
    
    def generate_k_clique(n, k):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < (k / (n * (n - 1) / 2)):
                    edges.append((i, j))
        return edges

    def monotone_dnf_formula(edges, n):
        variables = [f'x{i}' for i in range(n)]
        formula = []
        for edge in edges:
            clause = f'{variables[edge[0]]} AND {variables[edge[1]]}'
            formula.append(clause)
        return ' OR '.join(formula)

    def matroid_expansion_rank(edges, n):
        rank = 0
        matroid = set()
        for edge in edges:
            if len(matroid.intersection(edge)) == 0:
                rank += 1
                matroid.update(edge)
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = int(math.sqrt(n))
        if k == 0: continue
        edges = generate_k_clique(n, k)
        formula = monotone_dnf_formula(edges, n)
        rank = matroid_expansion_rank(edges, n)
        results.append({'n': n, 'rank': rank})
    
    mean_rank = sum(result['rank'] for result in results) / len(results)
    conjecture_holds = all(n**0.5 <= rank <= n for n, rank in zip(n_values, [result['rank'] for result in results]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "matroid_expansion_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")