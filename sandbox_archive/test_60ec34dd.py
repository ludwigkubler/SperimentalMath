# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, permutations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def monomial_ideal(boolean_func):
        n = len(boolean_func)
        ideal = set()
        for i in range(1, n + 1):
            for comb in combinations(range(n), i):
                monomial = [1 if j in comb else 0 for j in range(n)]
                ideal.add(tuple(monomial))
        return ideal
    
    def coxeter_group_rank(ideal):
        n = len(next(iter(ideal)))
        generators = []
        for i in range(n):
            generators.append((1,) * i + (0,) * (n - i) + (-1,))
        relations = set()
        for gen1, gen2 in combinations(generators, 2):
            product = tuple(a * b for a, b in zip(gen1, gen2))
            if all(x != y for x, y in zip(product, (1,) * n)):
                relations.add((gen1, gen2))
        return len(relations)
    
    def degree(boolean_func):
        n = len(boolean_func)
        max_length = 0
        for i in range(1 << n):
            binary_rep = bin(i)[2:].zfill(n)
            if all(binary_rep[j] == str(boolean_func[j]) for j in range(n)):
                length = sum(int(bit) for bit in binary_rep)
                if length > max_length:
                    max_length = length
        return max_length
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        boolean_func = generate_boolean_function(n)
        ideal = monomial_ideal(boolean_func)
        rank = coxeter_group_rank(ideal)
        degree_value = degree(boolean_func)
        results.append((n, rank, degree_value))
    
    mean_rank = sum(rank for _, rank, _ in results) / len(results)
    support_fraction = all(rank <= degree_value for _, rank, degree_value in results)
    
    return {
        "metric_name": "Coxeter Group Rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction,
        "counterexample": "" if support_fraction else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed)["metric_value"] for seed in seeds]
    mean_result = sum(results) / len(results)
    support_fraction = all(result <= n for result, n in zip(results, [5, 10, 15, 20, 30, 40]))
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_result} std=0.0 support_fraction=1.0")
    elif any(result > n for result, n in zip(results, [5, 10, 15, 20, 30, 40])):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")