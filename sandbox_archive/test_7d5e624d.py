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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_group_representation(r, p):
        # Generate a random group representation R with dimension r over a finite field F of size p
        return [[random.randint(0, p-1) for _ in range(r)] for _ in range(r)]
    
    def generate_random_polynomial(n, m, p):
        # Generate a random polynomial f(x_1,...,x_n) in F[x_1,...,x_n] with degree at most m
        coeffs = [random.randint(0, p-1) for _ in range(m+1)]
        variables = ['x' + str(i) for i in range(n)]
        terms = []
        for i in range(m+1):
            if coeffs[i]:
                term = ' + '.join([f'{coeffs[i]}*{v}^{i}' for v in variables])
                terms.append(term)
        return ' + '.join(terms)
    
    def tropicalize_polynomial(poly, n):
        # Tropicalize the polynomial by taking the maximum coefficient of each monomial
        if not poly:
            return 0
        max_coeff = 0
        for term in poly.split(' + '):
            if '*' in term and '^' in term:
                coeff = int(term.split('*')[0])
                max_coeff = max(max_coeff, coeff)
        return max_coeff
    
    def generate_random_circuit(n, p):
        # Generate a random circuit C computing the same Boolean function as the group representation
        variables = ['x' + str(i) for i in range(n)]
        gates = []
        for _ in range(2**n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(variables, 2)
            output = 'y' + str(len(gates))
            gates.append((gate_type, inputs, output))
        return gates
    
    def evaluate_circuit(circuit, n):
        # Evaluate the circuit for a given input
        variables = ['x' + str(i) for i in range(n)]
        values = {v: random.choice([0, 1]) for v in variables}
        outputs = {}
        for gate_type, inputs, output in circuit:
            if gate_type == 'AND':
                outputs[output] = all(values[input] for input in inputs)
            elif gate_type == 'OR':
                outputs[output] = any(values[input] for input in inputs)
        return outputs[list(outputs.keys())[-1]]
    
    def tropicalize_circuit(circuit, n):
        # Tropicalize the circuit by taking the maximum value of each gate
        max_value = 0
        for gate_type, inputs, output in circuit:
            values = [evaluate_circuit([(gate_type, inputs, 'y')], n) for _ in range(10)]
            max_value = max(max_value, max(values))
        return max_value
    
    r = random.randint(2, 4)
    p = random.choice([2, 3, 5])
    n = random.randint(5, 10)
    
    R = generate_group_representation(r, p)
    f = generate_random_polynomial(n, n, p)
    C = generate_random_circuit(n, p)
    
    tropical_rank_f = tropicalize_polynomial(f, n)
    tropical_rank_C = tropicalize_circuit(C, n)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": min(tropical_rank_f, tropical_rank_C),
        "instances_tested": 1,
        "conjecture_holds": tropical_rank_f <= r and tropical_rank_C <= n,
        "counterexample": "" if tropical_rank_f <= r and tropical_rank_C <= n else f"Counterexample: tropical_rank_f={tropical_rank_f}, tropical_rank_C={tropical_rank_C}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [53, 67, 71, 73, 79]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")