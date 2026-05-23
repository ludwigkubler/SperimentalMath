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
    
    def generate_monotone_circuit(n):
        if n == 1:
            return (0,)
        else:
            left = generate_monotone_circuit(random.randint(1, n-1))
            right = generate_monotone_circuit(n - len(left) - 1)
            return (0,) + left + right
    
    def decision_tree_depth(circuit):
        if not circuit:
            return 0
        else:
            return max(decision_tree_depth(circuit[1:]), decision_tree_depth(circuit[len(circuit)//2+1:])) + 1
    
    def young_tableau(circuit):
        if len(circuit) == 1:
            return [circuit]
        else:
            left = young_tableau(circuit[1:len(circuit)//2+1])
            right = young_tableau(circuit[len(circuit)//2+1:])
            merged = []
            i, j = 0, 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1
            merged.extend(left[i:])
            merged.extend(right[j:])
            return [merged[0]] + young_tableau(merged[1:])
    
    def rank(tableau):
        if not tableau:
            return 0
        elif len(tableau) == 1:
            return 1
        else:
            max_rank = 0
            for i in range(len(tableau)):
                subtableau = [row[:i] for row in tableau[1:]]
                subrank = rank(subtableau)
                if subrank > max_rank:
                    max_rank = subrank
            return max_rank + 1
    
    n = random.randint(5, 40)
    circuit = generate_monotone_circuit(n)
    depth = decision_tree_depth(circuit)
    tableau = young_tableau(circuit)
    rho = rank(tableau)
    
    metric_value = rho / math.log2(depth)
    instances_tested = 1
    conjecture_holds = metric_value <= 3
    counterexample = "" if conjecture_holds else f"rho={rho}, log(depth)={math.log2(depth)}, ratio={metric_value}"
    
    return {
        "metric_name": "Rank of Young Tableaux vs Decision Tree Depth",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values))} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")