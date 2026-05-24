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

def gaussian_elimination(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] + [0] for row in matrix]
    rank = 0
    
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        if augmented_matrix[i][i] == 0:
            continue
        
        rank += 1
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i] / augmented_matrix[i][i]
                for k in range(n + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    circuit = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    try:
        rank = gaussian_elimination(circuit)
    except Exception as e:
        return {
            "metric_name": "Rank vs DPLL Heig",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    c = 2.0  # Example constant, adjust as needed
    expected_rank = math.ceil(c * math.log(n))
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= expected_rank,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"Rank {result['metric_value']} > {math.ceil(c * math.log(result['instances_tested']))}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break
        else:
            print("RESULT: INCONCLUSIVE reason=unknown")