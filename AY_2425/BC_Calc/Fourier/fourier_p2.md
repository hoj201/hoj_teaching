---
marp: true
---

# Goal

On the left is a spectrogram of a violin
We would like to understand the striation patterns

![bg right](images/Spectrogram_of_violin.png)

[watch this video](https://www.youtube.com/embed/6JeyiM0YNo4?si=iBHws45iXrHiIzNL)

<!-- 5 minutes -->
---

# Modelling a violin string

Let's model the deviation of the string as a function of space and time, $h(x,t)$ with the boundary condition:

$$
h(-\pi,t) = h(\pi,t) = 0
$$

![bg right](images/violin-strings.jpg)

<!-- 10 minute walk through the process of going from a function of space to a function of space time starting at t=0 -->

---

# The wave equation

$$
\frac{\partial^2 h}{\partial t^2} =  \kappa \frac{\partial^2 h}{\partial x^2}
$$

![bg right](images/hokusai.jpg)

<!-- 5 minutes You will need to explain the notion of a partial derivative-->
<!-- 5 minutes You will also need to explain how this is physically justified.  Do this with a picture-->

---

# Question
Assume

$$
  h(x,t) = s(t) \sin(nx)
$$
for some fixed $n$.
Can we choose $s(t)$ so that $h(x,t)$ satisfies the wave equation?

<!-- Check students understand the question (5 minutes) -->

---

# Answer (yes)

$h(x,t) = s(t) \sin(nx)$ satisfies the wave equation if (and only if)

$$
    \frac{d^2 s}{dt^2} = -\kappa n^2 s
$$
for $n=1,2,\dots$

This is a differential equation of a single variable!
Can we solve it?

<!-- See if the students can solve this (2 minutes) -->

---

# Solution

$$
h(x,t) = \left( A \sin( n \sqrt{\kappa} \cdot  t) + B \cos(n \sqrt{\kappa} \cdot t) \right) \cdot \sin(nx)  
$$
satisfies the wave equation

$$
\frac{\partial^2 h}{\partial t^2} =  \frac{\partial^2 h}{\partial x^2}
$$
and the boundary condition $h(-\pi,t) = h(\pi,t) = 0$.

<!-- You should have 15-20 minutes left -->

---

# Linearity
If we have two such solutions
$$
\begin{align}
    h_1(x,t) &= (A \sin(n \sqrt{\kappa} \cdot t) + B \cos(n \sqrt{\kappa} \cdot t)) \sin(nx) \\
    h_2(x,t) &= (C \sin(m \sqrt{\kappa} \cdot t) + D \cos(m \sqrt{\kappa} \cdot t)) \sin(m x)
\end{align}

$$
Then is
$$
    h(x,t) = h_1(x,t) + h_2(x,t)
$$
also a solution?


---
# General solution of the wave equation

$$
    h(x,t) = \sum_{k=1}^{\infty} (A_n \sin(n \sqrt{\kappa} \cdot t) + B_n \cos(n \sqrt{\kappa} \cdot t)) \sin(nx)
$$

<!-- note how the only oscillations we see in time are integers multiples of root(kappa)-->

---

# Goal

On the left is a spectrogram of a violin
We would like to understand the striation patterns

![bg right](images/Spectrogram_of_violin.png)

[watch this video](https://www.youtube.com/embed/6JeyiM0YNo4?si=iBHws45iXrHiIzNL)

