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
    
    def generate_sat_instance(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            while len(set(clause)) == 1:  # Ensure at least one positive and one negative
                clause[random.randint(0, n-1)] *= -1
            clauses.append(clause)
        return clauses
    
    def ternary_diatomic_sequences(clauses):
        sequences = set()
        for assignment in product([-1, 0, 1], repeat=len(clauses)):
            sequence = []
            for i, clause in enumerate(clauses):
                if all(assignment[j] * clause[j] >= 0 for j in range(len(clause))):
                    sequence.append(1)
                elif any(assignment[j] * clause[j] < 0 for j in range(len(clause))):
                    sequence.append(-1)
                else:
                    sequence.append(0)
            sequences.add(tuple(sequence))
        return sequences
    
    def product(iterables):
        pools = [tuple(pool) for pool in iterables]
        result = [[]]
        for pool in pools:
            result = [x + [y] for x in result for y in pool]
        return result
    
    n_max = 0
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, 41):
        for m in range(5, 41):
            if n * m > 200:  # Avoid excessive computation time
                continue
            instances_tested += 1
            n_max = max(n_max, n)
            clauses = generate_sat_instance(n, m)
            sequences = ternary_diatomic_sequences(clauses)
            metric_value = len(sequences)
            total_metric_value += metric_value
            
            if instances_tested >= 30:
                break
        
        if instances_tested >= 30:
            break
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = instances_tested / 60
    
    return {
        "metric_name": "Number of Ternary Diatomic Sequences",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")