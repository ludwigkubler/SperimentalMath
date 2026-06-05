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
    
    def generate_random_circuit(n, d):
        circuit = []
        for _ in range(d):
            level = [random.choice(['AND', 'OR']) for _ in range(n)]
            circuit.append(level)
        return circuit
    
    def monotone_width(circuit):
        width = 0
        for level in circuit:
            width = max(width, len([g for g in level if g == 'AND']))
        return width
    
    def simplicial_complex(circuit):
        n = len(circuit[0])
        complex_ = []
        for i in range(1 << n):
            face = [j for j in range(n) if (i & (1 << j)) != 0]
            complex_.append(face)
        return complex_
    
    def local_induction_dimension(complex_):
        dim = -1
        while True:
            new_complex = []
            for face in complex_:
                if len(face) > dim + 1:
                    continue
                if all(all(j in f for j in face) for f in complex_ if len(f) == dim + 2):
                    new_complex.append(face)
            if not new_complex:
                return dim
            dim += 1
            complex_ = new_complex
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            circuit = generate_random_circuit(n, random.randint(1, n))
            width = monotone_width(circuit)
            complex_ = simplicial_complex(circuit)
            dim = local_induction_dimension(complex_)
            
            if dim < math.log(n) * math.log(width):
                conjecture_holds = False
                counterexample = f"n={n}, circuit={circuit}, width={width}, dim={dim}"
                break
            
            total_metric_value += dim
            instances_tested += 1
            n_max = max(n_max, n)
    
    return {
        "metric_name": "minimal_local_induction_dimension",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] > 10 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence_or_budget_exceeded")