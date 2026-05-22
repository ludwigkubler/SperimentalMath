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

def generate_ac0_circuit(n, max_gates):
    if n <= 1 or max_gates < 2:
        return []
    
    circuit = []
    inputs = list(range(n))
    for _ in range(max_gates - 1):
        gate_type = random.choice(['NOT', 'XOR'])
        if gate_type == 'NOT':
            input_index = random.choice(inputs)
            output_index = n + len(circuit)
            circuit.append((input_index, output_index, 'NOT'))
            inputs.append(output_index)
        else:
            input_indices = random.sample(sorted(inputs), 2)
            output_index = n + len(circuit)
            circuit.append((input_indices[0], input_indices[1], output_index, 'XOR'))
            inputs.append(output_index)
    
    return circuit

def generate_non_associative_algebra(n):
    F2 = [0, 1]
    algebra = [[F2[(i + j) % 2] for j in range(n)] for i in range(n)]
    return algebra

def calculate_symplectic_form(algebra):
    n = len(algebra)
    symplectic_form = [[F2[algebra[i][j] * algebra[j][i]] for j in range(n)] for i in range(n)]
    return symplectic_form

def calculate_minimal_rank(symplectic_form):
    n = len(symplectic_form)
    rank = 0
    for row in symplectic_form:
        if any(row[i] != 0 for i in range(n)):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_ac0_circuit(n, max_gates=40)
        if not circuit:
            continue
        
        algebra = generate_non_associative_algebra(n)
        symplectic_form = calculate_symplectic_form(algebra)
        minimal_rank = calculate_minimal_rank(symplectic_form)
        
        results.append({
            "n": n,
            "gate_count": len(circuit),
            "minimal_rank": minimal_rank
        })
    
    if not results:
        return {
            "metric_name": "Gate Count vs Minimal Rank",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid AC0 circuits generated"
        }
    
    gate_counts = [result["gate_count"] for result in results]
    minimal_ranks = [result["minimal_rank"] for result in results]
    
    mean_gate_count = sum(gate_counts) / len(gate_counts)
    std_gate_count = math.sqrt(sum((x - mean_gate_count) ** 2 for x in gate_counts) / len(gate_counts))
    mean_minimal_rank = sum(minimal_ranks) / len(minimal_ranks)
    std_minimal_rank = math.sqrt(sum((x - mean_minimal_rank) ** 2 for x in minimal_ranks) / len(minimal_ranks))
    
    correlation_coefficient = sum((gate_counts[i] - mean_gate_count) * (minimal_ranks[i] - mean_minimal_rank) for i in range(len(gate_counts))) / (len(gate_counts) * std_gate_count * std_minimal_rank)
    
    return {
        "metric_name": "Gate Count vs Minimal Rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": abs(correlation_coefficient) > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
        if not result["conjecture_holds"]:
            break
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Gate count does not match minimal rank\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=No valid AC0 circuits generated")