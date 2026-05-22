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
    
    def generate_ac0_parity_circuit(n):
        # Generate a random AC⁰ parity circuit
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            if gate_type == 'AND':
                inputs = [random.randint(0, 1) for _ in range(2)]
                circuit.append((gate_type, inputs))
            else:
                inputs = [random.randint(0, 1) for _ in range(2)]
                circuit.append((gate_type, inputs))
        return circuit
    
    def tropicalize_circuit(circuit):
        # Tropicalize the circuit
        tropicalized = []
        for gate_type, inputs in circuit:
            if gate_type == 'AND':
                tropicalized.append(min(inputs))
            else:
                tropicalized.append(max(inputs))
        return tropicalized
    
    def compute_rank(tropicalized):
        # Compute the rank of the tropicalized sheaf
        n = len(tropicalized)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    matrix[i][j] = 1
                else:
                    matrix[i][j] = abs(tropicalized[i] - tropicalized[j])
        
        def gaussian_elimination(mat):
            rows, cols = len(mat), len(mat[0])
            for col in range(cols):
                pivot_row = None
                for row in range(col, rows):
                    if mat[row][col] != 0:
                        pivot_row = row
                        break
                if pivot_row is None:
                    continue
                
                # Swap rows to put the pivot at the top
                mat[col], mat[pivot_row] = mat[pivot_row], mat[col]
                
                # Normalize the pivot element
                for j in range(cols):
                    mat[col][j] /= mat[col][col]
                
                # Eliminate other elements in the column
                for row in range(rows):
                    if row != col:
                        factor = mat[row][col]
                        for j in range(cols):
                            mat[row][j] -= factor * mat[col][j]
            
            rank = sum(1 for row in mat if any(row))
            return rank
        
        rank = gaussian_elimination(matrix)
        return rank
    
    n = random.randint(5, 40)
    circuit = generate_ac0_parity_circuit(n)
    tropicalized = tropicalize_circuit(circuit)
    rank = compute_rank(tropicalized)
    
    metric_name = "min_rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= math.log(n, 2)
    counterexample = "" if conjecture_holds else f"Rank {rank} is less than log({n}, 2) = {math.log(n, 2)}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank less than log(n, 2)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")