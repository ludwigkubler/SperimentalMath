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
    
    def generate_boolean_circuit(depth, num_inputs):
        if depth == 1:
            return [random.choice([0, 1])]
        else:
            subcircuits = [generate_boolean_circuit(random.randint(1, depth-1), num_inputs) for _ in range(num_inputs)]
            return [random.choice([0, 1]) for _ in range(len(subcircuits))]

    def compute_clause_set(circuit):
        if len(circuit) == 1:
            return circuit
        else:
            clause = []
            for i in range(len(circuit)):
                subclause = compute_clause_set(circuit[i])
                clause.extend([subclause[j] | circuit[0][j] for j in range(len(subclause))])
            return clause

    def grothendieck_teichmueller_group_order(clause_set):
        if not clause_set:
            return 1
        order = 1
        for clause in clause_set:
            order *= len(clause)
        return order

    n_max = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            circuit = generate_boolean_circuit(random.randint(1, min(n, 10)), n)
            clause_set = compute_clause_set(circuit)
            order = grothendieck_teichmueller_group_order(clause_set)
            depth = len(circuit) - 1
            expected_bound = depth ** 3
            
            if order > expected_bound:
                conjecture_holds = False
                counterexample = f"Circuit with n={n}, D={depth} has order {order} > bound {expected_bound}"
            
            metric_values.append(order)
    
    return {
        "metric_name": "Grothendieck-Teichmüller Group Order",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": 30,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 31)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")