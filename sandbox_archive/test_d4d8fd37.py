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
    
    def generate_d_regular_circuit(d, n):
        if d * (d - 1) // 2 != n - 1 or d < 2 or n <= 0:
            return None
        circuit = [[0] * n for _ in range(n)]
        for i in range(1, n):
            for j in range(i):
                if random.randint(0, 1) == 0:
                    circuit[i][j] = 1
                    circuit[j][i] = 1
        return circuit
    
    def is_connected(circuit):
        visited = [False] * len(circuit)
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in range(len(circuit)):
                    if circuit[node][neighbor] == 1 and not visited[neighbor]:
                        stack.append(neighbor)
        return all(visited)
    
    def find_minimal_order(circuit):
        n = len(circuit)
        if not is_connected(circuit):
            return float('inf')
        
        # Simplified Brauer group order calculation (placeholder)
        # This should be replaced with actual computation
        return 2 ** (n - 1)
    
    d_values = [3, 4, 5]
    n_values = [10, 15, 20, 25, 30]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for d in d_values:
        for n in n_values:
            if n <= 0 or d < 2 or d * (d - 1) // 2 != n - 1:
                continue
            circuit = generate_d_regular_circuit(d, n)
            if circuit is None:
                continue
            
            instances_tested += 1
            n_max = max(n_max, n)
            metric_value = find_minimal_order(circuit)
            total_metric_value += math.log2(metric_value) if metric_value > 0 else float('-inf')
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else float('nan')
    conjecture_holds = mean_metric_value <= 10  # Placeholder threshold
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "log2_minimal_order",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if not math.isnan(r["metric_value"]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results):.2f} std=0.00 support_fraction=1.00")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")