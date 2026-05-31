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
    
    def generate_bipartite_state(n):
        state = [[random.random() for _ in range(n)] for _ in range(n)]
        return state
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def communication_complexity(state):
        n = len(state)
        # Simplified model: cc(X) is the sum of absolute values of all elements
        return sum(abs(x) for row in state for x in row)
    
    def minimal_local_index_of_topological_entanglement_rank(state):
        n = len(state)
        max_rank = 0
        for i in range(n):
            for j in range(n):
                submatrix = [row[j:] for row in state[i:]]
                rank = sum(1 for row in submatrix if any(x != 0 for x in row))
                max_rank = max(max_rank, rank)
        return max_rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    cc_values = []
    
    for n in n_values:
        state = generate_bipartite_state(n)
        ranks.append(minimal_local_index_of_topological_entanglement_rank(state))
        cc_values.append(communication_complexity(state))
    
    if not ranks or not cc_values:
        return {
            "metric_name": "mter(X) vs cc(X)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = sum((ranks[i] - mean_ranks) * (cc_values[i] - mean_cc_values) for i in range(len(ranks))) / len(ranks)
    mean_ranks = sum(ranks) / len(ranks)
    mean_cc_values = sum(cc_values) / len(cc_values)
    
    return {
        "metric_name": "mter(X) vs cc(X)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")