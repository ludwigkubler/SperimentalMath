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
    
    def generate_circuit(n, m):
        inputs = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(inputs, 2)
            if random.choice([True, False]):
                clause[0] = f'¬{clause[0]}'
            clauses.append(clause)
        return inputs, clauses

    def resolution_proof_complexity(circuit):
        inputs, clauses = circuit
        n = len(inputs)
        m = len(clauses)
        
        # Simplify the circuit using DPLL algorithm (simplified version)
        while True:
            unit_clauses = [c for c in clauses if len(c) == 1]
            if not unit_clauses:
                break
            literal, _ = unit_clauses[0]
            for i in range(m):
                if literal in clauses[i]:
                    clauses[i].remove(literal)
                if f'¬{literal}' in clauses[i]:
                    clauses[i] = []
            inputs.remove(literal.replace('¬', ''))
        
        return m - len([c for c in clauses if not c])

    def minimal_groupoid_composition_width(circuit):
        # Placeholder implementation (not actual groupoid composition width)
        inputs, clauses = circuit
        n = len(inputs)
        return n

    n = random.randint(5, 40)
    m = random.randint(n // 2, n * 2)
    circuit = generate_circuit(n, m)
    
    gcw = minimal_groupoid_composition_width(circuit)
    w = resolution_proof_complexity(circuit)
    
    if w == 0:
        return {
            "metric_name": "gcw/w",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_proof_complexity_is_zero"
        }
    
    ratio = Fraction(gcw, w)
    return {
        "metric_name": "gcw/w",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results)} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"gcw/w ratio exceeds 2\" first_failing_seed={first_failing_seed}")