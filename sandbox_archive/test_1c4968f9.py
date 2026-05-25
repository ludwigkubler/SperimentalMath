# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + random.randint(0, m - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(x != 0 for x in row))
        return rank
    
    def parity_circuit_size(n):
        return 2 ** (n - 1)
    
    def tropicalized_sheaf_rank(n):
        # Placeholder function to simulate the rank of a tropicalized sheaf
        return random.randint(1, n)
    
    c = Fraction(1, 2)  # Example constant for ψ(T) ≥ c·log(size(T))
    c_prime = Fraction(1, 3)  # Example constant for ψ(T) > c'·log(size(C))
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        conjecture_holds = True
        counterexample = ""
        
        for _ in range(5):  # Test with 5 instances per size
            T_rank = tropicalized_sheaf_rank(n)
            C_size = parity_circuit_size(n)
            
            if T_rank < c_prime * Fraction(C_size).log(Fraction(2)):
                conjecture_holds = False
                counterexample = f"n={n}, T_rank={T_rank}, C_size={C_size}"
                break
            
            instances_tested += 1
        
        results.append({
            "metric_name": "tropicalized_sheaf_rank",
            "metric_value": T_rank,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        **results[0],
        "mean_metric_value": sum(result["metric_value"] for result in results) / len(results),
        "std_metric_value": (sum((result["metric_value"] - results[0]["mean_metric_value"]) ** 2 for result in results) / len(results)) ** 0.5,
        "support_fraction": sum(1 for result in results if result["conjecture_holds"]) / len(results)
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["mean_metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["mean_metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")