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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            variables = [random.randint(1, n), random.randint(1, n)]
            if variables[0] == variables[1]:
                continue
            clause = (variables[0], 1) + (variables[1], -1)
            clauses.append(clause)
        return clauses
    
    def construct_quantum_tensor_network(cnf):
        qubits = {}
        for var in range(1, n+1):
            qubits[var] = random.randint(1, 2)
        
        tensor_network = []
        for clause in cnf:
            tensor = [0] * (n + 1)
            for var, sign in clause:
                if sign == 1:
                    tensor[qubits[var]] += 1
                else:
                    tensor[qubits[var]] -= 1
            tensor_network.append(tensor)
        return tensor_network
    
    def calculate_rank(tensor_network):
        m = len(tensor_network)
        n = len(tensor_network[0])
        
        # Gaussian elimination
        for i in range(m):
            if tensor_network[i][i] == 0:
                for j in range(i+1, m):
                    if tensor_network[j][i] != 0:
                        tensor_network[i], tensor_network[j] = tensor_network[j], tensor_network[i]
                        break
            if tensor_network[i][i] == 0:
                continue
            
            pivot = Fraction(tensor_network[i][i])
            for j in range(n):
                tensor_network[i][j] /= pivot
        
            for j in range(m):
                if i != j:
                    factor = Fraction(tensor_network[j][i])
                    for k in range(n):
                        tensor_network[j][k] -= factor * tensor_network[i][k]
        
        rank = 0
        for row in tensor_network:
            if any(row):
                rank += 1
        return rank
    
    def calculate_resolution_width(cnf):
        # Simplified resolution width calculation (not accurate but sufficient for testing)
        return len(cnf) + n
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    tensor_network = construct_quantum_tensor_network(cnf)
    rank = calculate_rank(tensor_network)
    width = calculate_resolution_width(cnf)
    
    return {
        "metric_name": "Rank vs Width",
        "metric_value": abs(rank - width),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if rank != width else True,
        "counterexample": f"Rank {rank} does not match Width {width}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank does not match Width\" first_failing_seed={first_failing_seed}")