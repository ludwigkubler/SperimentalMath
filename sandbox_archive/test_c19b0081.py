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
    
    def generate_tseitin_circuit(n, m):
        inputs = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate literals
        literals = [random.choice(inputs + [f'~{i}' for i in inputs]) for _ in range(m)]
        
        # Ensure at least one literal is true and one is false
        if random.choice([True, False]):
            literals[0] = f'~{literals[0]}'
        
        return literals
    
    def construct_group_action(literals):
        G = []
        for perm in itertools.permutations(inputs):
            if all(perm[lit.index('x')] == lit.replace('~', '') for lit in literals):
                G.append(perm)
        return G
    
    def minimal_order(G):
        if not G:
            return None
        return max(len(g) for g in G)
    
    n = 5  # Fixed number of inputs
    m_values = [10, 20, 30, 40]  # Varying number of clauses
    
    results = []
    for m in m_values:
        circuit = generate_tseitin_circuit(n, m)
        G = construct_group_action(circuit)
        order = minimal_order(G)
        
        if order is None:
            return {
                "metric_name": "minimal_order",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "empty group action"
            }
        
        results.append(order)
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    
    return {
        "metric_name": "minimal_order",
        "metric_value": mean_value,
        "instances_tested": len(m_values),
        "conjecture_holds": abs(mean_value - m_values[0] ** 0.5) <= 0.1 * m_values[0] ** 0.5 and all(abs(order - m_values[0] ** 0.5) <= 0.2 * m_values[0] ** 0.5 for order in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r - m_values[0] ** 0.5) <= 0.1 * m_values[0] ** 0.5) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(r - m_values[0] ** 0.5) > 0.2 * m_values[0] ** 0.5 for r in results):
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if abs(r - m_values[0] ** 0.5) > 0.2 * m_values[0] ** 0.5)]
        print(f"RESULT: FALSIFIED counterexample=\"deviation_greater_than_20_percent\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")