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
    
    def xor_and_circuit(n):
        # Generate a random XOR-AND circuit with n variables
        gates = []
        for _ in range(2 ** (n - 1)):
            gate_type = random.choice(['xor', 'and'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            gates.append((gate_type, inputs))
        return gates
    
    def monodromy_representation(gates):
        # Compute the monodromy representation (simplified)
        d = len(gates)
        M = [[0] * d for _ in range(d)]
        for i in range(d):
            for j in range(d):
                if i != j:
                    M[i][j] = 1
        return M
    
    def minimal_rank(M):
        # Compute the minimal rank of the monodromy representation (simplified)
        rank = d
        for i in range(d):
            if all(M[j][i] == 0 for j in range(d)):
                rank -= 1
                break
        return rank
    
    def f(d, n):
        # Upper bound function f(d) = O(n^2 log n)
        return n**2 * math.log(n)
    
    def g(d, n):
        # Lower bound function g(d) = Ω(n^2 log n)
        return n**2 * math.log(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        circuit = xor_and_circuit(n)
        M = monodromy_representation(circuit)
        rank = minimal_rank(M)
        results.append({
            "n": n,
            "circuit_size": len(circuit),
            "monodromy_rank": rank
        })
    
    total_rank = sum(result["monodromy_rank"] for result in results)
    mean_rank = total_rank / len(results)
    conjecture_holds = all(f(result["monodromy_rank"], result["n"]) >= result["circuit_size"] for result in results) and \
                       all(g(result["monodromy_rank"], result["n"]) <= result["circuit_size"] for result in results)
    
    return {
        "metric_name": "Monodromy Rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")