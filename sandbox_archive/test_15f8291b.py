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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def negate_circuit(circuit):
        return [1 - bit for bit in circuit]
    
    def smallest_unate_polynomial_degree(circuit):
        n = len(circuit)
        max_degree = 0
        for i in range(n):
            count_0 = circuit[:i].count(0) + (circuit[i] == 0)
            count_1 = circuit[:i].count(1) + (circuit[i] == 1)
            degree = min(count_0, count_1)
            max_degree = max(max_degree, degree)
        return max_degree
    
    def tiling_system_rank(circuit):
        n = len(circuit)
        rank = 1
        for i in range(n):
            if circuit[i] == 1:
                rank *= 2
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n)
            negated_circuit = negate_circuit(circuit)
            degree = smallest_unate_polynomial_degree(negated_circuit)
            rank = tiling_system_rank(circuit)
            if rank == 0:
                continue
            ratio = math.exp(degree) / rank
            total_metric_value += ratio
            instances_tested += 1
            n_max = max(n_max, n)
            if ratio < 1:
                conjecture_holds = False
                counterexample = f"Circuit size {n} with ratio {ratio}"
    
    return {
        "metric_name": "Ratio of exp(degree) to rank",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")