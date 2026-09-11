# Article Structure for Wireless Communications Research

This guide provides detailed instructions for structuring and writing each section of a wireless communications research paper using the IMRAD format.

## Overall Structure

A typical wireless communications research paper follows this structure:

1. **Title** - Concise, descriptive
2. **Abstract** - 150-250 words
3. **Introduction** - 1-2 pages
4. **System Model** - 1-2 pages
5. **Proposed Method** - 2-3 pages
6. **Simulation Results** - 2-3 pages
7. **Discussion** - 1-2 pages
8. **Conclusion** - 0.5-1 page
9. **References** - All cited works

---

## 1. Title

**Purpose**: Clearly and concisely describe your research

**Guidelines**:
- Keep it under 15 words
- Include key technical terms
- Mention the specific technique or problem
- Avoid abbreviations unless widely known

**Good Examples**:
- "Resource Allocation for NOMA Systems with Deep Reinforcement Learning"
- "Beamforming Design for Intelligent Reflecting Surface Assisted MIMO Networks"
- "Energy-Efficient Power Control in Ultra-Dense Small Cell Networks"

**Poor Examples**:
- "A New Method for Wireless Communications" (too vague)
- "An RL-based NOMA Scheme with IRS for 6G" (too many abbreviations)

---

## 2. Abstract

**Purpose**: Standalone summary of the entire paper

**Structure** (write as flowing paragraphs, not labeled sections):

**Paragraph 1: Background and Problem** (2-3 sentences)
- Context: Why is this topic important?
- Problem: What is the specific challenge?

**Paragraph 2: Approach** (2-3 sentences)
- What is your proposed solution?
- What is novel about your approach?

**Paragraph 3: Results** (2-3 sentences)
- What are the key findings?
- Quantify improvements (e.g., "achieves 20% throughput gain")

**Length**: 150-250 words

**Example**:
```
Non-orthogonal multiple access (NOMA) has emerged as a promising technique for
enhancing spectral efficiency in 5G networks. However, conventional power
allocation schemes fail to adapt to dynamic channel conditions and user
requirements. This paper proposes a deep reinforcement learning-based power
allocation framework that optimizes sum-rate while maintaining user fairness
through intelligent power domain multiplexing. Our approach employs a
multi-agent deep deterministic policy gradient algorithm that learns optimal
power allocation policies through continuous interaction with the wireless
environment. Simulation results demonstrate that the proposed scheme achieves
23% higher sum-rate and 35% improvement in user fairness compared to
conventional fixed power allocation, while converging within 1000 training
episodes in practical network scenarios.
```

**Writing Tips**:
- Use complete sentences and flowing paragraphs
- Never use labeled sections (Background:, Methods:, etc.)
- Include specific quantitative results
- Mention key performance metrics

---

## 3. Introduction

**Purpose**: Motivate your research and present contributions

**Structure** (typically 3-4 paragraphs):

**Paragraph 1: Broad Context**
- Background on the wireless communication topic
- Why is this area important?
- Current trends or challenges

**Example**:
```
The exponential growth of mobile data traffic has driven the development of
fifth-generation (5G) wireless networks, which promise to support massive
connectivity, ultra-reliable low-latency communications, and enhanced mobile
broadband. Among the key enabling technologies for 5G, non-orthogonal multiple
access (NOMA) has attracted significant attention due to its potential to
improve spectral efficiency by serving multiple users in the same time-frequency
resource block through superposition coding and successive interference cancellation.
```

**Paragraph 2: Specific Problem**
- Narrow down to the specific problem you address
- What are the limitations of existing approaches?
- What is the gap in current research?

**Example**:
```
Despite the theoretical benefits of NOMA, practical implementation faces several
challenges. Conventional power allocation schemes typically rely on fixed power
ratios determined by channel state information, which fail to adapt to dynamic
network conditions and varying user requirements. Furthermore, most existing
works focus on simplified scenarios with ideal channel estimation, neglecting
the impact of estimation errors and interference from neighboring cells.
```

**Paragraph 3: Prior Work (Brief Literature Review)**
- What have others done?
- What are their limitations?
- How does your work differ?

> Follow the Core Principles in [related-work-improvement.md](related-work-improvement.md)（查证：读原文正文、核准目标函数；结构：分类分层、局限→动机；措辞：中性动词、术语溯源）— verify each paper against its full text before describing it.

