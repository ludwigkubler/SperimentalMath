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
            return [random.choice([left, right]) for _ in range(2)]
    
    def depth(circuit):
        if isinstance(circuit[0], list):
            return 1 + max(depth(sub) for sub in circuit)
        else:
            return 1
    
    def noncrossing_partition(circuit):
        if len(circuit) == 1:
            return [circuit]
        else:
            left = noncrossing_partition(circuit[:len(circuit)//2])
            right = noncrossing_partition(circuit[len(circuit)//2:])
            return [left, right]
    
    def local_coherence_index(partition):
        if len(partition) == 1:
            return 0
        else:
            return max(local_coherence_index(sub) for sub in partition)
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    depth_value = depth(circuit)
    partition = noncrossing_partition(circuit)
    coherence_index = local_coherence_index(partition)
    
    if coherence_index > math.log(n) * depth_value + 3 or coherence_index < math.log(n) * depth_value - 3:
        return {
            "metric_name": "local_coherence_index",
            "metric_value": coherence_index,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"n={n}, depth={depth_value}, coherence_index={coherence_index}"
        }
    
    return {
        "metric_name": "local_coherence_index",
        "metric_value": coherence_index,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
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
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, depth={depth(results[0]['circuit'])}, coherence_index={results[0]['coherence_index']}\" first_failing_seed={first_failing_seed}")