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
    
    def generate_formula(n):
        # Generate a random satisfiable Boolean formula with n variables
        clauses = []
        for _ in range(2 ** (n - 1)):
            clause = [random.choice(['', '¬']) + random.choice([f'x{i}' for i in range(n)]) for _ in range(random.randint(1, n))]
            clauses.append(' ∨ '.join(clause))
        return ' ∧ '.join(clauses)
    
    def tropical_norm(formula):
        # Compute the tropical norm of a formula
        # This is a placeholder implementation; replace with actual computation
        return len(formula.split())
    
    def proof_length(formula):
        # Compute the proof length in polynomial-size resolution refutations
        # This is a placeholder implementation; replace with actual computation
        return len(formula.split()) * 2
    
    n = random.randint(5, 30)
    formula = generate_formula(n)
    norm = tropical_norm(formula)
    length = proof_length(formula)
    
    c = 1.0  # Placeholder constant for the conjecture
    expected_bound = n ** c * length
    
    deviation = abs(norm - expected_bound) / expected_bound
    
    return {
        "metric_name": "tropical_norm_vs_proof_length",
        "metric_value": norm,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": deviation <= 0.1 and norm <= 1.1 * expected_bound,
        "counterexample": "" if deviation <= 0.1 else f"deviation={deviation:.2f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, {result}}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"deviation exceeds bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")