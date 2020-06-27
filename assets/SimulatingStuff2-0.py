import numpy as np
import matplotlib.pyplot as plt

def verlet(v, x, a, force, m, dt=.001):
    v = v + .5*a*dt
    x = x + v * dt
    a = force(v, x, a, m)/m
    v = v + .5*a*dt
    return v, x, a

def const_force(v, x, a, m, g=-1):
    return g*m

def main():
    x = 10
    v = 0
    m = 1
    g = -1
    a = g*m
    T = 5000

    vs = np.empty((T))
    xs = np.empty((T))
    for i in range(T):
        v, x, a = verlet(v, x, a, const_force, m)
        vs[i] = v
        xs[i] = x

    plt.plot(vs, 'x', label='$v$')
    plt.plot(xs, 'x', label='$x$')
    plt.xlabel('$t [\Delta t]$')
    plt.ylabel('$v, x$')
    
    # Analytical solution
    tsa = np.linspace(0, 5, 5000)
    xsa = .5*tsa**2*g + 10.
    vsa = tsa*g
    plt.plot(xsa, label='Analytical $x$')
    plt.plot(vsa, label='Analytical $v$')

    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
