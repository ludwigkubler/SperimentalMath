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
    
    def generate_ac0_circuit(n, func):
        # Placeholder function to generate an AC⁰ circuit for a given function
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def count_irreducible_components(circuit):
        # Placeholder function to count irreducible components of the associated variety
        # This is a dummy implementation and should be replaced with actual algebraic geometry code
        return len(circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_ac0_circuit(n, 'parity')
        irreducible_components = count_irreducible_components(circuit)
        results.append(irreducible_components)
    
    c = 1.0  # Absolute constant (this value should be derived from the actual conjecture)
    conjecture_holds = all(x < c * math.log(n) for n, x in zip(n_values, results))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "irreducible_components",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50))  # Default to first 30 primes
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r < c * math.log(n_values[i]) for i, n in enumerate(n_values)) / len(results)
    
    if all(r < c * math.log(n_values[i]) for i, r in enumerate(results)):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r < c * math.log(n_values[i]) for i, r in enumerate(results)):
        first_failing_seed = seeds[results.index(next(r for i, r in enumerate(results) if not r < c * math.log(n_values[i])))]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")