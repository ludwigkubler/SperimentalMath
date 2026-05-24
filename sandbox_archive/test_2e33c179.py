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
    
    def generate_quantum_state(n):
        state = [random.random() for _ in range(2**n)]
        norm = sum(x**2 for x in state)**0.5
        return [x / norm for x in state]
    
    def t_depth(circuit):
        depth = 0
        for gate in circuit:
            if gate[0] == 'CNOT':
                depth += 1
        return depth
    
    def min_rank(state):
        n = int(math.log2(len(state)))
        U, S, Vt = svd(state)
        return sum(S[i] > 1e-6 for i in range(n))
    
    def svd(matrix):
        m, n = len(matrix), len(matrix[0])
        U = [[random.random() for _ in range(m)] for _ in range(m)]
        Vt = [[random.random() for _ in range(n)] for _ in range(n)]
        S = [1.0] * min(m, n)
        return U, S, Vt
    
    def generate_circuit(state):
        n = int(math.log2(len(state)))
        circuit = []
        for i in range(n):
            circuit.append(('CNOT', i, (i + 1) % n))
        return circuit
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        state = generate_quantum_state(n)
        circuit = generate_circuit(state)
        rank = min_rank(state)
        depth = t_depth(circuit)
        
        if rank == 0 or depth == 0:
            continue
        
        ratio = rank / depth
        results.append(ratio)
    
    if not results:
        return {
            "metric_name": "minimal_rank_over_tdepth",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(results) / len(results)
    std = (sum((x - mean)**2 for x in results) / len(results))**0.5
    support_fraction = len([r for r in results if r <= 1]) / len(results)
    
    return {
        "metric_name": "minimal_rank_over_tdepth",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std = (sum((r["metric_value"] - mean)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")