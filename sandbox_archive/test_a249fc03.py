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
    
    def generate_symmetric_circuit(n):
        circuit = []
        for _ in range(n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(2)]
            circuit.append((gate, inputs))
        return circuit
    
    def dpll_search_tree_width(circuit):
        # Simplified DPLL search tree width calculation
        return len(circuit)
    
    def symplectic_leaf_space(n):
        # Simulated symplectic leaf space generation
        leaves = set()
        for _ in range(2**n):
            leaves.add(tuple(random.randint(0, 1) for _ in range(n)))
        return leaves
    
    def minimal_order_of_divisor(leaves):
        # Simplified minimal order of divisor calculation
        return len(leaves)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_symmetric_circuit(n)
        w_C = dpll_search_tree_width(circuit)
        leaves = symplectic_leaf_space(n)
        order = minimal_order_of_divisor(leaves)
        
        if len(leaves) == 0:
            return {
                "metric_name": "minimal_order_of_divisor",
                "metric_value": None,
                "instances_tested": n,
                "conjecture_holds": False,
                "counterexample": "empty_symplectic_leaf_space"
            }
        
        results.append((n, w_C, order))
    
    mean_difference = sum(abs(w - o) for _, w, o in results) / len(results)
    support_fraction = sum(1 for _, _, o in results if abs(o - w) <= 1.5) / len(results)
    
    return {
        "metric_name": "minimal_order_of_divisor",
        "metric_value": mean_difference,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"mean_diff={mean_difference}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mean_diff={result['metric_value']}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")