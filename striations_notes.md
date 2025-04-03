# Striations in Spectrograms

1. Play cello while running https://spectrogram.sciencemusic.org/.  Pause on a frame.
2. Explain what a spectrogram is on the white-board referencing the frame.
3. Note the striation patterns and pose the quantization question "What can $k$ be if $\sin(kx)=0$ at $x=\pm \pi$?"
4. Display it in Desmos: (mark nodes, graph $\sin(kx)$ and add a slider to $k$)
5. Note that we only car about how our ear-drums oscillate in time (not how a string's height oscillates in space)
6. Introduce the function $h(x,t)$.
7. Introduce the wave equation $\partial_t^2 h = 9 \partial_x^2 h$ and the boundary conditions.  Maybe explain it a bit.
8. Consider the ansatz $(x^2-\pi^2)t$.  Show how it does not satisfy the wave equation.
9. Consider the ansatz $\sin(x)\sin(3t)$.
10. Show linearity property
11. Show general solution $$\sum_k a_k \sin(kx) \sin(3kt) + b_k \sin(kx) \cos(3kt)$$
12. Tie this to the spectrogram and the striation patterns