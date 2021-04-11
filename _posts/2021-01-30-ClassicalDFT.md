---
layout: cite_post
title: "Building a Classical Density Functional Theory Code"
date: 2021-01-26
usemathjax: true
---

## Idea and Background
Classical Density Functional Theory (cDFT) is a relatively unknown methodology of determining the equilibrium density of fluids.
It's "parent theory" is the much more known [Density Functional Theory](https://en.wikipedia.org/wiki/Density_functional_theory), which is known as "DFT".
This well-known "DFT" method is used to calculate the electron density of a quantum mechanical system, i.e. solve the Schrödinger equation.
Interestingly this quantum mechanical DFT was developed before the classical version was conceived, making it one of the rare cases (as far as I know, the only), where a quantum method came first.

### Quantum Mechanical DFT
The trick employed in DFT is really elegant.
Basically, if you take a look at the Schrödinger equation (in the stationary form, location basis, roughly sketched) for a many body problem:

$$
\underbrace{\left(- \sum_i \left(\frac{1}{2} \frac{\mathrm{d}^2}{\mathrm{d} x_i ^2} + V_{\text{ext}}(x_i) + \sum_{j\ne i} 1/|x_j - x_i|\right)\right)}_{\hat{H}} \Psi(x) = E \Psi (x)  , 
$$

