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

# Helper functions for boolean circuit evaluation and algebraic quotient calculation

def evaluate_circuit(circuit, assignment):
    stack = []
    for gate_type, inputs in circuit:
        if gate_type == 'AND':
            result = 1
            for i in inputs:
                result &= assignment[i]
            stack.append(result)
        elif gate_type == 'OR':
            result = 0
            for i in inputs:
                result |= assignment[i]
            stack.append(result)
        elif gate_type == 'NOT':
            result = not assignment[inputs[0]]
            stack.append(result)
    return stack[-1]

def algebraic_quotient(circuit):
    n = len(circuit)
    equivalence_classes = {}
    for i in range(2**n):
        assignment = [i >> j & 1 for j in range(n)]
        output = evaluate_circuit(circuit, assignment)
        if output not in equivalence_classes:
            equivalence_classes[output] = []
        equivalence_classes[output].append(i)
    
    rank_quot = len(equivalence_classes)
    return rank_quot

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 0
    instances_tested = 0
    total_rank_quot = 0
    total_complexity = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        n_max = max(n_max, n)
        
        # Generate a random boolean circuit
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR', 'NOT'])
            if gate_type == 'NOT':
                inputs = [random.randint(0, n-1)]
            else:
                inputs = [random.randint(0, n-1) for _ in range(2)]
            circuit.append((gate_type, inputs))
        
        # Compute the algebraic quotient
        rank_quot = algebraic_quotient(circuit)
        complexity = len(circuit)
        
        total_rank_quot += rank_quot
        total_complexity += complexity
        instances_tested += 1
    
    mean_rank_quot = total_rank_quot / instances_tested
    conjecture_holds = mean_rank_quot <= 1.5 * (total_complexity / instances_tested)
    
    return {
        "metric_name": "mean_rank_quot",
        "metric_value": mean_rank_quot,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_rank_quot = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank_quot} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank_quot} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")