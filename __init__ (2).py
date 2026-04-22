# Machine-readable schema registry.
# Source of truth: SCHEMA.excalidraw (the diagram).
# Any code that disagrees with this yaml is wrong — fix the code, not
# the yaml.

version: 1

# Every .md file the flow touches. verify_integrity.py checks these.
files:
  # PROTOCOL
  - PROTOCOL/main_index.md
  - PROTOCOL/soul.md
  - PROTOCOL/tiny/_readme.md

  # ARCHIVE
  - ARCHIVE/system_archive_file_record.md
  - ARCHIVE/codes/_readme.md

  # MEMORY (self)
  - MEMORY/index.md
  - MEMORY/self/short_term.md
  - MEMORY/self/long_term.md
  - MEMORY/self/archived.md
  - MEMORY/self/ongoing_context.md
  - MEMORY/self/actual_tasks.md
  - MEMORY/self/tasks.md

  # MEMORY (user)
  - MEMORY/user/personal_experiences.md
  - MEMORY/user/environments.md
  - MEMORY/user/tasks.md
  - MEMORY/user/long_term_chat.md
  - MEMORY/user/self_md/_readme.md

  # TOOLS, LLMS
  - TOOLS/tool_record.md
  - LLMS/providers.md

# Update mode per file. Enforced by lib/md_io.py.
update_modes:
  "PROTOCOL/main_index.md": patch
  "PROTOCOL/soul.md": patch
  "PROTOCOL/tiny/*.md": read_only
  "ARCHIVE/system_archive_file_record.md": append
  "ARCHIVE/codes/*.md": append_new_file
  "MEMORY/index.md": patch
  "MEMORY/self/short_term.md": append_with_decay
  "MEMORY/self/long_term.md": append
  "MEMORY/self/archived.md": append
  "MEMORY/self/ongoing_context.md": replace
  "MEMORY/self/actual_tasks.md": patch
  "MEMORY/self/tasks.md": append
  "MEMORY/user/personal_experiences.md": append
  "MEMORY/user/environments.md": patch
  "MEMORY/user/tasks.md": patch
  "MEMORY/user/long_term_chat.md": append
  "MEMORY/user/self_md/*.md": read_only
  "TOOLS/tool_record.md": patch
  "LLMS/providers.md": patch

# Nodes. Names match SCHEMA.excalidraw verbatim.
nodes:
  USER:                  {module: user_entry,        role: YOURS}
  SEND:                  {module: send,              role: YOURS}
  PROMPT_HANDLER:        {module: prompt_handler,    role: YOURS}
  FORMAT_IDENTIFIER:     {module: format_identifier, role: YOURS}
  DIVIDE_FORMATS:        {module: divide_formats,    role: YOURS}
  FILE_FORMAT_FINDER:    {module: format_finder,     role: YOURS, arg: file}
  AUDIO_FORMAT_FINDER:   {module: format_finder,     role: YOURS, arg: audio}
  VIDEO_FORMAT_FINDER:   {module: format_finder,     role: YOURS, arg: video}
  IMAGE_FORMAT_FINDER:   {module: format_finder,     role: YOURS, arg: image}
  TEXT_FORMAT_FINDER:    {module: format_finder,     role: YOURS, arg: text}
  USE_CODE:              {module: use_code,          role: GLUE,   invokes: oc_skill}
  SEND_STATUS_TO_LLM:    {module: send_status_llm,   role: GLUE,   invokes: oc_llm}
  CONVERT:               {module: convert,           role: YOURS}
  ADD_NEW_METHOD:        {module: add_new_method,    role: YOURS}
  ADD_AS_TASK:           {module: add_as_task,       role: YOURS,  invokes: oc_queue}
  ORDER_AND_UNIFY:       {module: order_unify,       role: YOURS}
  SEND_TO_QUEUE:         {module: send_to_queue,     role: YOURS}
  PROMPT_QUEUE:          {module: prompt_queue,      role: NATIVE, invokes: oc_queue}
  LLM_STATUS_CHECK:      {module: llm_status_check,  role: YOURS}
  MODEL:                 {module: model,             role: YOURS}
  CHECK_RULE:            {module: check_rule,        role: YOURS}
  SKIP_IF_PROTO_NOT_MET: {module: skip_if_proto,     role: YOURS}
  VERIFIER:              {module: verifier,          role: YOURS}
  SMALL_CONTEXT_PROTO:   {module: small_context,     role: YOURS}
  MAIN_FILE_NAVIGATE:    {module: main_file_nav,     role: YOURS}
  PROMPT_CORRECTOR:      {module: prompt_corrector,  role: YOURS}
  INJECTION_GUARD:       {module: injection_guard,   role: YOURS}
  QUESTION:              {module: question,          role: GLUE,   invokes: oc_approval}
  LLM:                   {module: llm_caller,        role: NATIVE, invokes: oc_llm}
  OUTPUT:                {module: output,            role: YOURS}
  PROMPT_SPLITTER:       {module: prompt_splitter,   role: YOURS}
  USER_OUTPUT:           {module: user_output,       role: YOURS,  invokes: oc_channels_out}
  COMMAND_OUTPUT:        {module: command_output,    role: YOURS,  invokes: oc_runtimes}
  RECEIVE:               {module: receive,           role: YOURS}
  SELF_OUTPUT:           {module: self_output,       role: YOURS}
  NEXT_STEP_SELECTOR:    {module: next_step_selector,role: YOURS}
  UPDATES_WHEN_CHANGED:  {module: updates_watcher,   role: YOURS}

