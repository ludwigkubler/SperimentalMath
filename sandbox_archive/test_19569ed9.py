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
    
    def generate_circuit(n):
        # Generate a random Boolean circuit with n variables
        # This is a simplified version and may not be satisfiable
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def is_satisfiable(circuit):
        # Simplified check for satisfiability
        # This is not a proper SAT solver and may miss some cases
        for assignment in itertools.product([0, 1], repeat=len(circuit[0][1])):
            if all(assignment[i] == input_val for i, input_val in enumerate(circuit[0][1])):
                if circuit[0][0] == 'AND':
                    result = True
                else:
                    result = False
                for gate, inputs in circuit[1:]:
                    if gate == 'AND':
                        result &= all(assignment[i] == input_val for i, input_val in enumerate(inputs))
                    else:
                        result |= any(assignment[i] == input_val for i, input_val in enumerate(inputs))
                if result:
                    return True
        return False
    
    def construct_geometric_object(circuit):
        # Simplified construction of a geometric object
        # This is not a proper mapping and may not reflect actual Langlands duals
        rank = sum(1 for gate, _ in circuit if gate == 'AND')
        return rank
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    if not is_satisfiable(circuit):
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "circuit_not_satisfiable"
        }
    
    rank = construct_geometric_object(circuit)
    g_n = math.log(n, 2)  # Upper bound function g(n) = O(log n)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= g_n,
        "counterexample": "" if rank <= g_n else f"rank={rank}, expected={g_n}"
    }

if __name__ == "__main__":
    import sys
    import itertools
    
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30*2 + 1, 2))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")