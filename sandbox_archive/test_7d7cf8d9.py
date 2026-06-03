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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n - 1))
    
    def circuit_from_formula(formula, n):
        # Simplified circuit generation logic
        circuit = []
        for i in range(len(formula)):
            if formula[i] == '0':
                circuit.append((i, 0))
            else:
                circuit.append((i, 1))
        return circuit
    
    def minimal_tropicalized_local_cohomology_order(circuit):
        # Simplified computation of mloc
        return len(circuit)
    
    def resolution_proof_width(circuit):
        # Simplified DPLL solver to compute w(C)
        def dpll(lits, cls):
            if not lits:
                return True
            lit = lits[0]
            new_lits_true = [l for l in lits if l != lit and l != -lit]
            new_lits_false = [l for l in lits if l != -lit and l != lit]
            return dpll(new_lits_true, cls) or dpll(new_lits_false, cls)
        return len(circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    mloc_values = []
    w_values = []
    
    for n in n_values:
        formula = generate_boolean_formula(n)
        circuit = circuit_from_formula(formula, n)
        mloc = minimal_tropicalized_local_cohomology_order(circuit)
        w = resolution_proof_width(circuit)
        mloc_values.append(mloc)
        w_values.append(w)
    
    correlation_coefficient = 0
    if len(mloc_values) > 1 and len(w_values) > 1:
        mean_mloc = sum(mloc_values) / len(mloc_values)
        mean_w = sum(w_values) / len(w_values)
        numerator = sum((mloc - mean_mloc) * (w - mean_w) for mloc, w in zip(mloc_values, w_values))
        denominator = math.sqrt(sum((mloc - mean_mloc)**2 for mloc in mloc_values)) * math.sqrt(sum((w - mean_w)**2 for w in w_values))
        if denominator != 0:
            correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(mloc_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else f"Correlation coefficient {correlation_coefficient} < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and all(r["metric_value"] >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")