# Flow edges (directed). Source of truth for wiring.
# Each entry is a string "FROM -> TO" with optional "; when=CONDITION".
flow:
  - "USER -> SEND"
  - "SEND -> PROMPT_HANDLER"
  - "PROMPT_HANDLER -> FORMAT_IDENTIFIER"
  - "FORMAT_IDENTIFIER -> ORDER_AND_UNIFY; when=if_text_only"
  - "FORMAT_IDENTIFIER -> DIVIDE_FORMATS; when=if_multi_format"
  - "DIVIDE_FORMATS -> FILE_FORMAT_FINDER"
  - "DIVIDE_FORMATS -> AUDIO_FORMAT_FINDER"
  - "DIVIDE_FORMATS -> VIDEO_FORMAT_FINDER"
  - "DIVIDE_FORMATS -> IMAGE_FORMAT_FINDER"
  - "DIVIDE_FORMATS -> TEXT_FORMAT_FINDER"
  - "*_FORMAT_FINDER -> USE_CODE; when=if_known"
  - "*_FORMAT_FINDER -> SEND_STATUS_TO_LLM; when=if_unknown"
  - "USE_CODE -> CONVERT"
  - "SEND_STATUS_TO_LLM -> ADD_NEW_METHOD; when=if_possible"
  - "SEND_STATUS_TO_LLM -> ADD_AS_TASK; when=if_not_possible"
  - "ADD_NEW_METHOD -> CONVERT"
  - "ADD_NEW_METHOD -> ADD_AS_TASK; when=if_failed_gt_3"
  - "CONVERT -> ORDER_AND_UNIFY"
  - "ORDER_AND_UNIFY -> SEND_TO_QUEUE"
  - "SEND_TO_QUEUE -> PROMPT_QUEUE"
  - "PROMPT_QUEUE -> LLM_STATUS_CHECK"
  - "LLM_STATUS_CHECK -> MODEL; when=if_working_or_idle"
  - "LLM_STATUS_CHECK -> PROMPT_QUEUE; when=if_waiting"
  - "MODEL -> CHECK_RULE"
  - "CHECK_RULE -> SKIP_IF_PROTO_NOT_MET; when=if_not_needed"
  - "CHECK_RULE -> VERIFIER; when=if_needed"
  - "SKIP_IF_PROTO_NOT_MET -> LLM"
  - "VERIFIER -> SMALL_CONTEXT_PROTO"
  - "SMALL_CONTEXT_PROTO -> MAIN_FILE_NAVIGATE"
  - "MAIN_FILE_NAVIGATE -> PROMPT_CORRECTOR"
  - "PROMPT_CORRECTOR -> QUESTION; when=if_correction_needed"
  - "PROMPT_CORRECTOR -> INJECTION_GUARD"
  - "VERIFIER -> INJECTION_GUARD"
  - "INJECTION_GUARD -> QUESTION; when=if_injection_risk"
  - "INJECTION_GUARD -> LLM"
  - "QUESTION -> USER; when=if_ask_user"
  - "QUESTION -> SELF_OUTPUT; when=if_ask_self"
  - "LLM -> OUTPUT"
  - "OUTPUT -> PROMPT_SPLITTER"
  - "PROMPT_SPLITTER -> USER_OUTPUT"
  - "PROMPT_SPLITTER -> COMMAND_OUTPUT"
  - "PROMPT_SPLITTER -> SELF_OUTPUT"
  - "COMMAND_OUTPUT -> RECEIVE"
  - "RECEIVE -> USER_OUTPUT; when=if_works"
  - "RECEIVE -> VERIFIER; when=if_fail"
  - "SELF_OUTPUT -> PROMPT_QUEUE"

# OpenClaw primitives this schema expects to be available.
# lib/openclaw_shim.py maps each to a real SDK call (agent does this).
openclaw_primitives:
  channels_inbound:  [chat_gui, telegram, whatsapp]
  channels_outbound: [chat_gui, telegram, whatsapp, windows_desktop,
                      cmd_powershell, dashboard_viewer]
  runtimes:          [ubuntu_24_04, windows_11, linux_terminal, chrome,
                      shell, comfyui, ollama, lmstudio, devices]
  skills:            tool_runner
  queue:             fifo
  secret_store:      kv
  approval_gate:     sync

# Precedence rules. Loaded at startup and enforced at runtime.
precedence:
  - schema_nodes_win_over_oc_defaults
  - read_first_before_any_md_write
  - never_rename_nodes
  - reuse_oc_primitives_do_not_reimplement
  - no_new_files_without_schema_change

# Disabled OpenClaw defaults (agent must turn these off).
oc_defaults_disabled:
  - planner
  - router
  - critic
  - memory_agent
  - retry_policy
  - heartbeat
  - auto_context_injection
  - system_prompt_wrapping
  - auto_tool_result_trust
