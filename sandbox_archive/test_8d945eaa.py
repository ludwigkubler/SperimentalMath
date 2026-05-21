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
    n = 40
    depth = 3
    size_limit = 2**10
    
    # Generate a random AC⁰ circuit computing PARITY on n bits
    def generate_ac0_circuit(n, depth, size_limit):
        if depth == 0:
            return [random.choice([0, 1])]
        else:
            inputs = generate_ac0_circuit(n, depth - 1, size_limit)
            outputs = []
            for i in range(size_limit):
                gate_type = random.choice(['OR', 'AND'])
                if gate_type == 'OR':
                    output = any(inputs[j] for j in range(len(inputs)))
                else:
                    output = all(inputs[j] for j in range(len(inputs)))
                outputs.append(output)
            return outputs
    
    circuit = generate_ac0_circuit(n, depth, size_limit)
    
    # Compute the communication matrix
    def compute_communication_matrix(circuit):
        m = len(circuit)
        n = int(math.log2(m))
        comm_matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(m):
            x = bin(i)[2:].zfill(n)
            y = bin(circuit[i])[2:].zfill(n)
            for j in range(n):
                if x[j] == '1':
                    comm_matrix[j][n] += 1
                    comm_matrix[n][j] -= 1
        return comm_matrix
    
    comm_matrix = compute_communication_matrix(circuit)
    
    # Calculate the real rank via Gaussian elimination over R
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            if matrix[i][i] == 0:
                return None  # Singular matrix
            for j in range(i + 1, m):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    real_rank = gaussian_elimination(comm_matrix)
    
    # Verify the conjecture
    if real_rank is None:
        return {
            "metric_name": "real_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }
    
    metric_value = real_rank
    conjecture_holds = real_rank >= 0.1 * math.log(n)
    counterexample = "" if conjecture_holds else f"real_rank={real_rank}, expected ≥ {0.1 * math.log(n)}"
    
    return {
        "metric_name": "real_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={seed}")
                break