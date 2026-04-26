# auto-injected by SEC sandbox
import itertools
import collections
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
import sys
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            if rank >= m:
                break
            pivot_row = rank
            while pivot_row < m and matrix[pivot_row][i] == 0:
                pivot_row += 1
            if pivot_row == m:
                continue
            matrix[rank], matrix[pivot_row] = matrix[pivot_row], matrix[rank]
            for j in range(n):
                if j != i:
                    factor = matrix[j][i] / matrix[rank][i]
                    for k in range(m):
                        matrix[j][k] -= factor * matrix[rank][k]
            rank += 1
        return rank
    
    def decision_tree_depth(circuit):
        if isinstance(circuit, bool):
            return 0
        elif circuit == 'OR':
            return 1 + max(decision_tree_depth(child) for child in circuit)
        elif circuit == 'AND':
            return 1 + sum(decision_tree_depth(child) for child in circuit)
        else:
            raise ValueError("Invalid circuit")
    
    def generate_ac0_circuit(n):
        if n == 1:
            return random.choice([True, False])
        if random.random() < 0.5:
            return ('OR', generate_ac0_circuit(n-1), generate_ac0_circuit(n-1))
        else:
            return ('AND', generate_ac0_circuit(n-1), generate_ac0_circuit(n-1))
    
    n = random.choice([5, 8, 11, 14])
    circuit = generate_ac0_circuit(n)
    depth = decision_tree_depth(circuit)
    
    # Convert circuit to communication matrix
    m = 2 ** n
    communication_matrix = [[0] * m for _ in range(m)]
    def evaluate_circuit(node):
        if isinstance(node, bool):
            return [node]
        elif node == 'OR':
            left_values = evaluate_circuit(node[1])
            right_values = evaluate_circuit(node[2])
            return [a or b for a in left_values for b in right_values]
        elif node == 'AND':
            left_values = evaluate_circuit(node[1])
            right_values = evaluate_circuit(node[2])
            return [a and b for a in left_values for b in right_values]
        else:
            raise ValueError("Invalid circuit")
    
    values = evaluate_circuit(circuit)
    for i in range(m):
        communication_matrix[i][i] = 1
        for j in range(i + 1, m):
            if values[i] == values[j]:
                communication_matrix[i][j] = 1
                communication_matrix[j][i] = 1
    
    rank = gaussian_elimination(communication_matrix)
    
    conjecture_holds = rank <= 2 ** (0.5 * math.log2(n)) * depth
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "rank_over_depth",
        "metric_value": rank / depth,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [11, 23, 37, 53, 71]
    
    results = []
    total_rank_over_depth = 0
    total_instances_tested = 0
    support_count = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        total_rank_over_depth += trial_result["metric_value"] * trial_result["instances_tested"]
        total_instances_tested += trial_result["instances_tested"]
        if trial_result["conjecture_holds"]:
            support_count += 1
    
    mean_rank_over_depth = total_rank_over_depth / total_instances_tested
    support_fraction = support_count / len(seeds)
    
    print(json.dumps({"TRIAL": {"seed": seed, **trial_result}} for seed, trial_result in zip(seeds, results)))
    
    if support_fraction >= 0.8:
        result = "SUPPORTED"
    elif any(not trial["conjecture_holds"] for trial in results):
        result = "FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed=" + str(seeds[results.index(next(r for r in results if not r["conjecture_holds"]))])
    else:
        result = "INCONCLUSIVE mapping_undefined"
    
    print(result + f" mean={mean_rank_over_depth} std=0 support_fraction={support_fraction}")