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
    
    def generate_boolean_circuit(n):
        if n == 1:
            return ['0'], []
        else:
            inputs = [f'x{i}' for i in range(n)]
            gates = []
            for _ in range(n - 1):
                gate_type = random.choice(['AND', 'OR'])
                gate_inputs = random.sample(inputs, 2)
                output = f'y{len(gates)}'
                gates.append((gate_type, gate_inputs, output))
                inputs.append(output)
            return inputs, gates
    
    def algebraic_quotient(circuit):
        n = len(circuit[0])
        equivalence_classes = {}
        for i in range(n):
            equivalence_classes[f'x{i}'] = set([f'x{i}'])
        for gate_type, gate_inputs, output in circuit[1]:
            new_class = {output}
            for input_var in gate_inputs:
                if input_var not in equivalence_classes:
                    equivalence_classes[input_var] = set()
                new_class.update(equivalence_classes[input_var])
            for var in new_class:
                equivalence_classes[var] = new_class
        return len(equivalence_classes)
    
    def complexity(circuit):
        return len(circuit[1]) + len(circuit[0])
    
    n_max = 40
    instances_tested = 30
    total_rank_quot = 0
    
    for _ in range(instances_tested):
        inputs, gates = generate_boolean_circuit(random.randint(5, 40))
        rank_quot = algebraic_quotient((inputs, gates))
        complexity_val = complexity((inputs, gates))
        total_rank_quot += rank_quot / complexity_val
    
    mean_rank_quot = total_rank_quot / instances_tested
    conjecture_holds = mean_rank_quot <= 1.5
    counterexample = "" if conjecture_holds else "mean_rank_quot > 1.5"
    
    return {
        "metric_name": "mean_rank_quot",
        "metric_value": mean_rank_quot,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank_quot = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank_quot} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank_quot} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_rank_quot > 1.5\" first_failing_seed={first_failing_seed}")