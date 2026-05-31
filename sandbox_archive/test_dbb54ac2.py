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
        G = {i: set() for i in range(2**n)}
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if (i & j) == 0:
                    G[i].add(j)
                    G[j].add(i)
        return G
    
    def min_affine_generators(G):
        n = int(math.log2(len(G)))
        generators = set()
        for i in range(2**n):
            if all((i | j) in G[i] for j in G[i]):
                generators.add(i)
        return len(generators)
    
    def communication_complexity(G):
        n = int(math.log2(len(G)))
        max_degree = 0
        for i in range(2**n):
            max_degree = max(max_degree, len(G[i]))
        return max_degree
    
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
    mean_ranks = [sum(1 for x in m_Gs if x <= r) / len(m_Gs) for r in sorted(set(m_Gs))]
    rho = sum((m_G - mean_ranks[i]) * (comm_complexity - mean_ranks[i]) for i, (m_G, comm_complexity) in enumerate(results)) / math.sqrt(sum((m_G - mean_ranks[0])**2 for m_G in m_Gs) * sum((comm_complexity - mean_ranks[1])**2 for comm_complexity in comm_complexities))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": max(5, 10, 15, 20, 30, 40),
        "conjecture_holds": abs(rho) > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["metric_value"] is not None for r in results):
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        std_rho = math.sqrt(sum((r["metric_value"] - mean_rho)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if abs(r["metric_value"]) > 0.7) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if abs(r["metric_value"]) <= 0.7), None)
            print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some_results_missing")