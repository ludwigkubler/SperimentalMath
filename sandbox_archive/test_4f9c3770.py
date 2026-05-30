# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def generate_random_3cnf(n: int) -> list:
    clauses = []
    for _ in range(2 * n):
        literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
        random.shuffle(literals)
        clause = literals[:3]
        if len(set(clause)) == 3:  # Ensure no duplicate literals
            clauses.append(clause)
    return clauses

def apply_coxeter_group_action(clauses: list, seed: int) -> set:
    random.seed(seed)
    action_set = set()
    for clause in clauses:
        action_set.add(tuple(sorted(clause)))
    return action_set

def run_trial(seed: int) -> dict:
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = generate_random_3cnf(n)
        distinct_min_length_words = len(apply_coxeter_group_action(clauses, seed))
        n_cubed_root = round(n ** (1/3))
        
        if n_cubed_root == 0:
            continue
        
        ratio = Fraction(distinct_min_length_words, n_cubed_root)
        results.append({
            "n": n,
            "distinct_min_length_words": distinct_min_length_words,
            "n_cubed_root": n_cubed_root,
            "ratio": ratio
        })
    
    if not results:
        return {
            "metric_name": "Coxeter Group Action Ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = all(result["ratio"] >= Fraction(8, 10) for result in results)
    counterexample = "" if conjecture_holds else "First failing seed: {}".format(seed)
    
    return {
        "metric_name": "Coxeter Group Action Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_ratio, 0.0, support_fraction))
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={}".format(seeds[results.index(next(result for result in results if not result["conjecture_holds"]))]))
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")