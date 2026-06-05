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
    n = 10  # Start with a small size and increase if needed
    instances_tested = 0
    total_gL = 0.0
    max_n = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(30):
        n += 5  # Increase the size
        max_n = max(max_n, n)
        
        # Generate a random boolean circuit with satisfiability threshold θ(C)
        num_gates = random.randint(2, min(n, 10))
        gates = [random.choice(['AND', 'OR']) for _ in range(num_gates)]
        inputs = [random.choice([True, False]) for _ in range(n - num_gates)]
        
        # Construct the corresponding formal grammar L
        grammar = {}
        variables = set()
        for i, gate in enumerate(gates):
            var = f'V{i}'
            variables.add(var)
            if gate == 'AND':
                grammar[var] = (f'({variables.pop()} {variables.pop()})', 2)
            else:
                grammar[var] = (f'({variables.pop()} {variables.pop()})', 2)
        grammar['S'] = ('(' + ' '.join(variables) + ')', len(variables))
        
        # Calculate the minimal order of grammar complexity g(L)
        gL = max(len(var) for var in grammar if var != 'S')
        total_gL += gL
        instances_tested += 1
        
        # Check if the conjecture holds
        θ_C = num_gates / n
        if gL > 3 * θ_C:
            conjecture_holds = False
            counterexample = f"n={n}, g(L)={gL}, θ(C)={θ_C}"
    
    mean_gL = total_gL / instances_tested
    correlation_coefficient = 0.8  # Placeholder value, to be calculated
    
    return {
        "metric_name": "grammar_complexity",
        "metric_value": mean_gL,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_gL = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_gL} std=<not_calculated> support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")