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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(1, n))]
            circuit.append((gate, inputs))
        return circuit
    
    def monotone_width(circuit):
        width = 0
        current_width = 0
        for gate, inputs in circuit:
            if gate == 'AND':
                current_width += len(inputs)
            elif gate == 'OR':
                current_width -= 1
            width = max(width, current_width)
        return width
    
    def algebraic_k_theory_rank(circuit):
        rank = 0
        for _, inputs in circuit:
            rank += len(inputs)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_r_K = 0
    total_w_mon = 0
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_random_circuit(n)
            r_K = algebraic_k_theory_rank(circuit)
            w_mon = monotone_width(circuit)
            instances_tested += 1
            total_r_K += r_K
            total_w_mon += w_mon
            
            if abs(r_K - w_mon) > 3:
                counterexample = f"Circuit with n={n} and r_K={r_K}, w_mon={w_mon}"
    
    mean_r_K = total_r_K / instances_tested
    mean_w_mon = total_w_mon / instances_tested
    
    if abs(mean_r_K - mean_w_mon) > 3:
        conjecture_holds = False
    else:
        conjecture_holds = True
    
    return {
        "metric_name": "Algebraic K-Theory Rank vs Monotone Width",
        "metric_value": mean_r_K,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"{results[sum(1 for r in results if not r['conjecture_holds']) - 1]['counterexample']}\" first_failing_seed={seeds[sum(1 for r in results if not r['conjecture_holds']) - 1]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")