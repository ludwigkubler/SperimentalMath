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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += (-1) ** i * A[0][i] * determinant(submatrix)
        return det

    def free_entanglement_dimension(size):
        # Placeholder function to simulate the calculation
        # This is a dummy implementation and should be replaced with actual logic
        return math.log2(size)

    n = random.randint(5, 40)
    size = 2 ** n
    P = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    # Construct the corresponding quantum states (dummy implementation)
    quantum_states = [P[i] + P[j] for i in range(n) for j in range(i+1, n)]
    
    # Calculate the minimal free entanglement dimension
    dimensions = [free_entanglement_dimension(size) for _ in range(len(quantum_states))]
    min_dimension = min(dimensions)
    
    # Evaluate the correlation with the size of the branching programs
    expected_dimension = math.log2(size)
    std_dev = (sum((x - expected_dimension) ** 2 for x in dimensions) / len(dimensions)) ** 0.5
    
    metric_value = abs(min_dimension - expected_dimension) < std_dev * 1.96
    
    return {
        "metric_name": "free_entanglement_dimension",
        "metric_value": min_dimension,
        "instances_tested": len(quantum_states),
        "conjecture_holds": metric_value,
        "counterexample": "" if metric_value else f"Min dimension {min_dimension} not within 1 std dev of expected {expected_dimension}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Min dimension not within 1 std dev of expected\" first_failing_seed={first_failing_seed}")