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
    
    def generate_circuit(n):
        if n == 1:
            return '0'
        elif n == 2:
            return '(0, 1)'
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return f'({left}, {right})'
    
    def alexander_module(circuit):
        if isinstance(circuit, str) and circuit.startswith('(') and circuit.endswith(')'):
            left, right = circuit[1:-1].split(', ')
            A_left = alexander_module(left)
            A_right = alexander_module(right)
            # Construct Alexander module for AND-gate
            return [A_left[i] + A_right[j] for i in range(len(A_left)) for j in range(len(A_right))]
        elif circuit == '0':
            return ['']
        elif circuit == '1':
            return ['1']
    
    def min_rank(module):
        rank = 0
        for row in module:
            if any(row[i] != '0' for i in range(len(row))):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        A = alexander_module(circuit)
        rank = min_rank(A)
        f_n = math.log(n)
        results.append({
            "n": n,
            "rank": rank,
            "f_n": f_n
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    mean_f_n = sum(result["f_n"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if abs(result["rank"] - result["f_n"]) <= 3) / len(results)
    
    return {
        "metric_name": "Min Rank",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"n={results[0]['n']}, rank={results[0]['rank']}, f_n={results[0]['f_n']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 35)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, rank={results[0]['rank']}, f_n={results[0]['f_n']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")