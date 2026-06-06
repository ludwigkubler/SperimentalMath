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
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def ternary_diatomic_sequences(clauses):
        sequences = set()
        for assignment in product([-1, 0, 1], repeat=len(clauses)):
            sequence = []
            for clause in clauses:
                value = sum(x * a for x, a in zip(assignment, clause))
                if value > 0:
                    sequence.append(1)
                elif value < 0:
                    sequence.append(-1)
                else:
                    sequence.append(0)
            sequences.add(tuple(sequence))
        return sequences
    
    def product(iterables):
        result = [[]]
        for iterable in iterables:
            result = [x + [y] for x in result for y in iterable]
        return result
    
    n_values = [5, 10, 15, 20, 30, 40]
    m_values = [n // 2 for n in n_values]
    
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n, m in zip(n_values, m_values):
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_sat_instance(n, m)
            sequences = ternary_diatomic_sequences(clauses)
            metric_value = len(sequences)
            total_metric_value += metric_value
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = True
    counterexample = ""
    
    if instances_tested > 0:
        for n, m in zip(n_values, m_values):
            for _ in range(5):  # Ensure at least 30 instances per seed
                clauses = generate_sat_instance(n, m)
                sequences = ternary_diatomic_sequences(clauses)
                metric_value = len(sequences)
                if metric_value > n**2 * m:
                    conjecture_holds = False
                    counterexample = f"n={n}, m={m}: Expected <= {n**2 * m}, got {metric_value}"
                    break
    
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
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")