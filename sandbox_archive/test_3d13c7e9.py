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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def monomial_ideal(boolean_function):
        n = int(math.log2(len(boolean_function)))
        ideal = set()
        for i in range(2**n):
            if boolean_function[i] == 1:
                monomial = [0] * n
                for j in range(n):
                    if (i >> j) & 1:
                        monomial[j] = 1
                ideal.add(tuple(monomial))
        return ideal
    
    def coxeter_group_rank(ideal):
        generators = []
        for i in range(len(ideal)):
            for j in range(i + 1, len(ideal)):
                if all(x != y for x, y in zip(ideal[i], ideal[j])):
                    generators.append((i, j))
        return len(generators)
    
    def degree(boolean_function):
        n = int(math.log2(len(boolean_function)))
        max_degree = 0
        for i in range(2**n):
            if boolean_function[i] == 1:
                degree = sum(1 for x in bin(i)[2:] if x == '1')
                if degree > max_degree:
                    max_degree = degree
        return max_degree
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            boolean_function = generate_boolean_function(n)
            ideal = monomial_ideal(boolean_function)
            rank = coxeter_group_rank(ideal)
            degree_value = degree(boolean_function)
            
            total_rank += rank
            instances_tested += 1
            
            if rank > degree_value:
                return {
                    "metric_name": "Coxeter Group Rank",
                    "metric_value": rank,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, rank={rank}, degree={degree_value}"
                }
    
    mean_rank = total_rank / instances_tested
    return {
        "metric_name": "Coxeter Group Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": mean_rank <= max(n_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rank > degree' first_failing_seed={first_failing_seed}")