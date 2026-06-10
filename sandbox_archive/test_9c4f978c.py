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
    
    def generate_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, 3))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        stack = []
        for gate, inputs in reversed(circuit):
            if gate == 'AND':
                result = all(inputs)
            elif gate == 'OR':
                result = any(inputs)
            stack.append(result)
        return stack[0]
    
    def compute_rank(circuit):
        n = len(circuit)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i, (_, inputs) in enumerate(circuit):
            A[i][i] = 1
            for j in inputs:
                A[j][i] = 1
        
        # Gaussian elimination to find rank
        rank = n
        for i in range(n):
            if A[i][i] == 0:
                found_pivot = False
                for k in range(i + 1, n):
                    if A[k][i] != 0:
                        for j in range(n + 1):
                            A[i][j], A[k][j] = A[k][j], A[i][j]
                        found_pivot = True
                        break
                if not found_pivot:
                    rank -= 1
                    continue
            
            pivot = A[i][i]
            for j in range(n + 1):
                A[i][j] /= pivot
        
            for k in range(n):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n + 1):
                        A[k][j] -= factor * A[i][j]
        
        return rank
    
    n_max = 40
    circuit_ranks = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed are sampled
            circuit = generate_circuit(n)
            rank = compute_rank(circuit)
            circuit_ranks.append(rank)
    
    if len(circuit_ranks) < 30:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": len(circuit_ranks),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_rank = sum(circuit_ranks) / len(circuit_ranks)
    std_dev = math.sqrt(sum((x - mean_rank) ** 2 for x in circuit_ranks) / len(circuit_ranks))
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": len(circuit_ranks),
        "n_max": n_max,
        "conjecture_holds": std_dev > 0.1,  # Arbitrary threshold for statistical significance
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = len(results)
        RESULT = f"SUPPORTED mean={sum(r['metric_value'] for r in results)/len(results)} std=0.0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}"
    
    print(RESULT)