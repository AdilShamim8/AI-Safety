# Threat-model template

Used by chapters 12–15, 19, 22 and projects P07, P08, P10. A threat model
that does not name an attacker-controlled input is a diagram, not a model.

```markdown
# Threat model: <system name>
Version + date · Author · System commit/config reviewed

## 1. System description
What the system does, its components, and the data flows between them.
One paragraph of prose plus an ASCII diagram.

## 2. Trust boundaries
Each boundary as a line in the diagram, with: what crosses it, who
controls what crosses it, and what enforces the boundary (mechanism, not
policy — "the system prompt says" is a policy).

## 3. Assets and consequences
What an attacker wants: data confidentiality/integrity, capability misuse,
resource theft, reputation/harm via outputs. Rank by consequence severity,
not by likelihood intuition.

## 4. Adversaries
Who plausibly attacks: outsider, insider, compromised upstream (data or
dependency), and the *system's own model* behaving undesirably without an
attacker (the failure class security people forget). Capability and
knowledge level per adversary (black/gray/white-box, adaptive or not).

## 5. Attack surfaces (attacker-controlled inputs)
Enumerate every input fully or partially under adversarial control. This
is the section that must be exhaustive; each surface maps to at least one
test in the evaluation plan.

## 6. Assumptions (explicit)
What you assume holds and cannot verify: component trustworthiness,
isolation, key management, evaluation-transfer assumptions. Each
assumption gets a failure condition: what observation would falsify it.

## 7. Risk register
| ID | Threat | Adversary | Surface | Consequence | Controls now | Gaps | Evidence needed |

## 8. Controls and residual risk
For each control: the mechanism, where it lives (model-internal prompt vs.
enforced boundary vs. monitoring), and its bypass conditions. Residual
risk stated plainly — what remains accepted, and who accepted it.

## 9. Mapping (where applicable)
Map demonstrated attacks to external frameworks by identifier and version
(e.g., OWASP GenAI LLM Top 10 entries, MITRE ATLAS techniques), recording
the framework version used. Unmapped findings stay unmapped rather than
being forced into wrong boxes.
```