where $$x_i$$ is the location of the $$i$$-th atom, $$V_{\text{ext}}$$ is a external potential and where the equation was given in [Hartree atomic units](https://en.wikipedia.org/wiki/Hartree_atomic_units) (because that makes the equation way less cluttered).

If you have ever solve the Schrödinger equation for simple systems you will surely appreciate that the "ugly" part of the equation is the interactions between the electrons.
The hydrogen atom is one of the problems treatable in a analytical fashion, as it only has one electron, but even for the very simple helium atom-with its two electrons-we need to resort to approximations.
Wouldn't it be nice if we could just ignore the part with the interactions between electrons?
Well, that obviously gives the wrong answers, but another idea would be to find a way to describe the interaction potential in a more convenient way.
That's what the people that developed DFT thought as well and they came to the conclusion that one could reformulate the interaction potential in such a way that it looks like a external potential.
This reformulation takes the form of the so-called [Kohn-Sham equations](https://en.wikipedia.org/wiki/Kohn%E2%80%93Sham_equations) and can be proven to lead to the same electron density as the Schrödinger equation via the [Hohenberg-Kohn theorems](https://en.wikipedia.org/wiki/Density_functional_theory#Hohenberg%E2%80%93Kohn_theorems).
But all of this can be found elsewhere and I probably did not give a good account of it just then.

You might have guessed it already, but this sounds almost too good to be true.
And in a way it is, because the way in which we determine the "external potential-form of the interaction potential" now captures the complexity of the electron interactions.
This then leads to the uncomfortable fact of having to resort to approximations for determining this effective potential.
There are different approximations which have names like LDA, GGA or VDW, but again, these are described better somewhere else.

### Classical Density Functional Theory
We want to focus on doing cDFT here.
What is classical Density Function Theory, then?
Simply put, we follow a very similar goal to DFT, namely, calculating the density of particles which interact.
The only difference being, of course, that the particles are not electrons, but "classical" particles (i.e. particles which can be described by the laws of classical mechanics).
In a bit more detail, we want to calculate the equilibrium one-particle density $$\rho_0$$ (well-known observable of statistical mechanics), which is defined by

$$
\rho_0 (\vec{r}) := \left\langle \sum_ {i} \delta(\vec{r}-\vec{r}_{i} ) \right\rangle,
$$

where $$\vec{r}_i$$ is the position of the $$i$$-th particle and $$\langle\cdot\rangle$$ is the [ensemble average](https://en.wikipedia.org/wiki/Ensemble_average_(statistical_mechanics)).
Usually, the so-called grand-canonical ensemble is used, i.e. the system is thought to be in equilibrium with a heat bath and a particle bath, which makes the volume $$V$$, the temperature $$T$$ and the chemical potential $$\mu$$ the defining parameters of the system.

The governing equation (analogous to the Schrödinger equation for DFT) is then the grand canonical [functional](https://en.wikipedia.org/wiki/Functional_(mathematics)):

$$
\Omega_{\Phi} [\rho(\vec{r})] = \int \rho(\vec{r}) (V_{\text{ext}}(\vec{r}) - \mu )\mathrm{d}\vec{r} + \mathcal{F}_{\text{exc}}[\rho(\vec{r})] + \mathcal{F}_{\text{id}},
$$

where $$\mathcal{F}_{\text{exc}}$$ is the so-called excess free energy and $$\mathcal{F}_{\text{id}}$$ is the ideal free energy.
These [free energy terms](https://en.wikipedia.org/wiki/Helmholtz_free_energy) $$\mathcal{F}$$ are the most interesting part of the above equation.
The ideal part, i.e. the part of the thermodynamic free energy that a ideal gas (that is a non-interacting gas) would exhibit can be written down analytically {% cite Evans1979Apr %} and thus not that interesting, but the excess part is where the magic happens.
It can be shown that we get the equilibrium density $$\rho_0$$ out of the functional $$\Omega_{\Phi}$$ by [functional minimization](https://en.wikipedia.org/wiki/Calculus_of_variations) (same idea as Euler Lagrange formalism in classical mechanics).
But we are going to see that we can make our life even easier, pretty soon.

Now, we are just going to ignore the exact form of $$\mathcal{F} _{\text{exc}}$$ for the time being, because we ought to have a look at how exactly we may make our life easier first.
Later, we can deal with the "boring details".
Now, the trick of cDFT is pretty similar to the one pulled by Hohenberg, Kohn and Sham, we find a way of treating the interaction between particles (the $$\mathcal{F} _{\text{exc}}$$ part) as a external potential.
Then, if we manage to pull this bit of magic off, the equation is way simpler, as it will look like that of a ideal gas subjected to a external force.
If you want to learn how exactly we can do this, have a look at {% cite Evans1979Apr %}, which gives a super long and thorough treatment of everything and also is basically the foundation of the field of cDFT.
We will do everything in a hand-wavy sort of way, because the key concepts are easier to understand this way, IMHO.

First, start by performing a [functional derivative](https://en.wikipedia.org/wiki/Functional_derivative) on $$\Omega _{\Phi}$$ and set this derivative to 0, because this will yield $$\rho_0$$, the equilibrium density that we are interested in.
Think of it just like you would determine the minimum of a function by setting $$f(x) \overset{!}{=} 0 $$, just that in this case we determine the minimum of a functional rather than a function.
While performing the derivative, we encounter a term with the excess free energy functional in it.
We sieze the opportunity and define a new functional, called the direct correlation functional

$$
c [\rho (\vec{r})] := -\beta \frac{\delta \mathcal{F} _{\text{exc}}[\rho (\vec{r})]}{\delta \rho (\vec{r} ) },
$$

where $$\frac{\delta \cdot}{\delta \cdot}$$ is the functional derivative that we talked about before and $$\beta := 1/{k _{\text{B}}T }$$ is the inverse temperature, with $$k _{\text{B}}$$ being the [Boltzmann constant](https://en.wikipedia.org/wiki/Boltzmann_constant).
Don't worry if you do not know how such a derivative is performed, for the purposes of this discussion it does not matter all that much.
The fact that $$c[\rho (\vec{r})]$$ has its own name should be a sign to you that it has some importance in physics, which is true as it is related to the radial distribution function and similar important observables of a fluid, but here we are only interested in one thing: its use as a "effective external force".

The full solution of our minimization is given by

$$
\rho_0 (\vec{r}) = z\exp( -\beta V _{\text{ext}} (\vec{r}) + c[\rho_0] + \beta \mu _{\text{exc}} ),
$$

where $$z$$ is the so-called [fugacity](https://en.wikipedia.org/wiki/Fugacity) and the chemical potential $$\mu := \mu _{\text{id}} + \mu _{\text{exc}}$$ has been split into a ideal part and the excess part due to particle-particle interactions.
Don't pay too much attention to the details here.
Instead pay attention to the very interesting implications of this equation.
This indeed looks like the well-known equilibrium density of a ideal gas, which would look something like this:

$$
\rho _{\text{0}} (\vec{r}) = z \exp (-\beta V _{\text{ext}} (\vec{r})).
$$

The only difference to the equation above is that the latter includes what looks like a extra potential given by $$-\beta ^{-1} c[\rho _{\text{0}}]$$ (and a extra part with the excess chemical potential $$\mu _{\text{exc}}$$, which adds just a constant offset).
This is **the** important trick in cDFT.
Just as we did for the DFT method (introduction of the Kohn-Sham equations), we have packed the interactions into a effective potential and **reformulated the equations in a way so that the fluid looks like a non-interacting ideal gas in a external potential**.

Now, where the Kohn-Sham equations are a set of differential equations, the above equation for $$\rho _0$$ is a so-called self-consistency equation.
This essentially means that only $$\rho = \rho_0$$ will satisfy the equal sign correctly.
Interestingly, this property can also be used to iteratively converge on $$\rho _0$$ in a numerical method called [Picard-Iteration](https://en.wikipedia.org/wiki/Fixed-point_iteration#Picard_iteration).
The gist of this method is as follows:
 1. Guess a initial density distribution, e.g. by considering the bulk ideal gas solution $$\rho _{\text{ideal, blk}} := z\exp(\beta V _{\text{ext}} (\vec{r}))$$
 2. Next, insert this initial guess in the self-consistency equation, i.e.
 $$
 \tilde{\rho}_{\text{new}} = z\exp(\beta V _{\text{ext}} + c[\rho] + \beta \mu _{\text{exc}})
 $$
 3. Interpolate the old and the new guess linearly, proportional to the "mixing factor" $$\alpha$$ via 
 $$
 \rho _{\text{new}} = (1-\alpha) \rho _{\text{old}} + \alpha \tilde{\rho} _{\text{new}}
 $$
 4. Repeat the procedure from step 2. on until some convergence criterion is met.
 
If you are interested in this method in greater detail, a good source is Roth's review paper {% cite Roth2010Jan %}.
The mixing factor $$\alpha\in [0,1]$$ is necessary for if it is omitted, the iteration usually becomes unstable.
The higher it is set, the faster the iteration "progresses", but there is a higher probability for instabilities.
Thus, tuning this hyper-parameter is one of the main practical challenges of cDFT calculations.

Now, if you are like me, you might be sceptical at this point.
Surely, there has to be some cost to just packing the particle-particle interactions, i.e. The thing that makes the system so complicated, out of sight in this way.
And you would be totally right, unfortunately there is no free lunch in this case as well.
To cost has to be paid in terms of having to determine $$c[\rho]$$ in a sensible manner.
Usually (always ?), approximations have to be made to get a good choice for $$c$$.
The following section will deal with how such a approximation might look like.

## Approximations for Particle Interactions 
Just as was mentioned in the previous section, particle interactions have to be treated approximately to be able to use the Picard iteration method to converge on the equilibrium density.
Just as is the case for the quantum mechanics DFT, there is a whole family of different approximations.
Here, I just want to highlight a often used approximation, the so-called random phase approximation method.
