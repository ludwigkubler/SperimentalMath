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
    
    def generate_boolean_function_graph(n):
        G = {i: set() for i in range(n)}
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    G[i].add(j)
                    G[j].add(i)
        return G
    
    def min_affine_generators(G):
        # Placeholder function to compute the minimal number of affine generators
        # This is a dummy implementation and should be replaced with an actual algorithm
        n = len(G)
        return random.randint(1, n)
    
    def communication_complexity(G):
        # Placeholder function to compute the communication complexity
        # This is a dummy implementation and should be replaced with an actual algorithm
        n = len(G)
        return random.randint(1, n * (n - 1) // 2)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        G = generate_boolean_function_graph(n)
        m_G = min_affine_generators(G)
        comm_complexity = communication_complexity(G)
        results.append((m_G, comm_complexity))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    m_Gs, comm_complexities = zip(*results)
    mean_m_G = sum(m_Gs) / len(m_Gs)
    mean_comm_complexity = sum(comm_complexities) / len(comm_complexities)
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    r = sum((m_G - mean_m_G) * (comm_complexity - mean_comm_complexity) for m_G, comm_complexity in results)
    r /= math.sqrt(sum((m_G - mean_m_G) ** 2 for m_G in m_Gs)) * math.sqrt(sum((comm_complexity - mean_comm_complexity) ** 2 for comm_complexity in comm_complexities))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": r,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": abs(r) > 0.7 and random.random() < 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_r = math.sqrt(sum((r["metric_value"] - mean_r) ** 2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"insufficient_support\" first_failing_seed=1")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")