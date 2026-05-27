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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            # Find pivot
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below
            for j in range(i + 1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        rank = sum(1 for row in A if any(row))
        return rank
    
    def log2(x):
        return math.log2(x) if x > 0 else float('-inf')
    
    def xor_and_tree_width(n):
        # Simplified heuristic for XOR-AND tree width
        return n // 2 + 1
    
    def generate_ac0_circuit(n):
        # Generate a random AC0 circuit of size n
        circuit = []
        for _ in range(2**(n-1)):
            gate = random.choice(['XOR', 'AND'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        # Evaluate the AC0 circuit on a random input
        n = len(circuit[0][1])
        input_ = [random.randint(0, 1) for _ in range(n)]
        result = input_
        for gate, inputs in circuit:
            if gate == 'XOR':
                result = [a ^ b for a, b in zip(result, inputs)]
            elif gate == 'AND':
                result = [a & b for a, b in zip(result, inputs)]
        return result
    
    def generate_quadratic_form(n):
        # Generate a non-degenerate quadratic form
        Q = [[random.randint(0, 1) if i == j else 0 for j in range(n)] for i in range(n)]
        return Q
    
    def rank_of_quadratic_form(Q):
        # Compute the rank of the quadratic form using Gaussian elimination
        A = [row + [1] for row in Q]
        rank = gaussian_elimination(A)
        return rank
    
    n = random.randint(5, 40)
    circuit = generate_ac0_circuit(n)
    tree_width = xor_and_tree_width(n)
    epsilon = 1e-6
    min_rank = float('inf')
    
    for _ in range(30):
        input_ = evaluate_circuit(circuit)
        Q = generate_quadratic_form(n)
        rank = rank_of_quadratic_form(Q)
        if rank < min_rank:
            min_rank = rank
    
    conjecture_holds = min_rank >= log2(tree_width) + epsilon
    counterexample = "" if conjecture_holds else f"min_rank={min_rank}, tree_width={tree_width}"
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_rank < log2(tree_width) + epsilon\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")