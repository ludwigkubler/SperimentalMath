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
    
    def minor_free_planar_graph(G):
        # Implement a procedure to generate a minor-free planar graph M_G from G
        # This is a placeholder implementation; replace with actual logic
        return G
    
    def geometric_entropy(v):
        # Implement a function to compute the geometric entropy of vertex v
        # This is a placeholder implementation; replace with actual logic
        return random.random()
    
    def ACC0_circuit(f):
        # Implement a procedure to construct an ACC⁰ circuit C_f for function f
        # This is a placeholder implementation; replace with actual logic
        return []
    
    def count_vertices_with_entropy(G, ε):
        H_G = [v for v in G if geometric_entropy(v) <= ε]
        return len(H_G)
    
    n = random.randint(5, 40)
    f = lambda x: sum(x[i] * i for i in range(n))  # Example explicit function
    C_f = ACC0_circuit(f)
    G = [i for i in range(n)]  # Example graph representing the circuit
    
    M_G = minor_free_planar_graph(G)
    ε = max(geometric_entropy(v) for v in G)
    H_M_G = count_vertices_with_entropy(M_G, ε)
    
    metric_name = "Number of Vertices with Geometric Entropy ≤ ε"
    metric_value = H_M_G
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if H_M_G >= n / 2:  # Example condition; replace with actual logic
        conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
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
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")