# metrics-computation

`metrics-computation` is a tool for parsing and analyzing agent trajectories from [swebench.com](https://swebench.com). 

It helps inspect message patterns, tool usage, API-call behavior, and cost/performance trade-offs across different agentic coding models.

## Features

* **Parse** SWE-bench agent trajectories from dashboard URLs.
* **Count** system, user, assistant, and tool messages.
* **Analyze** top-performing agent runs.
* **Compare** resolution rates, API-call usage, and cost efficiency.
* **Evaluate** successful versus failed task behavior.

## Installation

```bash
git clone <repository-url>
cd metrics-computation
pip install -r requirements.txt
```

## Usage

### Basic Trajectory Analysis
```bash
metrics-computation --url "https://docent.transluce.org/dashboard/b038912e-0133-4594-b093-92806f8ffb17/agent_run/912a0729-eca8-495e-8453-9a445cc827a4?transcript_id=1b4be5e1-e434-4d7c-a288-a5c766006bf1"
```

### Example Output
```text
System messages:      1
User messages:        1
Assistant messages:  27
Tool messages:       30
=======================
Total messages:      59
```

### Deep Analysis
Use `main.py` to perform deeper analysis on the top 5 agent trajectories from SWE-bench:
```bash
python main.py
```

## Key Findings

### 1. More API Calls Can Reduce Overall Model Cost
Based on data collected from SWE-bench trajectories:
* **Claude 4.5 Opus** (high reasoning) achieves the highest task resolution rate among evaluated models, but at a significantly higher cost than **MiniMax M2.5** (high reasoning).
* Models making more external API/tool calls can often reduce total model processing costs by relying less on internal reasoning.
* Despite averaging the highest number of API calls, MiniMax M2.5 (high reasoning) achieves the same resolution rate as **Gemini 3 Flash** (high reasoning) at a fraction of the cost.
* MiniMax M2.5 offers the strongest cost-to-performance ratio in this evaluation.

> **Note:** Systems with expensive external APIs, rate limits, or latency-sensitive workloads may still benefit from models like Claude 4.5 Opus, which rely more heavily on internal reasoning and less on external tooling.

#### Resolution Rate vs Cost

| Model | Resolved | Avg Calls | Total Cost |
| :--- | :---: | :---: | :---: |
| Claude 4.5 Opus (high reasoning) | 76.8% | 32.896 | $376.95 |
| Gemini 3 Flash (high reasoning) | 75.8% | 56.126 | $177.98 |
| MiniMax M2.5 (high reasoning) | 75.8% | 60.450 | $36.64 |
| Claude Opus 4.6 | 75.6% | 28.932 | $275.76 |
| GPT-5-2 Codex | 72.8% | 28.072 | $224.71 |

---

### 2. Message Distribution Analysis
Using the `metrics-computation` tool, we observed a similar trend in message and tool-call distributions.


| Model | System Msgs | User Msgs | Assistant Msgs | Tool Msgs |
| :--- | :---: | :---: | :---: | :---: |
| Claude 4.5 Opus (high reasoning) | 500 | 502 | 16,446 | 18,757 |
| Gemini 3 Flash (high reasoning) | 500 | 505 | 28,054 | 27,559 |
| MiniMax M2.5 (high reasoning) | 500 | 506 | 30,219 | 29,722 |
| Claude Opus 4.6 | 500 | 500 | 14,466 | 14,956 |
| GPT-5-2 Codex | 500 | 503 | 17,520 | 17,918 |

**Observation:** Models with higher tool-call counts generally produced more assistant messages, more iterative reasoning, and lower total inference costs.

---

### 3. Open-Source Models Show Strong Cost Efficiency
Open-source-oriented models such as MiniMax M2.5 achieved task completion rates comparable to leading closed-source systems while operating at a substantially lower cost. This highlights the growing competitiveness of efficient reasoning models that rely heavily on external tooling.

---

### 4. Cost Analysis: Successful vs Failed Tasks
* Failed tasks consistently required **higher average cost** and **more API calls** across all evaluated models.
* Failed-task trajectories were generally **less than 2×** the cost/call count of successful tasks, suggesting failures were not primarily caused by runaway execution or excessively long trajectories.

> *Note: Per-instance details for GPT-5-2 Codex were unavailable on SWE-bench and therefore could not be included in this analysis.*

#### Success vs Failure Metrics

| Model | Avg Success Cost | Avg Fail Cost | Avg Success Calls | Avg Fail Calls | Success Count | Fail Count |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Claude 4.5 Opus (high reasoning) | $0.6308 | $1.1614 | 29.72 | 43.41 | 384 | 116 |
| Gemini 3 Flash (high reasoning) | $0.3402 | $0.4054 | 54.66 | 60.70 | 379 | 121 |
| MiniMax M2.5 (high reasoning) | $0.0603 | $1.1141 | 54.23 | 79.92 | 379 | 121 |
| Claude Opus 4.6 | $0.4464 | $0.8771 | 25.84 | 38.50 | 378 | 122 |

## Conclusion

This analysis suggests a strong relationship between tool/API usage, reasoning strategy, and total operational cost.
* More API/tool calls can reduce model inference costs.
* High-tool-usage models can remain highly competitive on task completion.
* MiniMax M2.5 demonstrated the strongest cost-efficiency tradeoff among evaluated models.
* Lower internal reasoning cost does not necessarily reduce performance quality.

## Future Work

Potential extensions for `metrics-computation`:
* Per-step latency analysis
* Token-level cost tracking
* Visualization dashboards
* Failure trajectory clustering
* Tool efficiency scoring
* Benchmark comparison across datasets
