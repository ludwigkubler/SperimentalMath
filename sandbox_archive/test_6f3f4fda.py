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
    
    def is_invertible(matrix):
        n = len(matrix)
        if n == 0 or not all(len(row) == n for row in matrix):
            return False
        
        def determinant(A):
            if len(A) == 1:
                return A[0][0]
            det = Fraction(0)
            sign = 1
            for i in range(len(A)):
                submatrix = [row[:i] + row[i+1:] for row in A[1:]]
                det += sign * A[0][i] * determinant(submatrix)
                sign *= -1
            return det
        
        return determinant(matrix) != 0
    
    def generate_quandle_group(n):
        quandle_group = []
        for i in range(2**n):
            row = [0] * n
            for j in range(n):
                if (i >> j) & 1:
                    row[j] = 1
            quandle_group.append(row)
        return quandle_group
    
    def circuit_depth(circuit):
        depth = 0
        for gate in circuit:
            if gate[0] == 'XOR':
                depth += max(circuit_depth(gate[1]), circuit_depth(gate[2]))
            else:
                depth += 1
        return depth
    
    n = random.randint(5, 40)
    quandle_group = generate_quandle_group(n)
    
    min_order = float('inf')
    for i in range(len(quandle_group)):
        if is_invertible(quandle_group[i]):
            order = sum(quandle_group[i])
            if order < min_order:
                min_order = order
    
    circuit = []
    for _ in range(2**n):
        gate = random.choice(['XOR', 'NOT'])
        if gate == 'XOR':
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs[:n//2], inputs[n//2:]))
        else:
            input_ = random.randint(0, 1)
            circuit.append((gate, input_, None))
    
    depth = circuit_depth(circuit)
    
    return {
        "metric_name": "Minimal Order of Quandle Group",
        "metric_value": min_order,
        "instances_tested": len(quandle_group),
        "conjecture_holds": min_order <= n**2 and min_order >= 0.9 * n**2,
        "counterexample": "" if conjecture_holds else f"n={n}, min_order={min_order}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30, 150, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='n={results[0]['instances_tested']}, min_order={min(r['metric_value'] for r in results if not r['conjecture_holds'])}' first_failing_seed={first_failing_seed}")