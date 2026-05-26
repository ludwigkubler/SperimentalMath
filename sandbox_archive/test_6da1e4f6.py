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
    
    def generate_boolean_circuit(n, s):
        circuit = []
        for _ in range(s):
            gate_type = random.choice(['AND', 'OR'])
            if gate_type == 'AND':
                inputs = [random.randint(0, 1) for _ in range(2)]
            else:
                inputs = [random.randint(0, 1) for _ in range(2)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = inputs[0] and inputs[1]
            else:
                result = inputs[0] or inputs[1]
            stack.append(result)
        return stack.pop()
    
    def tropicalize_poisson_tensor_product(circuit):
        n = len(circuit)
        values = set()
        for tau in itertools.product([0, 1], repeat=n):
            value = evaluate_circuit([(gate_type, [tau[i] for i in inputs]) for gate_type, inputs in circuit])
            values.add(value)
        return values
    
    def min_rank(values):
        matrix = []
        for value in values:
            row = [int(bit) for bit in bin(value)[2:].zfill(n)]
            matrix.append(row)
        
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(rank, len(matrix))):
                for j in range(rank, len(matrix)):
                    if matrix[j][i] != 0:
                        matrix[j], matrix[rank] = matrix[rank], matrix[j]
                        break
                for j in range(len(matrix)):
                    if j != rank:
                        factor = -matrix[j][i] / matrix[rank][i]
                        for k in range(n):
                            matrix[j][k] += factor * matrix[rank][k]
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            s = random.randint(n, min(40, n * 4))
            circuit = generate_boolean_circuit(n, s)
            values = tropicalize_poisson_tensor_product(circuit)
            rank = min_rank(values)
            results.append((n, s, rank))
    
    if not results:
        return {
            "metric_name": "min_rank",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_rank = sum(rank for _, _, rank in results)
    mean_rank = total_rank / len(results)
    max_s = max(s for _, s, _ in results)
    f_n = math.ceil(max_s ** 0.5)
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": mean_rank <= f_n,
        "counterexample": "" if mean_rank <= f_n else f"n={n}, s={max_s}, rank={mean_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")