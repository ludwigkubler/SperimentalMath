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
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(matrix[i][i])
            for j in range(cols):
                matrix[i][j] /= factor
            for j in range(rows):
                if i != j:
                    factor = Fraction(matrix[j][i])
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def compute_minimal_rank(n):
        # Generate a random AC⁰ circuit for the PARITY function
        circuit = []
        for i in range(n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(gate)]
            circuit.append((gate, inputs))
        
        # Convert the circuit to an algebraic curve (simplified example)
        # This is a placeholder; actual computation would be more complex
        curve = []
        for gate, inputs in circuit:
            if gate == 'AND':
                curve.append(min(inputs))
            elif gate == 'OR':
                curve.append(max(inputs))
        
        # Compute the minimal rank of the algebraic curve
        matrix = [[curve[i] ** j for j in range(n+1)] for i in range(n+1)]
        return gaussian_elimination(matrix)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    for n in n_values:
        rank = compute_minimal_rank(n)
        ranks.append(rank)
    
    mean_rank = sum(ranks) / len(ranks)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in ranks) / len(ranks))
    
    conjecture_holds = all(rank >= n * log2(n) for rank, n in zip(ranks, n_values))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")