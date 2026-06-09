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
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR', 'NOT'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def evaluate_circuit(circuit, assignment):
        stack = []
        for gate, inputs in reversed(circuit):
            if gate == 'AND':
                result = all(stack.pop() for _ in range(len(inputs)))
            elif gate == 'OR':
                result = any(stack.pop() for _ in range(len(inputs)))
            else:  # NOT
                result = not stack.pop()
            stack.append(result)
        return stack[0]
    
    def galois_action(circuit):
        actions = set()
        n = len(circuit[0][1])
        for perm in itertools.permutations(range(n)):
            new_circuit = []
            for gate, inputs in circuit:
                if gate == 'NOT':
                    new_inputs = [perm.index(i) for i in inputs]
                else:
                    new_inputs = [perm[i] for i in inputs]
                new_circuit.append((gate, new_inputs))
            actions.add(tuple(new_circuit))
        return actions
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        if time.time() - start_time > 200:
            return {
                "metric_name": "|Γ_C|",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "budget_exceeded"
            }
        
        for _ in range(30):
            circuit = generate_circuit(n)
            assignment = [random.randint(0, 1) for _ in range(n)]
            if evaluate_circuit(circuit, assignment):
                actions = galois_action(circuit)
                instances_tested += 1
                total_metric_value += len(actions)
                if len(actions) > n**2 * math.log(n):
                    conjecture_holds = False
                    counterexample = f"n={n}, |Γ_C|={len(actions)} exceeds O(n^2 log n)"
    
    return {
        "metric_name": "|Γ_C|",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    import time
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    start_time = time.time()
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction:.2f}")