**Example**:
```
Several approaches have been proposed to address power allocation in NOMA
systems. Game-theoretic methods [1-3] provide distributed solutions but often
converge to local optima. Optimization-based approaches [4-6] guarantee
optimality but require complete channel state information and high computational
complexity. Recent works have explored machine learning techniques [7-9], yet
most rely on supervised learning requiring extensive labeled training data and
lack generalization to unseen scenarios.
```

**Paragraph 4: Your Contributions**
- What is your proposed solution?
- What are the key contributions?
- What results do you achieve?

**Example**:
```
This paper proposes a deep reinforcement learning-based power allocation
framework for NOMA systems that addresses the limitations of existing approaches.
Our main contributions are: (1) We formulate the power allocation problem as a
Markov decision process that captures the dynamic nature of wireless channels;
(2) We design a multi-agent deep deterministic policy gradient algorithm that
learns optimal power allocation policies without requiring labeled training data;
(3) We demonstrate through extensive simulations that our approach achieves
significant improvements in both sum-rate and user fairness compared to
conventional schemes, while maintaining computational efficiency suitable for
real-time implementation.
```

**Writing Tips**:
- Use complete paragraphs (no bullet points in final manuscript)
- Cite key references using appropriate citation style
- Build a logical narrative: broad context → specific problem → your solution
- Keep it concise (1-2 pages maximum)

---

## 4. System Model

**Purpose**: Describe the wireless system and mathematical model

**Structure**:

**4.1 Network Topology**
- Describe the network layout
- Number and placement of base stations, users, obstacles
- Communication scenario (downlink, uplink, device-to-device)

**Example**:
```
Consider a downlink single-cell NOMA system where a base station (BS) equipped
with N_t antennas serves K single-antenna users. The users are randomly
distributed within a circular cell of radius R. The BS transmits superimposed
signals to all users simultaneously in the same time-frequency resource block.
```

**4.2 Channel Model**
- Mathematical representation of the channel
- Path loss, fading model, shadowing
- Antenna configuration

**Example**:
```
The channel vector between the BS and user k is denoted as h_k ∈ C^{N_t×1},
incorporating both large-scale path loss and small-scale Rayleigh fading. The
path loss is modeled as PL_k = PL_0 + 10n log_10(d_k/d_0), where PL_0 is the
path loss at reference distance d_0, n is the path loss exponent, and d_k is the
distance between the BS and user k.
```

**4.3 Signal Model**
- Transmitted and received signal equations
- Signal-to-interference-plus-noise ratio (SINR) expressions
- Key assumptions

**Example**:
```
The transmitted signal at the BS is given by x = ∑_{k=1}^K √(p_k) s_k, where p_k
is the allocated power for user k and s_k is the normalized data symbol with
E[|s_k|^2] = 1. The received signal at user k is y_k = h_k^H x + n_k, where
n_k ~ CN(0, σ^2) is additive white Gaussian noise. Users are ordered according
to their channel gains, with user 1 having the weakest channel and user K the
strongest.
```

**4.4 Performance Metrics**
- Define key metrics (sum-rate, energy efficiency, fairness, etc.)
- Mathematical expressions for metrics

**Example**:
```
The achievable rate for user k is R_k = log_2(1 + γ_k), where γ_k is the SINR
after successive interference cancellation. The system sum-rate is R_sum =
∑_{k=1}^K R_k. User fairness is measured using Jain's fairness index
J = (∑_{k=1}^K R_k)^2 / (K ∑_{k=1}^K R_k^2).
```

**Writing Tips**:
- Define all symbols at first use
- Use consistent notation throughout
- Number all equations for reference
- Clearly state all assumptions
- Include a table of notation if helpful

---

## 5. Proposed Method

**Purpose**: Present your solution in detail

**Structure**:

**5.1 Problem Formulation**
- Mathematical optimization problem
- Objective function, constraints
- Problem complexity analysis

**Example**:
```
The power allocation problem is formulated as:
max_{p_1,...,p_K} ∑_{k=1}^K R_k
s.t. ∑_{k=1}^K p_k ≤ P_total
     p_k ≥ p_min, ∀k
     R_k ≥ R_min, ∀k

This is a non-convex optimization problem due to the coupled interference terms
in the SINR expressions, making it NP-hard to solve optimally in polynomial
time.
```

**5.2 Proposed Approach**
- Overview of your method
- Key ideas and innovations
- Algorithm design

**Example**:
```
To address the computational complexity of the optimization-based approach, we
propose a deep reinforcement learning framework that learns optimal power
allocation policies through interaction with the environment. The key insight is
that the power allocation problem can be formulated as a Markov decision process
(MDP), where the BS (agent) observes the current channel state (state) and
allocates power to users (action) to maximize the sum-rate (reward) over time.
```

