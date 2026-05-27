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
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for j in range(n):
            i_max = rank
            for i in range(rank, m):
                if abs(matrix[i][j]) > abs(matrix[i_max][j]):
                    i_max = i
            if matrix[i_max][j] == 0:
                continue
            matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
            for i in range(m):
                if i != rank:
                    factor = -matrix[i][j] / matrix[rank][j]
                    for k in range(n):
                        matrix[i][k] += factor * matrix[rank][k]
            rank += 1
        return rank
    
    def tseitin_circuit(width):
        n = width + 2
        variables = list(range(1, n))
        clauses = []
        
        # Add clauses for each variable
        for i in range(n - 2):
            clauses.append([variables[i], variables[n - 2]])
        
        # Add clauses for the OR gate
        for i in range(n - 3):
            clauses.append([-variables[i], -variables[n - 3]])
        
        # Add clauses for the AND gate
        for i in range(n - 4):
            clauses.append([variables[i], variables[n - 4]])
        
        return clauses
    
    def motivic_homology_rank(clauses):
        n = len(clauses)
        m = len(variables) + n
        matrix = [[0] * (m + 1) for _ in range(m)]
        
        for i, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    matrix[i][var - 1] = 1
                else:
                    matrix[i][-var - 1] = 1
        
        return gaussian_elimination(matrix)
    
    width = random.randint(5, 40)
    circuit = tseitin_circuit(width)
    rank = motivic_homology_rank(circuit)
    
    metric_name = "motivic_homology_rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= 2 ** (width / 2)
    counterexample = "" if conjecture_holds else f"Rank {rank} is less than 2^{width/2}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results) or support_fraction < 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank less than 2^(w/2)\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")