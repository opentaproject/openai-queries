\title{
TIF106 - Nonequilibrium processes in physics, biology, and chemistry
}

Johannes Hofmann, johannes.hofmann@physics.gu.se
TA: Enrique Rozas Garcia, enrique.rozas.garcia@physics.gu.se

\section*{Random Walk with Pauses}

Question: Consider a discrete random walk on a line with equal step lengths. Different from the lectures, assume that an addition to a move to the right (with probability $p$ ) and a move to the left (with probability $q$ ), the walker can remain on the spot and not move.
a) Write down the distribution for the position $m$ after $N$ steps. Hint: Introduce a variable for the number of steps in place and extend the combinatorial argument from the lectures.
b) Show that the mean displacement is given by
\[
\mu=N(p-q)
\]
and the variance
\[
\sigma_{m}^{2}=N\left[p+q-(p-q)^{2}\right] .
\]

Hint: Use the multinomial theorem: https://en.wikipedia.org/wiki/Multinomial_theorem.
Solution: a) Since the steps are independently distributed, the probability of a combination with $n_{r}$ steps to the right, $n_{l}$ steps to the left, and $N-n_{r}-n_{l}$ steps to the same position is given by $p^{n_{r}} q^{n_{l}}(1-p-q)^{N-n_{r}-n_{l}}$. The displacement for such a configuration is $m=n_{r}-n_{l}$.
Now we apply a combinatorial argument. For a fixed $n_{r}, n_{l}$ there are
\[
\frac{N!}{n_{r}!n_{l}!\left(N-n_{r}-n_{l}\right)!}=\binom{N}{n_{r}, n_{l}, N-n_{r}-n_{l}}
\]
ways to arrange the steps. We thus have
\[
P(m)=\sum_{n_{r}-n_{l}=m}\binom{N}{n_{r}, n_{l}, N-n_{r}-n_{l}} p^{n_{r}} q^{n_{l}}(1-p-q)^{N-n_{r}-n_{l}},
\]
where the sum is over pairs of $\left\{n_{r}, n_{l}\right\}$ that are consistent with the total displacement $m$.
b) For this exercise we note that the distribution (2) corresponds to the coefficients of the expansion of $(p+q+c)^{N}$, where $c=1-p-q$. Using the same trick introduced for the binomial distribution in the lectures, we can introduce a dummy variable $u$ and take derivatives w.r.t it to generate the moments.

To compute the mean we evaluate
\[
\begin{aligned}
\langle m\rangle & =\sum_{m=-N}^{N} m P(m)=\left.\sum_{m=-N}^{N} u \frac{d}{d u} u^{m}\right|_{u=1} P(m) \\
& =\left.u \frac{d}{d u} \sum_{m=-N}^{N} \sum_{n_{r}-n_{l}=m}\binom{N}{n_{r}, n_{l}, N-n_{r}-n_{l}} u^{m} p^{n_{r}} q^{n_{l}}(1-p-q)^{N-n_{r}-n_{l}}\right|_{u=1} \\
& =\left.u \frac{d}{d u} \sum_{n_{r}, n_{l}}\binom{N}{n_{r}, n_{l}, N-n_{r}-n_{l}}(u p)^{n_{r}}(q / u)^{n_{l}}(1-p-q)^{N-n_{r}-n_{l}}\right|_{u=1} \\
& =\left.u \frac{d}{d u}\left(u p+\frac{q}{u}+[1-p-q]\right)^{N}\right|_{u=1}=\left.u\left(p-\frac{q}{u^{2}}\right)\left(u p+\frac{q}{u}+[1-p-q]\right)^{N-1}\right|_{u=1} \\
& =N(p-q) .
\end{aligned}
\]

Note that this is what one expects intuitively, since on average we will take $N p$ steps to the right and $N q$ steps to the left.

The variance can be obtained by using the same trick to calculate the second moment
\[
\begin{aligned}
\left\langle m^{2}\right\rangle & =\sum_{m=-N}^{N} m^{2} P(m)=\left.\sum_{m=-N}^{N}\left(u \frac{d}{d u}\right)^{2} u^{m}\right|_{u=1} P(m) \\
& =\left.\left(u \frac{d}{d u}\right)^{2}\left(u p+\frac{q}{u}+[1-p-q]\right)^{N}\right|_{u=1} \\
& =N(N-1)(p-q)^{2}+N(p+q),
\end{aligned}
\]
and so the variance is
\[
\sigma^{2}=N(N-1)(p-q)^{2}+N(p+q)-N^{2}(p-q)^{2}=N\left[p+q-(p-q)^{2}\right] .
\]

Note that for $p+q=1$ we must get back the results we obtained for the binomial distribution.