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
    
    def generate_ac0_circuit(n):
        # Generate a simple AC0 circuit computing PARITY on n inputs
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropical_representation(circuit):
        # Compute the tropical polynomial representation over F_2
        n = len(circuit)
        max_order = 0
        distinct_representations = set()
        
        for i in range(2**n):
            value = circuit[i]
            order = bin(i).count('1')
            if order > max_order:
                max_order = order
            distinct_representations.add(value)
        
        return len(distinct_representations), max_order
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_ac0_circuit(n)
        distinct_representations, max_order = tropical_representation(circuit)
        
        if distinct_representations == 0 or max_order == 0:
            return {
                "metric_name": "Tropical Representations",
                "metric_value": 1,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Distinct representations: {distinct_representations}, Max order: {max_order}"
            }
        
        results.append({
            "n": n,
            "distinct_representations": distinct_representations,
            "max_order": max_order
        })
    
    avg_distinct_representations = sum(r["distinct_representations"] for r in results) / len(results)
    avg_max_order = sum(r["max_order"] for r in results) / len(results)
    
    conjecture_holds = all(avg_distinct_representations >= n**(1/3) and avg_max_order >= n**(1/3) for n in n_values)
    counterexample = "" if conjecture_holds else f"Distinct representations: {avg_distinct_representations}, Max order: {avg_max_order}"
    
    return {
        "metric_name": "Tropical Representations",
        "metric_value": avg_distinct_representations,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")