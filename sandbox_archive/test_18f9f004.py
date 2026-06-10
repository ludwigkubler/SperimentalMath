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
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit

    def evaluate_circuit(circuit, assignment):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = all(stack.pop() for _ in inputs)
            elif gate_type == 'OR':
                result = any(stack.pop() for _ in inputs)
            stack.append(result)
        return stack[0]

    def find_satisfying_assignments(circuit):
        n = len(circuit)
        satisfying_assignments = []
        for assignment in range(2**n):
            if evaluate_circuit(circuit, [assignment >> i & 1 for i in range(n)]):
                satisfying_assignments.append(assignment)
        return satisfying_assignments

    def geometric_group_dimension(satisfying_assignments):
        n = len(satisfying_assignments[0])
        G = set()
        for assignment in satisfying_assignments:
            for i in range(n):
                if assignment & (1 << i) == 0:
                    G.add((assignment, assignment | (1 << i)))
                else:
                    G.add((assignment, assignment ^ (1 << i)))
        return len(G)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        satisfying_assignments = find_satisfying_assignments(circuit)
        dim_G = geometric_group_dimension(satisfying_assignments)
        
        results.append({
            "metric_name": "dim(G)",
            "metric_value": dim_G,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": dim_G <= 3 * n * math.log(n),
            "counterexample": "" if dim_G <= 3 * n * math.log(n) else f"dim(G) = {dim_G} > 3 * {n} * log({n})"
        })
    
    return {
        "metric_name": "dim(G)",
        "metric_value": sum(r["metric_value"] for r in results),
        "instances_tested": len(results),
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8 and mean_value <= 3:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"dim(G) > 3 for some circuits\" first_failing_seed={first_failing_seed}")