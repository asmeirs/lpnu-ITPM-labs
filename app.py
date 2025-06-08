import streamlit as st
import numpy as np
from sympy.printing.pretty import pretty
import matplotlib.pyplot as plt
from core import (
    parse_function,
    get_domain_and_range,
    get_safe_numeric_domain,
    evaluate_function,
    evaluate_derivative,
    compute_tangent_line,
    compute_definite_integral,
)

st.set_page_config(layout="wide")
st.title("Interactive Calculus Visualizer")

# --- Inputs ---
st.sidebar.header("Function Setup")
func_str = st.sidebar.text_input("Enter a function f(x):", value="sin(x)")

try:
    func_sym, f_lambdified, deriv_sym, deriv_lambdified = parse_function(func_str)
except ValueError:
    st.error("Invalid function expression. Please check your input.")
    st.stop()

try:
    domain, range_y = get_domain_and_range(func_sym)
    print(domain)
    print(range_y)
    st.markdown(f"**Function domain:** {pretty(domain)}")
    st.markdown(f"**Function range:** {pretty(range_y)}")
except Exception:
    st.warning("Could not compute domain/range.")

try:
    x_valid_min, x_valid_max = get_safe_numeric_domain(domain)
except ValueError:
    st.error("Function is undefined over default domain (-20, 20).")
    st.stop()

x_min, x_max = st.sidebar.slider("Domain (x-axis range):", x_valid_min, x_valid_max, (max(x_valid_min, -10.0), min(x_valid_max, 10.0)))

show_tangent = st.sidebar.checkbox("Show tangent line", value=True)
x0 = st.sidebar.slider("Point for tangent (x₀):", x_min, x_max, (x_max + x_min)/2)
show_derivative = st.sidebar.checkbox("Show derivative f′(x)", value=True)

st.sidebar.header("Integral Setup")
show_integral = st.sidebar.checkbox("Show definite integral", value=False)
a = st.sidebar.slider("a (start of interval):", x_min, x_max, x_min)
b = st.sidebar.slider("b (end of interval):", x_min, x_max, x_max)


# --- Plot initialization ---
x_vals = np.linspace(x_min, x_max, 400)
y_vals = evaluate_function(f_lambdified, x_vals)

plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, label="f(x)", color='blue')


# --- Tangent Line ---
if show_tangent:
    try:
        tangent_line, f_x0, slope = compute_tangent_line(f_lambdified, deriv_lambdified, x_vals, x0)
        plt.plot(x_vals, tangent_line, label=f"Tangent at x₀={x0:.2f}", linestyle="--", color='green')
        plt.scatter([x0], [f_x0], color='green')
        st.markdown(f"**Tangent line at x₀ = {x0:.2f}:** f′(x₀) = {slope:.4f}, f(x₀) = {f_x0:.4f}")
    except ValueError as e:
        st.warning(f"Could not compute tangent line: {e}")
    except Exception:
        st.warning("An unexpected error occurred while computing the tangent line.")


# --- Derivative ---
if show_derivative:
    try:
        dy_vals = evaluate_derivative(deriv_lambdified, x_vals)
        plt.plot(x_vals, dy_vals, label="f′(x)", color='orange')
    except Exception:
        st.warning("Could not compute derivative for plotting.")


# --- Integral ---
if show_integral and a < b:
    x_fill = np.linspace(a, b, 200)
    y_fill = evaluate_function(f_lambdified, x_fill)
    plt.fill_between(x_fill, y_fill, alpha=0.3, label=f"∫ f(x) dx from {a} to {b}", color='purple')
    try:
        definite_integral = compute_definite_integral(func_sym, a, b)
        st.markdown(f"**Definite integral from {a} to {b}:** {definite_integral:.4f}")
    except ValueError as e:
        st.warning(f"Could not compute integral: {e}")
    except Exception:
        st.warning("An error occurred while computing the integral.")


# --- Plot output ---
plt.axhline(0, color='gray', lw=0.5)
plt.axvline(0, color='gray', lw=0.5)
plt.legend()
plt.grid(True)

x_plot_min, x_plot_max = plt.xlim()
y_plot_min, y_plot_max = plt.ylim()

x_plot_min = max(x_plot_min, -30)
x_plot_max = min(x_plot_max, 30)
y_plot_min = max(y_plot_min, -30)
y_plot_max = min(y_plot_max, 30)

plt.xlim(x_plot_min, x_plot_max)
plt.ylim(y_plot_min, y_plot_max)
st.pyplot(plt.gcf())
