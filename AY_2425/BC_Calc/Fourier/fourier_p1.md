---
marp: true
html: true
---
# What is sound?

[watch this video](https://www.youtube.com/embed/6JeyiM0YNo4?si=iBHws45iXrHiIzNL)

---



# Activity

1. Create a script using https://randomwordgenerator.com/sentence.php


2. Two students to read sentences into your computer mic while [this oscilloscope](https://oscilloscope.sciencemusic.org/) is running

3. The same two students will read the same sentences while the [spectrogram](https://spectrogram.sciencemusic.org/) app runs



---
# Discuss
What are we looking at here?

![dolpin_spec](./images/Dolphin1.jpg)
Spectrogram of dolphin vocalizations; chirps, clicks and harmonizing are visible as inverted Vs, vertical lines and horizontal striations respectively.

---
# What is Sound?
<figure>
<img src="./images/Anatomy_of_the_Human_Ear.svg" width=500/>
<img src="./images/Organ_of_corti.svg" width=500/>
<figcaption> Cochlea (left), Organ of Corti (right) . CC license from wikipedia </figcaption>
</figure>

<!--![anatomy](./images/Anatomy_of_the_Human_Ear.svg){width=400}
![corti](./images/Organ_of_corti.svg)-->


---
# Fourier Analysis

$$
s(t) = \underbrace{\sum_{k=0}^{\infty} c_k \cos(kt)}_{\text{even}} + \underbrace{\sum_{k \geq 1}s_k \sin(kt)}_{\text{odd}}
$$

---
# Fourier Analysis

$$
\begin{align}
c_0 &= \frac{1}{2\pi} \int_{-\pi}^\pi s(\tau) d\tau\\
c_k &= \frac{1}{\pi} \int_{-\pi}^\pi s(\tau) \cos(k\tau) d\tau \\
s_k &= \frac{1}{\pi} \int_{-\pi}^\pi s(\tau) \sin(k\tau) d\tau
\end{align}
$$

---
# Live Example


