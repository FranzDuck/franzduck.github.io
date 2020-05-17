---
layout: post
title: "Simulating Shit for Fun and Profit 1"
date: 2020-5-17
usemathjax: true
---

A fascinating fact of physical theories is that they enable us to compute everything.
By that I mean, once you have found out the rules that govern a system, for example $$F = ma$$ for mechanics, you can in theory calculate any possible system described by those rules.
No limitations on how far into the future you want to look (or into the past, if you wish).
Just plug in the numbers and you can predict the future in its entirety.

Even more fascinating is what you usually learn next: that in practice we are not even able to solve the simplest systems.
This apparent contradiction, that on one hand everything should be computable in its entirety, but that on the other hand even the systems close to the absolute basic examples are not solvable, is perplexing at first.
The most well-known example of a system that illustrates how the mathematics explaining a simple system explode in complexity once you add a simple "complication" is the [double pendulum](https://en.wikipedia.org/wiki/Double_pendulum) system.
A single pendulum is solvable (although some still think that working out the solution is pretty tedious for how simple the system actually is), but once you add another pendulum to the first one, the equations get incredibly complex, albeit being still solvable.
A even better example is the [three body problem](https://en.wikipedia.org/wiki/Three-body_problem).
The two body problem (think earth and moon in space) was solved by [Kepler](https://en.wikipedia.org/wiki/Johannes_Kepler) in the 17th century.
Finding the solution is pretty complex, but doable.
Adding just a single body to the system changes everything.
Although there have been some [special cases with nice solutions](https://en.wikipedia.org/wiki/Three-body_problem#Special-case_solutions), the problem, in general it is thought to be unsolvable.
As someone who always thought that we could in practice calculate everything, this came as somewhat of a shock when I first heard about it.
It felt wrong, that we have found (most) of the rules that govern the behavior of physical systems, but can not even calculate how the system of sun, earth and moon works.

Of course people have figured out how we can learn the superpower of predicting what systems with even, say, 10000 bodies do in the years since Kepler.
The magic that one has to learn to be able to "solve the unsolvable systems", is of course numerical simulation.
In the following I want to show, how one can write a simple algorithm that calculates the solution to a three, four, five, etc. body problem.
But, as there is no free lunch, we have to pay a price.
The price in this situation is, that we no longer get a exact solution, but "just" a arbitrarily close approximation.
And while it definitely feels like we are not getting "the real thing", if we calculate a approximate answer, we have to keep in mind that "arbitrarily close" is pretty good.
If we are interested in knowing something with little uncertainty, then we must increase the accuracy until the solution is better than what we want to know.
Say that for example you are in charge of a space agency and want to calculate how you can send a probe to mars. 
You know that there is already a uncertainty associated with the way your rocket can move, e.g. maybe the thrusters controlling the attitude can fire for durations with uncertainty of 1 millisecond.
This uncertainty then causes your rocket to be slightly off from the perfect attitude.
And while you of course correct those mistakes on the fly by constant feedback loops, you will not be able to land at exactly the spot down to millimeter accuracy.
Calculating the position of mars on to a higher accuracy than what your lander is capable of achieving in its steering then is enough to land where we want to anyways.

If you are anything like me, trying to write a simulator script sounds great, and you will want to get cracking.
Let's start by examining how one solves mechanical problems.
While we can use numerical techniques to solve problems in other domains (quantum mechanics, general relativity, etc.) mechanical problems are the best to start out on.
There are two reasons for that, the first one being that "mechanical simulations" are still one of the most important areas that numerical simulation are applied to.
The second reason being that we as humans have evolved a good intuition on what mechanical systems do, and thus are able to spot when a system behaves not as it ought to.
This is immensely useful in fixing bugs.
Ok back to the topic: how do we solve a mechanical problem?
As I wrote in the very beginning the main "rule" describing any mechanical system is $$F = ma$$.
Now let me quickly show how one would for example solve the problem for a ball falling under constant force.
Take the aforementioned formula with the knowledge that the acceleration $$a$$ is the second derivative of the location.
If a body in a constant gravitational field feels a constant force proportional to some constant $$g$$ times its weight $$m$$, then we may write:

$$
\begin{gather}
F = m a = m \dot{v} = m \ddot{x} = F_{ \text{grav}} = m g,
\end{gather}
$$

where $$v$$ is the velocity of the particle and $$x$$ the position.
If you are not familiar with the notation of writing dots for derivations of the time variable, note that $$\dot{a} = a'(t)$$ in the notation that most student learn in school.

This in fact is a simple form of a differential equation.
The fact that such systems are described by differential equations and solving differential equations is hard, is the reason why even slightly more complex systems become unsolvable in general as I have mentioned above.
Now normally you would take the last part of the equation and integrate it twice to obtain the solution:

$$
\begin{gather}
m \ddot{x} = m g \Leftrightarrow \ddot{x} = g \text{, integrate once:}\\
\Leftrightarrow \dot{x} = gt + v_0 \text{ integrate a second time:}\\
\Leftrightarrow x = \frac{1}{2} g t^2 + v_0 t + x_0.
\end{gather}
$$

If you could not follow the derivation above, don't worry.
While the technical steps used are not particularly hard they are also not required to understand the rest of what I am going to write.
The important thing is how the above equation was determined: by integration.
This, as was already mentioned above is not possible in general, even if we just increase the complexity by a tiny bit, for example if we were to add another body to the equation that interacts with the first body.
The second important thing is the interpretation of the equation.
The function $$x = \frac{1}{2} g t^2 + v_0 t + x_0$$, where $$x$$ is usually written $$x(t)$$ to show that it is a function dependent on time, describes the bodies' position over time.
This is the powerful feature of physics that fascinates me: if we know the initial velocity $$v_0$$ and the initial position $$x_0$$, we can compute the bodies' entire history ($$t$$ negative) and future ($$t$$ positive).
Just insert the respective numbers (preferably all in the same [unit system](https://en.wikipedia.org/wiki/International_System_of_Units)) and set $$t$$ to the time that you are interested in, and the above function magically returns where the body will be at that particular time.

## Deriving a Integration Scheme

If we now succeed in obtaining a scheme with which such a integral equation can be solved without applying the integration steps, we would have a very powerful system.
I am going to gloss over quite a number of important facts in the following derivation of a "numerical integrator", but we are here to have fun, not to understand the minutia (there are already countless books on that topic and none of them were anywhere near "fun" last time I checked).
So here goes our "handwaving" derivation:
Recall from your calculus class that the derivation is determined by forming the limit of the difference quotient:

$$
\begin{gather}
\dot{x}(t) = x'(t) = \lim_{h \to 0} \frac{x(t+h) - x(t)}{h}
\end{gather}
$$

The idea is now to accept that we are not exactly determining the limit of $$h\to 0$$ if we choose $$h$$ to be a "small number" but instead only get a approximation of the derivative.
For example just set $$h = 0.0000001$$ and you might get very close to the actual value.
To denote that we are only working with a "approximate limit" we often use $$\Delta t$$ instead of $$h$$.
Hence the equation becomes:

$$
\begin{gather}
\dot{x}(t) \approx \frac{x(t+\Delta t) - x(t)}{\Delta t} \text{ for small } \Delta t.
\end{gather}
$$

Cool, right?
No longer do we have to derive the derivative using the "complicated" rules that we learned in school.
Just insert the numbers in the equation and you are done.
One important thing to note: Of course it is hard to say what is a sufficiently small number for $$\Delta t$$.
Some processes might change a lot in a very short amount of time and thus require a higher "resolution" in time, i.e. a smaller value for $$\Delta t$$ than other processes.
As an example: If we want to calculate the trajectory of a bullet, we would have to take way smaller "steps" in time (a bullet takes a fraction of a second to reach a near target) than if we want to calculate the trajectory of the earth in the solar system (the earth takes a whole year to revolve around the sun).

Now that you have seen the basic mechanism of numeric estimation, let's get back to the problem at hand.
Let's rewrite the differential equation for the velocity, which we saw above:

$$
\begin{gather}
v(t) = \dot{x}(t) = gt + v_0 \text{, now let's apply the approximation:}\\
\dot{x}(t) \approx \frac{x(t+\Delta t) - x(t)}{\Delta t} = gt + v_0
\end{gather}
$$

Now we have not really gained anything in terms of integration so far, but if we reformulate the latter half of the last equation we obtain

$$
\begin{gather}
\frac{x(t+\Delta t) - x(t)}{\Delta t} = gt + v_0 \Leftrightarrow x(t + \Delta t) = gt\Delta t + v_0 \Delta t + x(t)
\end{gather}
$$

If you have not (yet) written many iterative programs you might not realize why the last equation is remarkable.
But this equation in fact is a great success, actually it is (almost) the complete solution to our problem.
The above equation is a iterative description of how to calculate the complete trajectory (approximately of course) given a initial position $$x(t)$$ for a later time $$x(t+\Delta t)$$.
The fact that the second point calculated using the above formula is only one a small fraction of time later than the first one does not disturb us, as we can just apply the equation to the new point again and thus obtain the position at twice the time step: $$x(t + \Delta t)$$.
And because computers are extremely good at such calculations we don't even have to calculate a lot.
Just let the computer do the work.
This is the sort of solution that I really like, because you invest some thought into a scheme which allows one to offload all the work onto a computer, and then you can just lazily wait for it to finish its calculations.

## Recap
Let's quickly restate what we have learned so far, before the new learned facts evaporate into thin air.
Physical systems are described using differential equations (which for mechanics is done by applying Newtons second law).
Because these equations quickly become unsolvable for more complex systems, and because we are lazy as hell, we want to find a method of solving the equations approximately with a computer.
This can be done by approximating the difference quotient for small steps in time.
Finally we arrived at a equation which iteratively lets us calculate the position of a particle/body, allowing us to obtain a complete trajectory.
Implementing this iteration would free us of slaving over the calculations (at least if your job was to calculate trajectories) because we can just give the work to a more competent entity, i.e. a computer.

##Outlook
In the next part we want to get to coding the integrator in a more general form.
This will allow us to calculate the trajectory of a falling body, so yeah... That's something to look forward to.
