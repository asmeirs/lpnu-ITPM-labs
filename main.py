import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# --- Symbolic setup ---
x = sp.symbols('x')

st.title("Interactive Calculus Visualizer")

# --- User Inputs ---
st.sidebar.header("Function Setup")
func_str = st.sidebar.text_input("Enter a function f(x):", value="sin(x)")

try:
    func_sym = sp.sympify(func_str)
    f_lambdified = sp.lambdify(x, func_sym, modules=["numpy"])
    deriv_sym = sp.diff(func_sym, x)
    deriv_lambdified = sp.lambdify(x, deriv_sym, modules=["numpy"])
except (sp.SympifyError, TypeError):
    st.error("Invalid function expression. Please check your input.")
    st.stop()


# --- Function Domain and Range ---
domain = sp.calculus.util.continuous_domain(func_sym, x, sp.S.Reals)
range_y = sp.calculus.util.function_range(func_sym, x, domain)

st.markdown(f"**Function domain:** {domain}")
st.markdown(f"**Function range:** {range_y}")


# --- Adjust sliders according with function domain ---
default_min, default_max = -20.0, 20.0
safe_domain = domain.intersect(sp.Interval(default_min, default_max))

if safe_domain.is_empty:
    st.error("Function is undefined over default domain (-20, 20). Please try a different function.")
    st.stop()

try:
    x_valid_min = float(safe_domain.inf)
    x_valid_max = float(safe_domain.sup)
except (TypeError, ValueError):
    st.error("Could not determine valid numeric domain bounds.")
    st.stop()

x_min, x_max = st.sidebar.slider("Domain (x-axis range):", x_valid_min, x_valid_max, (max(x_valid_min, -5.0), min(x_valid_max, 5.0)))

show_tangent = st.sidebar.checkbox("Show tangent line", value=True)
x0 = st.sidebar.slider("Point for tangent (x₀):", x_min, x_max, (max(x_valid_min, 1.0)))
show_derivative = st.sidebar.checkbox("Show derivative f′(x)", value=True)

st.sidebar.header("Integral Setup")
show_integral = st.sidebar.checkbox("Show definite integral", value=False)
a = st.sidebar.slider("a (start of interval):", x_min, x_max, x_min)
b = st.sidebar.slider("b (end of interval):", x_min, x_max, x_max)

# --- Plotting ---
x_vals = np.linspace(x_min, x_max, 400)
y_vals = f_lambdified(x_vals)

plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, label="f(x)", color='blue')

# --- Tangent line ---
if show_tangent:
    f_x0 = f_lambdified(x0)
    slope = deriv_lambdified(x0)
    tangent_line = slope * (x_vals - x0) + f_x0
    plt.plot(x_vals, tangent_line, label=f"Tangent at x₀={x0:.2f}", linestyle="--", color='green')
    plt.scatter([x0], [f_x0], color='green')
    st.markdown(f"**Tangent line at x₀ = {x0:.2f}:** f′(x₀) = {slope:.4f}, f(x₀) = {f_x0:.4f}")

# --- Derivative plot ---
if show_derivative:
    try:
        dy_vals = deriv_lambdified(x_vals)
        plt.plot(x_vals, dy_vals, label="f′(x)", color='orange')
    except Exception:
        st.warning("Could not compute derivative for plotting.")

# --- Integral area ---
if show_integral and a < b:
    x_fill = np.linspace(a, b, 200)
    y_fill = f_lambdified(x_fill)
    plt.fill_between(x_fill, y_fill, alpha=0.3, label=f"∫ f(x) dx from {a} to {b}", color='purple')
    try:
        definite_integral = sp.integrate(func_sym, (x, a, b))
        st.markdown(f"**Definite integral from {a} to {b}:** {sp.N(definite_integral):.4f}")
    except Exception:
        st.warning("Could not compute integral.")

plt.axhline(0, color='gray', lw=0.5)
plt.axvline(0, color='gray', lw=0.5)
plt.legend()
plt.grid(True)
st.pyplot(plt.gcf())
