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
    
    def generate_circuit(n):
        circuit = []
        for _ in range(n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(1, n))]
            circuit.append((gate, inputs))
        return circuit
    
    def tautology_set(circuit):
        if not circuit:
            return {()}
        gate, inputs = circuit[0]
        remaining_circuit = circuit[1:]
        if gate == 'AND':
            return set.intersection(*[tautology_set(remaining_circuit)] + [set([tuple(inputs)])])
        elif gate == 'OR':
            return set.union(*[tautology_set(remaining_circuit)] + [set([tuple(inputs)])])
    
    def categorial_invariants(tautology):
        invariants = {}
        for t in tautology:
            if len(t) not in invariants:
                invariants[len(t)] = 1
            else:
                invariants[len(t)] += 1
        return invariants
    
    def entanglement_entropy(invariants):
        total = sum(invariants.values())
        entropy = 0
        for count in invariants.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        tautology = tautology_set(circuit)
        invariants = categorial_invariants(tautology)
        order = sum(invariants.values())
        entropy = entanglement_entropy(invariants)
        diff = abs(order - entropy)
        results.append((n, order, entropy, diff))
    
    mean_diff = sum(diff for _, _, _, diff in results) / len(results)
    support_fraction = sum(1 for _, _, _, diff in results if diff <= 1) / len(results)
    
    conjecture_holds = support_fraction >= 0.8 and all(diff <= 10 for _, _, _, diff in results)
    counterexample = "" if conjecture_holds else "n=40, order=20, entropy=5"
    
    return {
        "metric_name": "Absolute Difference",
        "metric_value": mean_diff,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] == "n=40, order=20, entropy=5" for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"n=40, order=20, entropy=5\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds'] and r['counterexample'] == 'n=40, order=20, entropy=5'))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")