# LLMComparisonScale
 
A basic tool to quantify the capability of various LLMs.

To do so, we will first select our standard for a good LLM. This should ideally be the best LLM available for this system to work.

From there, we select a 'bad' standard. I'm unsure whether it would be better for this to be just random token generation or a standard 'bad' LLM. In the scoville scale or Tom7 example, the water or random move bot represents a canonically bad solution. I feel like random token generation may be the way to go, but idrk, open to other's thoughts

Finally, we use some objective tests to quantify the dilution needed to perform comparitatively to the LLM being tested. This is very vague, but I haven't fully figured out the details so that seems reasonable atm.

## Notable Issues / Points of Friction

- I'm kinda struggling to find things to act as the objective tests

- This idea was kinda based on being able to use the actual next token prediction with later GPTs. Chat completions make things weird. Gotta look into that.
  - I switched to using the completions endpoint and it works now, but still gotta find a way to use this for GPT-4+

## Current Progress

- I've started making calibration graphs to establish a baseline.
  - I am a bit concerned that the success rate is being affected more simply by luck of the draw on when davinci gets to input its token, but I guess it should be fine, this really isn't a very good test
    - hopefully increased resolution will fix that.
- I need to figure out a way to make sure files aren't overwritten. Atm they will be so I'm just manually doing that.
- I need to figure out why trying to use the evaluate_functional_correctness function from evaluate doesn't work and says it can't find the data module.

### Human Eval Score Testing
  - 10 Samples per test seems to yield roughly equal results to 1 sample per test at 500 tokens which makes sense
  - 10 SPT 1CPT 500 Tokens 3.5 Only: 
    - pass@1: 65.7% 
    - pass@10: 66.5%
  - 1 SPT 1CPT 500 Tokens 3.5 Only:
    - pass@1: 64.6% (test 1)
    - pass@1: 65.9% (test 2)
    - pass@1: 64.6% (test 3)
    - pass@1: 65.9% (test 4)
    - pass@1: 64.6% (test 5)
    - pass@1: 65.9% (test 6)

    **It's consistently one or the other, and it's the exact number every time.** 
  - 2 SPT 1CPT 500 Tokens 3.5 Only:
    - pass@1: 65.85% (test 1)
    - pass@1: 65.85% (test 2)

    **Weird**
  - 1 SPT 10 CPT 50 Tokens
    - pass@1: 65.9%
  - 1 SPT 100 CPT 5 Tokens (maybe the way to go given time vs result. Seems like success rate goes down with increased calls)
    - pass@1: 65.2% (test 1)
    - pass@1: 66.5% (test 2)
    - pass@1: 65.9% (test 3) (this is the average of the previous two and equal to the max of the 1CPT 500 Tokens 3.5 Only)
    - pass@1: 65.2% (test 4)
    - pass@1: 65.2% (test 5)
    - pass@1: 64.0% (test 6)

    (weird)
  - 1 SPT 500 CPT 1 Token (took like half an hour, maybe more)
    - pass@1: 64.6%


### Dilution Calibration
  - X-Axis: Dilution
  - Y-Axis: Successrate

#### Parameters:
  - 2 Samples Per Test
  - 100 Calls Per Test
  - 5 Tokens Per Call


  