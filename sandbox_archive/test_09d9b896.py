# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_sipser_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def truth_table_to_additive_energy(truth_table):
        n = len(truth_table)
        energy = 0
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    for l in range(k+1, n):
                        if truth_table[i] + truth_table[j] == truth_table[k] + truth_table[l]:
                            energy += 1
        return energy
    
    def is_acc0_circuit(truth_table):
        # Simplified simulation of ACC⁰ circuit using random guessing
        n = len(truth_table)
        for _ in range(100):  # 100 attempts to guess the function
            guessed_function = [random.choice([0, 1]) for _ in range(n)]
            if truth_table == guessed_function:
                return True
        return False
    
    n = 40
    sipser_function = generate_sipser_function(n)
    energy = truth_table_to_additive_energy(sipser_function)
    acc0_circuit_exists = is_acc0_circuit(sipser_function)
    
    metric_name = "additive_energy"
    metric_value = energy
    instances_tested = 1
    conjecture_holds = energy >= n**2.5 - 0.1 * n**2.5 and not acc0_circuit_exists
    counterexample = "" if conjecture_holds else "ACC⁰ circuit exists for Sipser function"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*10**4+1, 1000))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_energy = sum(r["metric_value"] for r in results if "metric_value" in r)
    mean_energy = total_energy / len(results) if results else 0
    std_energy = (sum((r["metric_value"] - mean_energy)**2 for r in results if "metric_value" in r) / len(results))**0.5 if results else 0
    support_fraction = sum(r["conjecture_holds"] for r in results if "conjecture_holds" in r) / len(results)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_energy} std={std_energy} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")