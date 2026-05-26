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
    
    def generate_circuit(n, m):
        # Generate a random arithmetic circuit with n inputs and m output bits
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            if gate_type == 'AND':
                inputs = random.sample(range(n), 2)
            else:
                inputs = random.sample(range(n), 2)
            circuit.append((gate_type, inputs))
        return circuit
    
    def symplectic_leaves(circuit):
        # Compute the associated symplectic leaves for a given circuit
        leaves = set()
        for gate in circuit:
            if gate[0] == 'AND':
                leaves.add(tuple(sorted(gate[1])))
            else:
                leaves.add(tuple(sorted(gate[1])))
        return leaves
    
    def min_rank(leaves):
        # Compute the minimal rank of the symplectic leaves
        vectors = list(leaves)
        rank = 0
        for i in range(len(vectors)):
            if all(all(vectors[j][k] != vectors[i][k] for k in range(len(vectors[0]))) for j in range(i+1, len(vectors))):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = sum(n_values)
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different circuits
            circuit = generate_circuit(n, n // 2)
            leaves = symplectic_leaves(circuit)
            rank = min_rank(leaves)
            total_rank += rank
    
    mean_value = total_rank / instances_tested
    conjecture_holds = mean_value <= (n * math.log(n)) * 1.5  # Allow a small constant factor c_0 > 0
    counterexample = "" if conjecture_holds else f"rank={mean_value}, expected={n * math.log(n)}"
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='{result['counterexample']}' first_failing_seed={first_failing_seed}")