# Stylized Natural Language Question Synthesis

This is the final step in our data synthesis framework, focused on generating step-by-step chain-of-thought (CoT) solutions for `<database, question, SQL query>` triplets.

## Step 1: Chain-of-Thought Generation

Create CoT solutions for each data sample.

1. Run `python3 generate_cot_synthesis_prompts.py` to prepare prompts for CoT generation.
2. Execute `python3 synthesize_cot.py` to generate CoT solutions for `<database, question, SQL query>` samples. (Note: Ensure the `llm_inference()` function is implemented to integrate your preferred LLM. For each prompt, we sample multiple CoT solutions with a temperature of `0.8`.)

## Step 2: Post-Processing

1. Run `python3 post_process_cot.py` to perform execution-based major voting, selecting the most reliable CoT solutions.
2. Save the final synthetic `<database, question, SQL query, CoT solution>` samples to `./results/synthetic_text2sql_dataset.json`.