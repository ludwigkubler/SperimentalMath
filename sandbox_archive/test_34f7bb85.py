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
        if n == 1:
            return ['x0']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - len(left))
            return [f'({left[0]} OR {right[0]})'] + left + right
    
    def evaluate_circuit(circuit, valuation):
        if isinstance(circuit, str) and circuit.startswith('x'):
            return valuation[circuit]
        elif circuit == 'TRUE':
            return 1
        elif circuit == 'FALSE':
            return 0
        else:
            op = circuit[1:-1].split()
            left = evaluate_circuit(op[0], valuation)
            right = evaluate_circuit(op[2], valuation)
            if op[1] == 'AND':
                return min(left, right)
            elif op[1] == 'OR':
                return max(left, right)
    
    def non_archimedean_valuation(circuit):
        n = len(circuit.split())
        valuation = {f'x{i}': random.uniform(0.5, 1) for i in range(n)}
        valuation[f'x{i}'] = -valuation[f'x{i}']
        return valuation
    
    def minimal_rank(valuation):
        rank = 0
        for v in valuation.values():
            if v != 0:
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        circuit = generate_circuit(n)
        valuation = non_archimedean_valuation(circuit)
        rank = minimal_rank(valuation)
        total_rank += rank
        instances_tested += 1
    
    avg_rank = total_rank / instances_tested
    expected_rank = math.log(len(circuit.split())) / math.log(2)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": avg_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": abs(avg_rank - expected_rank) <= 1,
        "counterexample": "" if abs(avg_rank - expected_rank) <= 1 else f"avg_rank={avg_rank}, expected_rank={expected_rank}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - avg_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"avg_rank deviates from expected\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")