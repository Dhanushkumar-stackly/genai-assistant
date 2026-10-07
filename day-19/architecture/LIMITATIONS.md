# Known Limitations

## 1. Retrieval Dependency

Answer quality depends on the quality and coverage of
the indexed documents.

If the required information is not present in the
knowledge base, the system may be unable to provide
a grounded answer.

## 2. Model Dependency

Generated responses depend on the configured model,
prompt, context quality, and model behavior.

## 3. Voice Recognition

STT accuracy may vary depending on:

- Audio quality
- Background noise
- Accent
- Pronunciation
- Recording quality

## 4. TTS

TTS availability depends on the configured provider.

A text fallback may be required when TTS is unavailable.

## 5. Evaluation

Evaluation scores depend on:

- Dataset
- Model
- Prompt
- Retrieval configuration
- Evaluation criteria

Scores from different configurations should not be
compared without recording the configuration.

## 6. Latency

End-to-end latency depends on:

- STT
- Retrieval
- Model generation
- TTS
- Network
- Infrastructure

## 7. External Dependencies

The system may depend on external model or service
providers.

Provider outages may affect availability.

## 8. Security

The system must not be treated as a replacement for
human authorization or enterprise security controls.

## 9. Data Privacy

Sensitive information must not be entered unless the
deployment has been explicitly configured and approved
to process that information.

## 10. Unsupported Use Cases

The system is not intended to:

- Make autonomous legal decisions
- Make autonomous medical decisions
- Make autonomous financial decisions
- Reveal unauthorized private information
- Bypass access controls
- Guarantee factual correctness
- Replace human approval for high-impact decisions