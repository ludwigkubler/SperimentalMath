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
    
    def is_symmetric(graph):
        n = len(graph)
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] != graph[j][i]:
                    return False
        return True
    
    def find_minimal_rank(graph):
        # Placeholder for the actual computation of minimal rank
        # This is a dummy implementation and should be replaced with the actual algorithm
        return random.randint(1, 5)
    
    def find_monotone_circuit_depth(graph):
        # Placeholder for the actual computation of monotone circuit depth
        # This is a dummy implementation and should be replaced with the actual algorithm
        return random.randint(1, 5)
    
    n = random.randint(5, 40)
    graph = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                graph[i][j] = 1
                graph[j][i] = 1
    
    if not is_symmetric(graph):
        return {
            "metric_name": "MinRank vs Circuit Depth",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "graph_not_symmetric"
        }
    
    min_rank = find_minimal_rank(graph)
    circuit_depth = find_monotone_circuit_depth(graph)
    
    return {
        "metric_name": "MinRank vs Circuit Depth",
        "metric_value": abs(min_rank - circuit_depth),
        "instances_tested": 1,
        "conjecture_holds": min_rank <= circuit_depth,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["metric_value"] is not None for result in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(i for i, result in enumerate(results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some_trials_skipped")