from guardrail_logger import log_guardrail_decision


print("DAY 15 - GUARDRAIL DECISION LOGGING")
print("=" * 60)


decision = log_guardrail_decision(
    control_triggered="instruction_hierarchy",
    outcome="BLOCKED",
    reason_code="PROMPT_INJECTION_DETECTED",
)


print("Guardrail decision recorded:")
print(decision)

print("\nSensitive request content:")
print("NOT LOGGED")

print("\nLog file:")
print("guardrail_decisions.jsonl")