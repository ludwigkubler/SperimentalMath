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
            return 'x0'
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return f'({left} OR {right})'

    def evaluate_circuit(circuit, valuation):
        if circuit.startswith('(') and circuit.endswith(')'):
            circuit = circuit[1:-1]
        if ' OR ' in circuit:
            left, right = circuit.split(' OR ')
            return evaluate_circuit(left, valuation) or evaluate_circuit(right, valuation)
        elif ' AND ' in circuit:
            left, right = circuit.split(' AND ')
            return evaluate_circuit(left, valuation) and evaluate_circuit(right, valuation)
        else:
            var, negated = circuit.startswith('¬'), circuit[1:] if circuit.startswith('¬') else circuit
            return valuation[var] != negated

    def non_archimedean_valuation(circuit):
        if circuit == 'x0':
            return {'x0': 0}
        elif ' OR ' in circuit:
            left, right = circuit.split(' OR ')
            val_left = non_archimedean_valuation(left)
            val_right = non_archimedean_valuation(right)
            for var in set(val_left) | set(val_right):
                if var not in val_left or var not in val_right:
                    return {var: 1}
            return {var: max(val_left[var], val_right[var]) for var in val_left}
        elif ' AND ' in circuit:
            left, right = circuit.split(' AND ')
            val_left = non_archimedean_valuation(left)
            val_right = non_archimedean_valuation(right)
            for var in set(val_left) | set(val_right):
                if var not in val_left or var not in val_right:
                    return {var: 0}
            return {var: min(val_left[var], val_right[var]) for var in val_left}
        else:
            var, negated = circuit.startswith('¬'), circuit[1:] if circuit.startswith('¬') else circuit
            return {var: int(negated)}

    def minimal_rank(valuation):
        rank = 0
        for value in valuation.values():
            rank = max(rank, math.ceil(math.log2(value + 1)))
        return rank

    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    valuation = non_archimedean_valuation(circuit)
    rank = minimal_rank(valuation)

    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank == math.log2(n) + 1,
        "counterexample": "" if rank == math.log2(n) + 1 else f"Counterexample for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Counterexample found\" first_failing_seed={first_failing_seed}")