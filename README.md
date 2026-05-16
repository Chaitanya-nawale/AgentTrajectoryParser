# metrics-computation is a tool which can be used to parse and analyse agent trajectories from swebench.com

Tool usage:
metrics-computation --url "https://docent.transluce.org/dashboard/b038912e-0133-4594-b093-92806f8ffb17/agent_run/912a0729-eca8-495e-8453-9a445cc827a4?transcript_id=1b4be5e1-e434-4d7c-a288-a5c766006bf1"
 
System messages:      1
User messages:        1
Assistant messages:  27
Tool messages:       30
=======================
Total messages:      59

# Use main.py to do a deeper analysis of top 5 agent trajectories on the website. Here are some of the points that I got to know from the website:
1. More API calls ⇒ Lower model cost: (Based on the data fetched from the swebench.com website)

  1. Although Claude 4.5 Opus (high reasoning) delivers the highest task resolution rate among the models tested, it costs much higher than MiniMax M2.5 (high reasoning).

  2. Models that make more API calls can often reduce overall processing cost. By relying more on external calls, the model performs fewer assumptions and less internal reasoning per task, which can lower total model costs while maintaining comparable resolution rates.

  3. Despite averaging the highest number of API calls, MiniMax M2.5 (high reasoning) reaches the same 75.8% resolution rate as Gemini 3 Flash (high reasoning) at only a fraction of the cost. This makes MiniMax M2.5 the strongest option from a cost-to-performance perspective.

  4. MiniMax M2.5 (high reasoning) provides better cost for value. However, in applications where external API calls are costlier than model processing, this might not be a suitable option.

  5. In systems where external API calls are expensive, rate-limited, or add more latency, models like Claude 4.5 Opus (high reasoning) may still be the more practical option because they rely less on external tooling and more on internal reasoning.

  NAME                                RESOLVED   AVG CALLS    TOTAL COST
  ——————————————————————————————————————————————————————————————————————
  Claude 4.5 Opus (high reasoning)      76.8%      32.896       $ 376.95
  Gemini 3 Flash (high reasoning)       75.8%      56.126       $ 177.98
  MiniMax M2.5 (high reasoning)         75.8%      60.45        $  36.64
  Claude Opus 4.6                       75.6%      28.932       $ 275.76
  GPT-5-2 Codex                         72.8%      28.072       $ 224.71

2. metrics-computation tool usage:

  1. With the help of the tool developed, we observe the similar pattern which is shown in the following table:

  NAME                                SYSTEM MSGS  USER MSGS  ASSISTANT MSGS  TOOL MSGS
  —————————————————————————————————————————————————————————————————————————————————————
  Claude 4.5 Opus (high reasoning)    500          502        16446           18757
  Gemini 3 Flash (high reasoning)     500          505        28054           27559
  MiniMax M2.5 (high reasoning)       500          506        30219           29722
  Claude Opus 4.6                     500          500        14466           14956
  GPT-5-2 Codex                       500          503        17520           17918

3. Open-source models such as MiniMax M2.5 achieved comparable task completion counts to leading closed-source models while operating at substantially lower cost.

4. Cost analysis for successful vs. failed tasks:
  1. As expected, failed tasks had a higher average cost and required more API calls than successfully resolved tasks across all evaluated models.
  2. Interestingly, the average cost and API calls for failed tasks were generally less than 2× those of successful tasks. This suggests that failures did not typically result from runaway execution or excessively long agent trajectories.
  3. Unfortunately, per-instance details for GPT-5-2 Codex were unavailable on swebench.com, so it could not be included in this analysis.

  NAME                                AVG_SUCCESS_COST  AVG_FAIL_COST  AVG_SUCCESS_CALLS  AVG_FAIL_CALLS  SUCCESS_COUNT  FAIL_COUNT
  —————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
  Claude 4.5 Opus (high reasoning)    $0.6308           $1.1614          29.72              43.41         384            116
  Gemini 3 Flash (high reasoning)     $0.3402           $0.4054          54.66              60.70         379            121
  MiniMax M2.5 (high reasoning)       $0.0603           $0.1141          54.23              79.92         379            121
  Claude Opus 4.6                     $0.4464           $0.8771          25.84              38.50         378            122
