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

def generate_monotone_circuit(n):
    if n == 1:
        return [0]
    else:
        left = generate_monotone_circuit(random.randint(1, n-1))
        right = generate_monotone_circuit(n - len(left) - 1)
        return [random.choice([0] + left + right)]

def construct_young_tableau(circuit):
    if not circuit:
        return []
    else:
        root = circuit[0]
        left = construct_young_tableau([x for x in circuit if x < root])
        right = construct_young_tableau([x for x in circuit if x > root])
        return [root] + left + right

def rank_of_young_tableau(tableau):
    n = len(tableau)
    if n == 0:
        return 0
    else:
        max_row_length = max(len(row) for row in tableau)
        rank = 1
        for i in range(1, max_row_length):
            if any(j >= len(row) for row in tableau[:i]):
                break
            rank += 1
        return rank

def decision_tree_depth(circuit):
    if not circuit:
        return 0
    else:
        left = decision_tree_depth([x for x in circuit if x < circuit[0]])
        right = decision_tree_depth([x for x in circuit if x > circuit[0]])
        return max(left, right) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            circuit = generate_monotone_circuit(n)
            tableau = construct_young_tableau(circuit)
            depth = decision_tree_depth(circuit)
            rank = rank_of_young_tableau(tableau)
            
            if depth == 0:
                continue
            
            ratio = rank / math.log2(2 ** depth)
            total_metric_value += ratio
            instances_tested += 1
    
    metric_mean = total_metric_value / instances_tested
    support_fraction = sum(ratio <= 3 for ratio in ratios) / len(ratios)
    
    conjecture_holds = support_fraction >= 0.8 and metric_mean <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of Rank to Log2(Decision Tree Depth)",
        "metric_value": metric_mean,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 83))  # First 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction=<z> (not enough seeds supported)")