import sympy as sp
import numpy as np

x = sp.symbols('x')

def parse_function(func_str):
    try:
        func_sym = sp.sympify(func_str)
        f_lambdified = sp.lambdify(x, func_sym, modules=["numpy"])
        deriv_sym = sp.diff(func_sym, x)
        deriv_lambdified = sp.lambdify(x, deriv_sym, modules=["numpy"])
        return func_sym, f_lambdified, deriv_sym, deriv_lambdified
    except (sp.SympifyError, TypeError):
        raise ValueError("Invalid function expression")

def get_domain_and_range(func_sym):
    domain = sp.calculus.util.continuous_domain(func_sym, x, sp.S.Reals)
    range_y = sp.calculus.util.function_range(func_sym, x, domain)
    return domain, range_y


def get_safe_numeric_domain(domain, default_min=-20.0, default_max=20.0):
    safe_domain = domain.intersect(sp.Interval(default_min, default_max))
    if safe_domain.is_empty:
        raise ValueError("Empty domain in default range")
    return float(safe_domain.inf), float(safe_domain.sup)

def evaluate_function(f_lambdified, x_vals):
    result = f_lambdified(x_vals)
    if np.isscalar(result):
        result = np.full_like(x_vals, result)
    return result

def evaluate_derivative(deriv_lambdified, x_vals):
    result = deriv_lambdified(x_vals)
    if np.isscalar(result):
        return np.full_like(x_vals, result, dtype=np.float64)
    return np.array(result)

def compute_tangent_line(f_lambdified, deriv_lambdified, x_vals, x0):
    f_x0 = f_lambdified(x0)
    slope = deriv_lambdified(x0)

    if not np.isfinite(f_x0):
        raise ValueError(f"f(x₀) is not finite at x₀ = {x0}")
    if not np.isfinite(slope):
        raise ValueError(f"f′(x₀) is not finite at x₀ = {x0}")

    tangent_line = slope * (x_vals - x0) + f_x0
    return tangent_line, f_x0, slope

def compute_definite_integral(func_sym, a, b):
    singularities = sp.singularities(func_sym, x)
    interval = sp.Interval(a, b)

    for s in singularities:
        if s in interval:
            raise ValueError(f"Function has a discontinuity at x = {s} in the interval [{a}, {b}]")

    return sp.N(sp.integrate(func_sym, (x, a, b)))
