from llm import all_prompt

class prompts_fewshot_parse:## fewshot parse prompt
    parse_fewshot= all_prompt.prompts_fewshot_parse2

class prompts1:
    extract_prompt= all_prompt.extract_prompt
    new_prompt=all_prompt.new_prompt0
    correct_prompt=all_prompt.correct_prompt

class prompts_wo_hint_only_sqllike_reparse_ext_atom(prompts1):# deepseek 68  qwenmax 61  全量：
    new_prompt=all_prompt.new_prompt2
    extract_prompt=all_prompt.reparse_extract_prompt
    noun_prompt=all_prompt.noun_prompt
    correct_prompt=all_prompt.correct_prompt_wo_hint


class prompts_wo_hint_only_sqllike_reparse_ext_atom_step(prompts1):# deepseek 68  qwenmax 61  全量：
    new_prompt=all_prompt.new_prompt3
    tmp_prompt=all_prompt.new_prompt1
    extract_prompt=all_prompt.reparse_extract_prompt
    noun_prompt=all_prompt.noun_prompt
    correct_prompt=all_prompt.correct_prompt_wo_hint
    soft_prompt=all_prompt.soft_prompt

class db_check_prompts(prompts_wo_hint_only_sqllike_reparse_ext_atom_step):
    extract_prompt=all_prompt.new_extract_prompt
    extract_prompt_wofewshot=all_prompt.new_extract_prompt_wofewshot
    new_prompt=all_prompt.new_prompt_O
    new_prompt_wocot=all_prompt.new_prompt_O_wocot
    new_prompt_uns_cot=all_prompt.new_prompt_unstruct_cot
    tmp_prompt=all_prompt.new_prompt3
    tmp_prompt_wocot=all_prompt.new_prompt3_wocot
    select_prompt=all_prompt.select_prompt
    vote_prompt=all_prompt.vote_prompt
class sft_prompts(prompts_wo_hint_only_sqllike_reparse_ext_atom_step):
    new_prompt=all_prompt.new_prompt1
    
class prompts_wo_hint_only_sqllike_reparse_ext(prompts1):#
    new_prompt=all_prompt.new_prompt1
    extract_prompt=all_prompt.reparse_extract_prompt
    noun_prompt=all_prompt.noun_prompt

class prompts_wo_hint_no_sqllike(prompts1):#5
    new_prompt=all_prompt.new_prompt_wo_hint_standQ_newsqllike

class prompts_wo_hint_no_sqllike5(prompts1):#57
    new_prompt=all_prompt.new_prompt_wo_hint_standQ
    
class prompts_wo_hint_only_sqllike(prompts1):#58 dev 57.89  #当前sota
    new_prompt=all_prompt.new_prompt1

class prompts_wo_hint_no_sqllike4(prompts1):#55
    extract_prompt= all_prompt.extract_prompt_wo_hint_no_Sqllike
    new_prompt=all_prompt.new_prompt_wo_hint_new_sqllike

class prompts_wo_hint_no_sqllike3(prompts_wo_hint_no_sqllike):
    extract_prompt= all_prompt.extract_prompt_wo_hint_no_Sqllike
    new_prompt=all_prompt.new_prompt_wo_hint_new_sqllike_wodb
    correct_prompt=all_prompt.correct_prompt_nodb

class prompts_wo_hint_no_sqllike_2(prompts_wo_hint_no_sqllike):
    new_prompt=all_prompt.new_prompt_wo_hint_no_sqllike
    