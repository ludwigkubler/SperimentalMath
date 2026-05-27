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
    
    def generate_tseitin_circuit(n, w):
        # Generate a Tseitin circuit with n variables and width w
        variables = list(range(1, n + 1))
        literals = [f'x{i}' for i in range(1, n + 1)]
        clauses = []
        
        def add_clause(clause):
            clauses.append(clause)
        
        # Add input literals
        for var in variables:
            add_clause([f'x{var}', f'-x{var}'])
        
        # Add OR gates
        for i in range(n, n + w - 1):
            literal = f'x{i}'
            add_clause([literal, f'-x{i}'] + literals[:i-1])
        
        # Add AND gates
        for i in range(n + w - 1, n + 2 * w - 2):
            literal = f'x{i}'
            add_clause([literal, f'-x{i}'] + literals[i-n+w-2:i-n+1])
        
        return literals, clauses
    
    def compute_symmetry_group(literals, clauses):
        # Compute the symmetry group of the circuit
        n = len(literals) // 2
        symmetries = []
        
        for perm in itertools.permutations(range(n)):
            if all(clause.substitute({f'x{i}': f'x{perm[i]}'}) == clause for clause in clauses):
                symmetries.append(perm)
        
        return symmetries
    
    n = random.randint(5, 30)
    w = random.randint(1, min(n, 40))
    literals, clauses = generate_tseitin_circuit(n, w)
    
    symmetries = compute_symmetry_group(literals, clauses)
    S_f = len(symmetries)
    
    c = 2  # Example constant
    cw = c * w
    
    return {
        "metric_name": "S(f) / cw",
        "metric_value": Fraction(S_f, cw),
        "instances_tested": 1,
        "conjecture_holds": S_f <= cw,
        "counterexample": "" if S_f <= cw else f"S(f) = {S_f} > {cw}"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction < 0.3:
        counterexample = next(result for result in results if not result["conjecture_holds"])["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, result in enumerate(results) if not result['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support fraction")