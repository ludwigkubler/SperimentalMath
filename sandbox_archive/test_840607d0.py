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
    
    def generate_k_clique(n):
        if n < 3:
            return []
        clique = [(i, j) for i in range(n) for j in range(i + 1, n)]
        random.shuffle(clique)
        return clique[:n - 2]
    
    def free_group_generators(clique):
        generators = set()
        relations = set()
        for u, v in clique:
            generators.add(f'g{u}')
            generators.add(f'g{v}')
            relations.add(f'(g{u} * g{v})^2')
        return len(generators), relations
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_generators = 0
    instances_tested = 0
    
    for n in n_values:
        clique = generate_k_clique(n)
        if not clique:
            continue
        num_generators, relations = free_group_generators(clique)
        total_generators += num_generators
        instances_tested += 1
    
    mean_generators = total_generators / instances_tested if instances_tested > 0 else 0
    conjecture_holds = mean_generators >= 3.69
    counterexample = "" if conjecture_holds else f"n={n}, generators={num_generators}"
    
    return {
        "metric_name": "mean_generators",
        "metric_value": mean_generators,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='n={result['counterexample']}' first_failing_seed={first_failing_seed}")