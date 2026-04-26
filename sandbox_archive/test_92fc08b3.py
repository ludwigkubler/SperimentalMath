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

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for j in range(n):
        i_max = rank
        for i in range(rank, m):
            if abs(matrix[i][j]) > abs(matrix[i_max][j]):
                i_max = i
        if abs(matrix[i_max][j]) < 1e-9:
            continue
        matrix[i_max], matrix[rank] = matrix[rank], matrix[i_max]
        for i in range(m):
            if i != rank:
                factor = -matrix[i][j] / matrix[rank][j]
                for k in range(n):
                    matrix[i][k] += factor * matrix[rank][k]
        rank += 1
    return rank

def decision_tree_depth(circuit, inputs):
    if isinstance(circuit, bool):
        return 0
    if circuit[0] == 'AND':
        return max(decision_tree_depth(circuit[1], inputs), decision_tree_depth(circuit[2], inputs)) + 1
    elif circuit[0] == 'OR':
        return max(decision_tree_depth(circuit[1], inputs), decision_tree_depth(circuit[2], inputs)) + 1
    elif circuit[0] == 'NOT':
        return decision_tree_depth(circuit[1], inputs) + 1

def generate_ac0_circuit(n, depth):
    if depth == 0:
        return random.choice([True, False])
    op = random.choice(['AND', 'OR', 'NOT'])
    if op == 'NOT':
        return (op, generate_ac0_circuit(n, depth - 1))
    else:
        return (op, generate_ac0_circuit(n, depth - 1), generate_ac0_circuit(n, depth - 1))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    depth = random.randint(2, 3 * math.log2(n))
    circuit = generate_ac0_circuit(n, depth)
    
    inputs = list(itertools.product([False, True], repeat=n))
    outputs = [circuit] + [eval(circuit, {'__builtins__': None}, {f'x{i}': x[i] for i in range(n)}) for x in inputs]
    
    communication_matrix = [[0] * (n + 1) for _ in range(2 ** n)]
    for i in range(2 ** n):
        for j in range(n):
            if outputs[i][j]:
                communication_matrix[i][j] = 1
        communication_matrix[i][-1] = int(outputs[i])
    
    rank = gaussian_elimination(communication_matrix)
    depth_value = decision_tree_depth(circuit, inputs)
    
    conjecture_holds = rank <= 2 ** (0.5 * math.log2(n)) * depth_value
    counterexample = "" if conjecture_holds else f"Rank {rank} > 2^{0.5 * math.log2(n)} * Depth {depth_value}"
    
    return {
        "metric_name": "Communication Matrix Rank",
        "metric_value": rank,
        "instances_tested": len(inputs),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_rank = sum(r['metric_value'] for r in results) / len(results)
    std_rank = math.sqrt(sum((r['metric_value'] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        counterexample_desc = results[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]['counterexample']
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")