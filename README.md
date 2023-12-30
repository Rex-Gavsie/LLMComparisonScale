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