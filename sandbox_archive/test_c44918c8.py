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
            return [0]
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [left, right]
    
    def depth(circuit):
        if isinstance(circuit, int):
            return 1
        else:
            return 1 + max(depth(circuit[0]), depth(circuit[1]))
    
    def noncrossing_partition(circuit):
        if isinstance(circuit, int):
            return {circuit}
        else:
            left_part = noncrossing_partition(circuit[0])
            right_part = noncrossing_partition(circuit[1])
            return left_part.union(right_part)
    
    def local_coherence_index(partition):
        n = len(partition)
        if n == 1:
            return 0
        else:
            max_distance = 0
            for i in range(n):
                for j in range(i + 1, n):
                    if partition[i] < partition[j]:
                        distance = partition[j] - partition[i]
                    else:
                        distance = partition[i] - partition[j]
                    if distance > max_distance:
                        max_distance = distance
            return max_distance
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        depth_value = depth(circuit)
        partition = noncrossing_partition(circuit)
        coherence_index = local_coherence_index(partition)
        
        results.append({
            "n": n,
            "depth": depth_value,
            "coherence_index": coherence_index
        })
    
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(abs(result["coherence_index"] - math.log(result["n"]) * result["depth"]) <= 3 for result in results)
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, depth={results[0]['depth']}, coherence_index={results[0]['coherence_index']}"
    
    return {
        "metric_name": "local_coherence_index",
        "metric_value": sum(result["coherence_index"] for result in results) / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, depth={results[0]['depth']}, coherence_index={results[0]['coherence_index']}\" first_failing_seed={first_failing_seed}")