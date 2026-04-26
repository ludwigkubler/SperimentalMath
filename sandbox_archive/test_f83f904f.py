import random
import math
import sys
import json

def GF2_poly_gcd(poly1, poly2):
    while poly2:
        poly1, poly2 = poly2, GF2_poly_mod(poly1, poly2)
    return poly1

def GF2_poly_mod(dividend, divisor):
    if not divisor:
        raise ValueError("Divisor cannot be zero polynomial")
    degree_dividend = len(dividend) - 1
    degree_divisor = len(divisor) - 1
    quotient = [0] * (degree_dividend - degree_divisor + 1)
    for i in range(degree_dividend, degree_divisor - 1, -1):
        leading_coeff_quotient = dividend[i] // divisor[degree_divisor]
        quotient[i - degree_divisor] = leading_coeff_quotient
        remainder = [0] * (i + 1)
        for j in range(degree_divisor + 1):
            remainder[j] = dividend[j] ^ (leading_coeff_quotient * divisor[j])
        dividend = remainder
    return dividend

def GF2_poly_div(dividend, divisor):
    if not divisor:
        raise ValueError("Divisor cannot be zero polynomial")
    degree_dividend = len(dividend) - 1
    degree_divisor = len(divisor) - 1
    quotient = [0] * (degree_dividend - degree_divisor + 1)
    for i in range(degree_dividend, degree_divisor - 1, -1):
        leading_coeff_quotient = dividend[i] // divisor[degree_divisor]
        quotient[i - degree_divisor] = leading_coeff_quotient
        remainder = [0] * (i + 1)
        for j in range(degree_divisor + 1):
            remainder[j] = dividend[j] ^ (leading_coeff_quotient * divisor[j])
        dividend = remainder
    return quotient, dividend

def Buchberger_algorithm(generators):
    S = set()
    for i in range(len(generators)):
        for j in range(i + 1, len(generators)):
            s = GF2_poly_gcd(generators[i], generators[j])
            if s:
                S.add(s)
    return list(S)

def random_CNF(n):
    clauses = []
    for _ in range(2**n - 1):
        clause = [random.randint(0, n-1) + 1]
        while True:
            next_var = random.randint(0, n-1) + 1
            if next_var not in clause and len(clause) < n:
                clause.append(next_var)
            else:
                break
        clauses.append(clause)
    return clauses

def CNF_to_polynomials(CNF):
    variables = set()
    for clause in CNF:
        for var in clause:
            variables.add(var)
    polynomials = []
    for var in variables:
        poly = [0] * (var + 1)
        poly[var] = 1
        polynomials.append(poly)
    return polynomials

def Extended_Frege_proof_size(CNF):
    n = len(CNF[0])
    return 2**n - 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    CNF = random_CNF(n)
    polynomials = CNF_to_polynomials(CNF)
    generators = Buchberger_algorithm(polynomials)
    proof_size = Extended_Frege_proof_size(CNF)
    metric_value = len(generators)
    instances_tested = 1
    conjecture_holds = abs(metric_value - proof_size) <= 2 * math.sqrt(proof_size)
    counterexample = "" if conjecture_holds else f"n={n}, generators={len(generators)}, proof_size={proof_size}"
    return {
        "metric_name": "Generator Count",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")