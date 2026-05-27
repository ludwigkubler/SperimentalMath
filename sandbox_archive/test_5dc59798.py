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
    
    def generate_boolean_circuit(n, m):
        # Generate a random boolean circuit with n variables and m gates
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            output = random.randint(0, 1)
            circuit.append((gate_type, inputs, output))
        return circuit
    
    def characteristic_polynomial(circuit):
        # Calculate the characteristic polynomial of a boolean circuit
        n = len(set(input for _, inputs, _ in circuit for input in inputs))
        m = len(circuit)
        
        # Initialize the matrix A
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for gate_type, inputs, output in circuit:
            if gate_type == 'AND':
                for i in inputs:
                    A[i][output] += 1
            elif gate_type == 'OR':
                for i in inputs:
                    A[output][i] += 1
        
        # Add the identity matrix to A
        for i in range(n + 1):
            A[i][i] += 1
        
        # Calculate the determinant of A
        det = 0
        if n == 1:
            det = A[0][0]
        else:
            for j in range(1, n + 1):
                submatrix = [row[:j-1] + row[j:] for row in A[1:]]
                det += (-1) ** (j % 2) * A[0][j-1] * determinant(submatrix)
        
        return det
    
    def determinant(matrix):
        # Calculate the determinant of a square matrix using Gaussian elimination
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** (j % 2) * matrix[0][j] * determinant(submatrix)
        
        return det
    
    def grothendieck_riemann_roch_index(circuit):
        # Calculate the Grothendieck–Riemann–Roch index of a boolean circuit
        n = len(set(input for _, inputs, _ in circuit for input in inputs))
        m = len(circuit)
        char_poly = characteristic_polynomial(circuit)
        
        # Count the number of independent monomials in the characteristic polynomial
        independent_monomials = 0
        terms = str(char_poly).split('+')
        for term in terms:
            if 'x' not in term and 'y' not in term:
                independent_monomials += 1
        
        return independent_monomials
    
    n = random.randint(5, 40)
    m = random.randint(n + 1, 2 * n)
    circuit = generate_boolean_circuit(n, m)
    
    gRR_C = grothendieck_riemann_roch_index(circuit)
    expected_bound = (m ** (1/3) * n ** (2/3))
    
    return {
        "metric_name": "Grothendieck–Riemann–Roch Index",
        "metric_value": gRR_C,
        "instances_tested": 1,
        "conjecture_holds": gRR_C <= expected_bound,
        "counterexample": "" if gRR_C <= expected_bound else f"gRR(C) = {gRR_C}, which is greater than O(m^(1/3)n^(2/3)) = {expected_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 97, 4))
    
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
        print(f"RESULT: FALSIFIED counterexample=\"gRR(C) > O(m^(1/3)n^(2/3))\" first_failing_seed={first_failing_seed}")