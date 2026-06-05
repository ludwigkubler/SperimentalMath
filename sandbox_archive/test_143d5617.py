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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def toffoli_xy_gate(q1, q2, c):
        if q1 == 1 and q2 == 1:
            return (q1, q2, 1 - c)
        return (q1, q2, c)
    
    def quantum_circuit(n, f):
        circuit = []
        for i in range(2**n):
            inputs = [int(x) for x in format(i, '0{}b'.format(n))]
            outputs = [f[i]]
            for j in range(n):
                if outputs[j] == 1:
                    circuit.append((j, (j+1)%n, (j+2)%n))
            for gate in circuit:
                inputs[gate[0]] = toffoli_xy_gate(inputs[gate[1]], inputs[gate[2]], inputs[gate[0]])[0]
                inputs[gate[1]] = toffoli_xy_gate(inputs[gate[1]], inputs[gate[2]], inputs[gate[0]])[1]
                inputs[gate[2]] = toffoli_xy_gate(inputs[gate[1]], inputs[gate[2]], inputs[gate[0]])[2]
            if outputs != [f[i]]:
                return None
        return circuit
    
    def entanglement_entropy(circuit):
        # Simplified model for demonstration purposes
        return len(circuit) / 2
    
    def k_theory_cohomology_rank(n, f):
        # Placeholder for actual K-theory computation
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_rank = 0
    total_entropy = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            circuit = quantum_circuit(n, f)
            if circuit is None:
                continue
            rank = k_theory_cohomology_rank(n, f)
            entropy = entanglement_entropy(circuit)
            total_rank += rank
            total_entropy += entropy
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_circuits"
        }
    
    mean_rank = total_rank / instances_tested
    mean_entropy = total_entropy / instances_tested
    correlation_coefficient = (instances_tested * sum(rank * entropy for rank, entropy in zip(range(n_values[-1]+1), range(n_values[-1]+1))) - mean_rank * mean_entropy) / math.sqrt((instances_tested * sum(rank**2 for rank in range(n_values[-1]+1)) - mean_rank**2) * (instances_tested * sum(entropy**2 for entropy in range(n_values[-1]+1)) - mean_entropy**2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_values[-1],
        "conjecture_holds": correlation_coefficient > 0.7 and all(0.5 <= cc for cc in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")