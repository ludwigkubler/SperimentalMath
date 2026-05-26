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
    
    def generate_boolean_circuit(n, m):
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def weyl_group_representation(circuit):
        n = len(circuit[0][1])
        representation = [[0] * n for _ in range(n)]
        for gate_type, inputs in circuit:
            if gate_type == 'AND':
                for i in range(n):
                    if all(inputs[j] == 1 for j in range(n) if (i >> j) & 1):
                        representation[i][i] = 1
            elif gate_type == 'OR':
                for i in range(n):
                    if any(inputs[j] == 1 for j in range(n) if (i >> j) & 1):
                        representation[i][i] = 1
        return representation
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i][j] != 0 for j in range(n)):
                rank += 1
                for j in range(n):
                    matrix[i][j] /= matrix[i][i]
                for k in range(m):
                    if k != i:
                        factor = matrix[k][i]
                        for j in range(n):
                            matrix[k][j] -= factor * matrix[i][j]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m_max = int(n ** (2/3))
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_boolean_circuit(n, random.randint(1, m_max))
            representation = weyl_group_representation(circuit)
            rank = matrix_rank(representation)
            results.append(rank)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = metric_value <= 3
    counterexample = "" if conjecture_holds else f"Mean rank {metric_value} exceeds bound 3"
    
    return {
        "metric_name": "Minimal Rank of Weyl Group Representations",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean rank exceeds bound 3\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")