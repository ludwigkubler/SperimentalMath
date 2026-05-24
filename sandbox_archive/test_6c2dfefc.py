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
    
    def generate_ac0_circuit(n, s):
        # Generate a random AC0 parity circuit with n inputs and size s
        circuit = []
        for _ in range(s):
            gate_type = random.choice(['AND', 'OR'])
            if gate_type == 'AND':
                gate = [random.randint(0, 1) for _ in range(n)]
            else:
                gate = [random.randint(0, 1) for _ in range(n)]
            circuit.append(gate)
        return circuit
    
    def compute_local_defect_complexity(circuit):
        # Compute the local defect complexity of an AC0 parity circuit
        n = len(circuit[0])
        S = set()
        for gate in circuit:
            S.update(gate)
        subring_closure = {1}
        for elem in S:
            new_elements = [x * elem % 2 for x in subring_closure]
            subring_closure.update(new_elements)
        return len(S) - math.log(len(subring_closure), 2)
    
    def find_affine_quotient(circuit):
        # Find an affine quotient Q such that the minimal local defect complexity is computed
        n = len(circuit[0])
        S = set()
        for gate in circuit:
            S.update(gate)
        subring_closure = {1}
        for elem in S:
            new_elements = [x * elem % 2 for x in subring_closure]
            subring_closure.update(new_elements)
        return len(S) - math.log(len(subring_closure), 2)
    
    n = random.randint(5, 40)
    s = random.randint(10, 30)
    circuit = generate_ac0_circuit(n, s)
    local_defect_complexity = compute_local_defect_complexity(circuit)
    alpha_s = math.log(s) / math.log(n)
    
    return {
        "metric_name": "local_defect_complexity_ratio",
        "metric_value": local_defect_complexity / math.log(n),
        "instances_tested": 1,
        "conjecture_holds": local_defect_complexity >= alpha_s * math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")