**5.3 Algorithm Details**
- Step-by-step description
- Mathematical derivations
- Algorithm pseudocode

**Example**:
```
Algorithm 1: DDPG-based Power Allocation

1: Initialize actor network μ(s;θ_μ) and critic network Q(s,a;θ_Q)
2: Initialize target networks μ' and Q' with same weights
3: Initialize replay buffer D
4: for episode = 1 to M do
5:     Observe initial channel state s_0
6:     for t = 0 to T-1 do
7:         Select action a_t = μ(s_t;θ_μ) + N_t
8:         Execute action, observe reward r_t and next state s_{t+1}
9:         Store transition (s_t, a_t, r_t, s_{t+1}) in D
10:        Sample random minibatch from D
11:        Update critic by minimizing loss
12:        Update actor using policy gradient
13:        Update target networks
14:    end for
15: end for
```

**5.4 Complexity Analysis**
- Computational complexity
- Convergence properties
- Practical considerations

**Example**:
```
The computational complexity of the proposed algorithm is O(K^2) per iteration,
mainly due to the critic network evaluation. The algorithm converges in
approximately 1000 episodes for a network with K=10 users, making it suitable
for real-time implementation with a time slot duration of 1 ms.
```

**Writing Tips**:
- Provide enough detail for reproducibility
- Use algorithm pseudocode for clarity
- Explain the intuition behind design choices
- Discuss practical implementation aspects

---

## 6. Simulation Results

**Purpose**: Present and analyze your results

**Structure**:

**6.1 Simulation Setup**
- Parameters and assumptions
- Comparison baselines
- Performance metrics

**Example**:
```
We consider a single-cell NOMA system with a BS located at the center of the
cell serving K=10 users randomly distributed within a radius of 500 m. The BS
is equipped with N_t=4 antennas, and each user has a single antenna. The path
loss exponent is n=3.7, the reference path loss at d_0=1 m is PL_0=38 dB, and
the noise power is σ^2=-90 dBm. The total transmit power is P_total=43 dBm.
We compare the proposed DDPG-based power allocation (DP-NOMA) against three
baselines: (1) Fixed Power Allocation (FPA) [4], (2) Game-Theoretic Power
Allocation (GTA) [2], and (3) Optimal Power Allocation (OPA) obtained through
exhaustive search.
```

**6.2 Performance Comparison**
- Present results for each metric
- Compare with baselines
- Use tables and figures effectively

**Example (Figure Description)**:
```
Figure 2 shows the sum-rate comparison versus total transmit power. As observed,
all schemes achieve higher sum-rate with increased transmit power. The proposed
DP-NOMA consistently outperforms FPA and GTA across all power levels, achieving
up to 23% improvement over FPA at P_total=43 dBm. The performance of DP-NOMA
approaches that of OPA, demonstrating near-optimal performance with significantly
lower computational complexity.
```

**6.3 Sensitivity Analysis**
- Impact of key parameters
- Robustness to assumptions
- Scalability analysis

**Example**:
```
Figure 3 illustrates the impact of the number of users on sum-rate performance.
As K increases from 5 to 20, the sum-rate initially increases due to multiuser
diversity but then saturates and decreases for K>15 due to increased inter-user
interference. The proposed DP-NOMA maintains its performance advantage across
all user numbers, demonstrating good scalability properties.
```

