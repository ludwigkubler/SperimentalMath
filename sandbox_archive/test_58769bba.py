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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_d_regular_circuit(d, depth):
        if d == 1 or depth == 0:
            return []
        elif depth == 1:
            return [[random.randint(0, 1)] * d]
        else:
            circuit = []
            for _ in range(d):
                sub_circuit = generate_random_d_regular_circuit(d, depth - 1)
                circuit.append([random.randint(0, 1)] + [x for sublist in sub_circuit for x in sublist])
            return circuit
    
    def construct_tropical_graph(circuit):
        n = len(circuit[0]) - 1
        T = [[math.inf] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            T[i][i] = 0
        for gate in circuit:
            for j in range(1, n + 1):
                if gate[j - 1] == 1:
                    for k in range(1, n + 1):
                        T[j][k] = min(T[j][k], T[gate[0]][j] + T[k][gate[-1]])
        return T
    
    def min_representation_size(T):
        n = len(T) - 1
        visited = [False] * (n + 1)
        stack = [1]
        size = 0
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                size += 1
                for i in range(1, n + 1):
                    if T[node][i] < math.inf and not visited[i]:
                        stack.append(i)
        return size
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    d = random.randint(2, 5)
    depth = int(math.log2(d)) + 1
    circuit = generate_random_d_regular_circuit(d, depth)
    T = construct_tropical_graph(circuit)
    min_rep_size = min_representation_size(T)
    
    metric_name = "min_representation_size"
    metric_value = min_rep_size
    instances_tested = 1
    n_max = len(circuit[0]) - 1
    conjecture_holds = min_rep_size <= depth ** 2 * math.log(d)
    counterexample = "" if conjecture_holds else f"min_rep_size={min_rep_size}, D^2*log(d)={depth**2*math.log(d)}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=undefined_mapping")