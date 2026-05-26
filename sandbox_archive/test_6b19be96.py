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
    
    def twisted_group_representation(protocol):
        n = len(protocol)
        if n < 5 or n > 40:
            return None
        
        # Define the mapping from protocol to group elements
        # This is a placeholder; replace with actual mapping logic
        group_elements = [random.randint(1, 2) for _ in range(n)]
        
        # Calculate the minimal rank of the induced matrix representation
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if group_elements[i] == 1 and group_elements[j] == 1:
                    matrix[i][j] = 1
        
        # Compute the rank of the matrix
        def gaussian_elimination(mat):
            rows, cols = len(mat), len(mat[0])
            rank = 0
            for j in range(cols):
                i_max = -1
                for i in range(rank, rows):
                    if mat[i][j] != 0:
                        i_max = i
                        break
                if i_max == -1:
                    continue
                
                mat[rank], mat[i_max] = mat[i_max], mat[rank]
                
                for i in range(rows):
                    if i != rank and mat[i][j] != 0:
                        factor = Fraction(mat[i][j], mat[rank][j])
                        for k in range(cols):
                            mat[i][k] -= factor * mat[rank][k]
                
                rank += 1
            return rank
        
        rank = gaussian_elimination(matrix)
        return rank
    
    def communication_complexity(protocol):
        n = len(protocol)
        # Placeholder for actual communication complexity calculation
        return random.randint(1, n**2)
    
    protocol = [random.choice([0, 1]) for _ in range(random.randint(5, 40))]
    rank = twisted_group_representation(protocol)
    if rank is None:
        return {
            "metric_name": "minimal_rank",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    cc = communication_complexity(protocol)
    tau_R = rank
    n_bits = len(protocol)
    
    # Check if the conjecture holds
    expected_rank = math.floor(n_bits**2 * math.log2(n_bits))
    margin = 0.05 * expected_rank
    conjecture_holds = tau_R >= expected_rank and abs(tau_R - expected_rank) <= margin
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": tau_R,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"rank={tau_R}, expected={expected_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")