**Writing Tips**:
- Describe figures/tables in text (don't just say "as shown in Figure 2")
- Report both absolute and relative improvements
- Discuss statistical significance if applicable
- Be objective in presenting results
- Include error bars or confidence intervals for multiple runs

---

## 7. Discussion

**Purpose**: Interpret results and provide insights

**Structure**:

**7.1 Interpretation of Findings**
- What do the results mean?
- Why does your method work?
- Connection to theory

**Example**:
```
The superior performance of DP-NOMA can be attributed to its ability to learn
adaptive power allocation policies that respond to dynamic channel conditions.
Unlike FPA, which uses fixed power ratios regardless of channel state, DP-NOMA
allocates more power to users with favorable channel conditions while ensuring
minimum rate requirements for cell-edge users. This adaptive behavior explains
the significant improvement in sum-rate while maintaining user fairness.
```

**7.2 Comparison with State-of-the-Art**
- How does your work compare to recent literature?
- What are the advantages and limitations?

**Example**:
```
Compared to recent deep learning approaches for NOMA power allocation [7-9],
DP-NOMA offers two key advantages. First, it does not require labeled training
data, learning instead through trial-and-error interaction with the environment.
Second, the multi-agent formulation allows for distributed implementation,
reducing signaling overhead compared to centralized schemes. However, DP-NOMA
requires a training phase before deployment, which may not be suitable for
highly dynamic scenarios with rapidly changing user distributions.
```

**7.3 Limitations**
- What are the limitations of your approach?
- What assumptions could be relaxed?

**Example**:
```
Our work has several limitations that provide directions for future research.
First, we assume perfect channel state information at the transmitter, which
may not hold in practical systems with estimation errors and feedback delays.
Second, the training time of the DDPG algorithm increases with the number of
users, potentially limiting scalability to very large networks. Third, we focus
on a single-cell scenario and do not consider inter-cell interference, which
is crucial in multi-cell deployments.
```

**Writing Tips**:
- Go beyond describing results to explaining them
- Connect findings to theory and prior work
- Be honest about limitations
- Suggest specific directions for future work

---

## 8. Conclusion

**Purpose**: Summarize contributions and findings

**Structure** (1-2 paragraphs):

**Paragraph 1: Summary**
- Restate the problem and your approach
- Summarize key contributions

**Example**:
```
This paper proposed a deep reinforcement learning-based power allocation
framework for NOMA systems that addresses the limitations of conventional
schemes in dynamic network environments. By formulating the power allocation
problem as a Markov decision process and employing a multi-agent DDPG algorithm,
our approach learns optimal power allocation policies without requiring
extensive labeled training data or complete channel state information.
```

**Paragraph 2: Key Findings and Future Work**
- Summarize main results
- Suggest future research directions

**Example**:
```
Simulation results demonstrated that the proposed scheme achieves 23% higher
sum-rate and 35% improvement in user fairness compared to conventional fixed
power allocation, while maintaining computational efficiency suitable for
real-time implementation. Future work will extend the framework to multi-cell
scenarios with inter-cell interference, incorporate imperfect channel state
information, and explore transfer learning approaches to reduce training time
in new network deployments.
```

**Writing Tips**:
- Keep it concise (0.5-1 page)
- Don't introduce new results
- Be specific about contributions and findings
- End with concrete future work directions

---

## 9. References

**Purpose**: Cite all works referenced in the paper

**Guidelines**:
- Use IEEE citation style for wireless communications
- Include DOI links when available
- Verify all citations against original sources
- Balance between classic and recent works

**Example (IEEE Style)**:
```
[1] Y. Saito, Y. Kishiyama, A. Benjebbour, T. Nakamura, A. Li, and K. Higuchi,
    "Non-orthogonal multiple access (NOMA) for cellular future radio access,"
    in Proc. IEEE Veh. Technol. Conf. (VTC Spring), Dresden, Germany, Jun. 2013,
    pp. 1-5.

[2] Z. Ding, P. Fan, and H. V. Poor, "Random beamforming in millimeter-wave NOMA
    networks," IEEE Access, vol. 5, pp. 7667-7681, Apr. 2017.

[3] L. Lei, D. Yuan, C. K. Ho, and S. Sun, "Power and channel allocation for
    NOMA with deep reinforcement learning," IEEE J. Sel. Topics Signal Process.,
    vol. 13, no. 3, pp. 632-645, Jun. 2019.
```

---

## General Writing Principles

1. **Use Complete Paragraphs**: Never submit bullet points in the final manuscript
2. **Maintain Consistent Notation**: Define all symbols at first use
3. **Provide Smooth Transitions**: Connect ideas between sentences and paragraphs
4. **Be Precise and Concise**: Avoid unnecessary words while maintaining clarity
5. **Cite Appropriately**: Give credit to prior work and provide context
6. **Use Active Voice**: "We propose" is better than "It is proposed"
7. **Define Abbreviations**: Spell out at first use, then use abbreviation
8. **Number Equations**: Reference equations by number when discussing them
9. **Proofread Carefully**: Check for grammar, spelling, and formatting errors
10. **Follow Journal Guidelines**: Adapt to specific venue requirements

## Common Mistakes to Avoid

- ❌ Using bullet points in Introduction, Results, or Discussion
- ❌ Leaving abbreviations undefined
- ❌ Inconsistent notation or symbols
- ❌ Missing transitions between paragraphs
- ❌ Overstating results or claims
- ❌ Ignoring limitations of the approach
- ❌ Forgetting to number equations
- ❌ Incomplete or inaccurate citations
