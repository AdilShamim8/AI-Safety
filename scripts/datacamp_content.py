"""DataCamp companion content — Chapter 1 (AI's Security Landscape).

Shared content for scripts/gen_datacamp_companion.py. One entry per
lesson of the course's chapter 1 (11 lessons: 4 videos, 5 interactive
exercises, 2 gamified scenarios), as verified on the public catalog
page 2026-11-03 and supplied with the owner's course synopsis the
same day. Video beats follow the owner-supplied synopsis; exercise
entries prepare the concepts the exercise tests (the interactive
content itself is account-walled and never reproduced).

Each lesson dict:
  slug, n, title, xp, kind ("video" | "exercise" | "gamified"),
  situation (where the lesson sits), beats [(heading, body)],
  throughlines [(chapter relpath, label, why)], angle.
"""

CH1 = {
    "number": 1,
    "title": "AI's Security Landscape",
    "purpose": (
        "Establish a strategic understanding of AI security, identify the "
        "unique security risks associated with AI, examine how AI can be a "
        "security change agent, and treat all players equally."
    ),
    "lessons": [
        {
            "slug": "ch01-01-security-risks-specific-to-ai",
            "n": 1,
            "title": "Security risks specific to AI",
            "xp": 50,
            "kind": "video",
            "situation": (
                "The course's opening video. It sets the contract for the "
                "whole course: AI offers significant potential, but only "
                "effective risk management lets you harness the benefits "
                "safely — and adopting AI means rethinking security, because "
                "traditional security strategies are not sufficient when AI "
                "is in the loop."
            ),
            "beats": [
                (
                    "A coin: benefits on one side, security risks on the other",
                    "The course's framing device: integrating AI is a coin "
                    "whose two sides are its benefits and its security risks. "
                    "The point of the metaphor is that you cannot accept one "
                    "side without the other — every AI adoption decision is "
                    "simultaneously a security decision. This repository "
                    "states the same thing operationally in its risk-model "
                    "chapter: a hazard without an exposure and a pathway is "
                    "not yet a risk, and an adopted system always creates "
                    "exposure.",
                ),
                (
                    "The five risks that are specific to AI",
                    "The video names the five: bias, hallucination, data "
                    "poisoning, adversarial attacks, and sensitive data "
                    "exposure. What makes them AI-specific is that they all "
                    "arise from the system learning from data — none of them "
                    "is a traditional software bug you can patch. The course "
                    "then works two of them as full examples: an AI hiring "
                    "system trained on historical company data that reflects "
                    "past bias learns and magnifies that bias (harm to "
                    "candidates and to the company — trust declines), and "
                    "attackers running a shopping platform's recommender "
                    "through fake user profiles and interactions — data "
                    "poisoning — misleading it into recommending unpopular "
                    "or harmful products to genuine users (customer "
                    "deception, reputational damage, lost trust).",
                ),
                (
                    "Speed is what makes AI bias different from human bias",
                    "A key difference the video draws: AI makes "
                    "lightning-fast decisions, often amplifying the impact "
                    "before anyone can notice. Bias at machine speed "
                    "unfairly favors or harms groups and creates uneven "
                    "outcomes at an alarming rate — the same reason this "
                    "repository treats propensity (a rate with a "
                    "denominator) as its own risk-model quantity.",
                ),
                (
                    "Hallucination, poisoning, adversarial input, data exposure",
                    "The remaining definitions, compressed: hallucination is "
                    "the AI generating incorrect or misleading information "
                    "and presenting it as truth (flawed decisions, "
                    "misinformation spread, lost trust); data poisoning is "
                    "someone intentionally tampering with training data so "
                    "the system veers off course — weeds planted in a "
                    "well-tended garden; adversarial attacks present "
                    "misleading inputs during operation (not training) and "
                    "are hard to detect, compromising the system's "
                    "integrity; sensitive data exposure is a poorly secured "
                    "AI system disclosing sensitive or protected information "
                    "it relies on for training and operation.",
                ),
                (
                    "Understanding is the first step; proactivity is the posture",
                    "The video closes its argument: recognizing these risks "
                    "is the first crucial step toward managing them, and it "
                    "is what lets you avoid the damages — financial losses, "
                    "reputational damage, wrong AI-powered decisions, "
                    "regulatory penalties. Because the AI risk landscape "
                    "constantly changes, proactive risk management is "
                    "essential: knowledge of the AI security ecosystem, "
                    "foresight to future-proof the approach, and the wisdom "
                    "to build a security-aware culture — the three things "
                    "the rest of the course teaches.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/01-risk-models-and-research-epistemics/README.md",
                    "Ch. 01",
                    "the repo's own risk vocabulary (hazard, exposure, "
                    "pathway, propensity) is the disciplined version of this "
                    "video's five-risk list.",
                ),
                (
                    "../../chapters/12-adversarial-ml-and-robustness/README.md",
                    "Ch. 12",
                    "adversarial input attacks at full technical depth.",
                ),
                (
                    "../../chapters/16-privacy-provenance-and-supply-chains/README.md",
                    "Ch. 16",
                    "sensitive data exposure, provenance, and the "
                    "data-protection practices that reduce it.",
                ),
                (
                    "../../chapters/21-sociotechnical-and-systemic-risk/README.md",
                    "Ch. 21",
                    "bias and trust as sociotechnical, not merely technical, "
                    "failures.",
                ),
            ],
            "angle": (
                "The only lesson in the library that introduces the five "
                "AI-specific risks through two worked business stories — a "
                "hiring system and a shopping platform — before any "
                "technical machinery: the complete beginner on-ramp this "
                "repository lacked."
            ),
        },
        {
            "slug": "ch01-02-ai-risk-awareness",
            "n": 2,
            "title": "AI risk awareness",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The first interactive exercise. It drills the five "
                "AI-specific risks the opening video introduced, testing "
                "whether the learner can tell them apart by their mechanism "
                "rather than by their outcome."
            ),
            "beats": [
                (
                    "The discriminating feature is the phase, not the harm",
                    "All five risks end in some kind of harm, so outcome "
                    "language ('it gave a wrong answer') cannot tell them "
                    "apart. The discriminating feature is where in the "
                    "pipeline the fault enters: poisoned or biased training "
                    "data (data poisoning, bias) faults the learning; "
                    "misleading inputs at run time (adversarial attacks) "
                    "fault the decisions; a confident fabrication with no "
                    "input trigger (hallucination) faults the generation; "
                    "and a disclosure of protected information (sensitive "
                    "data exposure) faults the handling of the data itself.",
                ),
                (
                    "The confusions the exercise is designed to catch",
                    "The two confusions the exercise probes: data poisoning "
                    "versus adversarial attacks (training-time versus "
                    "inference-time manipulation — the repo's chapters 12 "
                    "and 16 draw the same line), and bias versus "
                    "hallucination (systematic skew across groups versus "
                    "confident fabrication on individual outputs). A third, "
                    "subtler one: hallucination versus a wrong-but-honest "
                    "prediction, which turns on whether the system presents "
                    "the output as truth.",
                ),
                (
                    "How to prepare in five minutes",
                    "Re-state each risk in one sentence naming the phase: "
                    "'bias — the training data skews the learned behavior "
                    "across groups'; 'poisoning — an attacker corrupts the "
                    "training data'; 'adversarial — an attacker crafts "
                    "run-time inputs'; 'hallucination — the model fabricates "
                    "and asserts'; 'data exposure — the system leaks "
                    "protected information'. If your sentence cannot name "
                    "the phase, the exercise will find you.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/01-risk-models-and-research-epistemics/README.md",
                    "Ch. 01",
                    "the threat-hypothesis form forces the same "
                    "mechanism-first discipline.",
                ),
                (
                    "../../chapters/12-adversarial-ml-and-robustness/README.md",
                    "Ch. 12",
                    "the poisoning-versus-adversarial boundary at full depth.",
                ),
            ],
            "angle": (
                "Turns the video's definitions into a discrimination skill — "
                "the active-recall step this repository's flashcard method "
                "assumes but this course actually grades."
            ),
        },
        {
            "slug": "ch01-03-dinner-at-riskland-junction",
            "n": 3,
            "title": "Dinner at Riskland Junction",
            "xp": 100,
            "kind": "gamified",
            "situation": (
                "A gamified scenario exercise: the learner classifies risk "
                "examples into the five families while a story unfolds — "
                "the course's signature move of grading judgment, not "
                "recall."
            ),
            "beats": [
                (
                    "Scenario classification is a two-step procedure",
                    "For each story beat the exercise serves, the reliable "
                    "procedure is: first name the phase the fault entered "
                    "through (training data, run-time input, generation, "
                    "data handling), then match the phase to the family. "
                    "Stories are written to tempt you toward the harm word "
                    "('customers were deceived') instead of the mechanism "
                    "word — the same trap as classifying a risk by its "
                    "consequence instead of its causal pathway, which the "
                    "repo's risk-model chapter treats as the primary "
                    "classification error.",
                ),
                (
                    "Why the game grades judgment",
                    "Every wrong classification in this game would, in a "
                    "real organization, buy the wrong defense: calling "
                    "poisoning 'bias' sends you scrubbing labels instead of "
                    "auditing the data supply chain; calling an adversarial "
                    "attack 'hallucination' sends you retraining instead of "
                    "hardening inputs. The game makes that cost felt — the "
                    "repo's phrase for the same lesson is 'each family "
                    "implies different interventions, and misclassifying a "
                    "risk buys the wrong defense'.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/01-risk-models-and-research-epistemics/README.md",
                    "Ch. 01",
                    "the risk taxonomy with the full classification "
                    "discipline.",
                ),
                (
                    "../../chapters/20-misuse-dangerous-capabilities-release-evaluation/README.md",
                    "Ch. 20",
                    "misuse framing when the adversary is the point.",
                ),
            ],
            "angle": (
                "The only graded scenario trainer for risk classification in "
                "the library — judgment practice the video courses cannot "
                "give."
            ),
        },
        {
            "slug": "ch01-04-ai-as-a-change-agent-for-security",
            "n": 4,
            "title": "AI as a change agent for security",
            "xp": 50,
            "kind": "video",
            "situation": (
                "The chapter's second video: the flip of the coin. Having "
                "covered the risks AI brings, it covers AI as a tool FOR "
                "security — the four application families in security "
                "operations, and the new risks that come with them."
            ),
            "beats": [
                (
                    "Automated anomaly detection",
                    "AI sifting through network activity, user behavior, and "
                    "system logs to surface irregular patterns that could "
                    "be warning signs of malware, unauthorized access, or "
                    "fraud. The video's named example is UEBA — user and "
                    "entity behavior analytics: tools that study patterns of "
                    "user behavior to spot irregularities, pinpointing "
                    "compromised accounts or flagging insiders who pose "
                    "security risks.",
                ),
                (
                    "Threat intelligence platforms (TIPs)",
                    "AI-powered TIPs analyze threat intelligence data to "
                    "recognize the who, why, how, and what-next of potential "
                    "threats — attackers' motivations, tactics, and "
                    "techniques — so organizations can prepare and stay one "
                    "step ahead of relevant risks.",
                ),
                (
                    "SOAR — orchestration, automation, and response",
                    "SOAR tools use AI to streamline and synchronize security "
                    "tasks across systems: security log analysis, threat "
                    "containment, security patch management. The point of "
                    "the orchestration is that human experts redirect their "
                    "focus onto the sophisticated threats machines cannot "
                    "triage.",
                ),
                (
                    "SIEM with AI inside",
                    "Security information and event management systems "
                    "analyze real-time security event data to identify "
                    "anomalies, find patterns, and flag potential incidents. "
                    "Adding AI (machine learning, advanced data correlation) "
                    "identifies complex threats more efficiently than "
                    "traditional methods — faster incident detection, "
                    "improved threat prediction, actionable insights. The "
                    "worked example: a bank's SIEM detects unusual patterns "
                    "in international wire transfers (sudden transfers to "
                    "rarely used accounts in high-risk countries at unusual "
                    "times); AI trained on past fraud attempts analyzes the "
                    "transfer details in real time and flags potentially "
                    "fraudulent activity faster and more accurately than "
                    "manual review, so the bank investigates immediately "
                    "and minimizes losses.",
                ),
                (
                    "The new risks on the flip side",
                    "The video is careful: the same tools raise ethical and "
                    "accountability questions. Accountability for AI in "
                    "security is hard — when it is difficult to understand "
                    "how a system makes decisions, it is hard to know who is "
                    "responsible for them. And the ethics can cut against "
                    "the tool: facial recognition in surveillance can "
                    "produce unfair results for specific groups and raise "
                    "privacy concerns, so benefits must be weighed against "
                    "drawbacks. Conclusion: AI in security must be adopted "
                    "carefully — know and mitigate the related risks before "
                    "introducing it.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/12-adversarial-ml-and-robustness/README.md",
                    "Ch. 12",
                    "the robustness side of detection under adversarial "
                    "pressure.",
                ),
                (
                    "../../chapters/08-ai-control-and-monitoring/README.md",
                    "Ch. 08",
                    "control and monitoring — the repo's treatment of "
                    "AI-assisted monitoring pipelines.",
                ),
                (
                    "../../chapters/14-agent-tool-memory-mcp-security/README.md",
                    "Ch. 14",
                    "what happens when the AI doing the monitoring is itself "
                    "an agent with tools.",
                ),
                (
                    "../../chapters/19-multimodal-and-embodied-safety/README.md",
                    "Ch. 19",
                    "the facial-recognition fairness and privacy concerns at "
                    "full depth.",
                ),
            ],
            "angle": (
                "The only lesson in the library that names the four "
                "security-operations tool families (anomaly detection/UEBA, "
                "TIPs, SOAR, SIEM) and prices their accountability problem — "
                "a working surface this repository had no entry for until "
                "this companion."
            ),
        },
        {
            "slug": "ch01-05-enhancing-security-operations-with-ai",
            "n": 5,
            "title": "Enhancing security operations with AI",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The drill for the change-agent video: given a security-ops "
                "need, pick the right tool family — the exercise tests "
                "function-matching, not vendor knowledge."
            ),
            "beats": [
                (
                    "Match by function, not by brand",
                    "The reliable mapping: continuous streams of behavioral "
                    "and log data needing irregular-pattern detection → "
                    "anomaly detection / UEBA; intelligence about attackers "
                    "(motivations, tactics, techniques, what-next) needing "
                    "aggregation and analysis → TIPs; repetitive "
                    "cross-system tasks needing orchestration so experts "
                    "focus on sophisticated threats → SOAR; real-time event "
                    "correlation across systems to flag incidents → SIEM, "
                    "with AI adding detection speed and prediction.",
                ),
                (
                    "The trap: overlapping vocabulary",
                    "All four families say 'analyze' and 'alert', so the "
                    "exercise discriminates on the object of the analysis: "
                    "behavior (UEBA), adversary intelligence (TIP), "
                    "workflows (SOAR), events (SIEM). If a stem describes "
                    "what is analyzed rather than which product category "
                    "it belongs to, you have your answer.",
                ),
                (
                    "Why the bank example generalizes",
                    "The wire-transfer case in the video is the pattern to "
                    "re-use: a real-time event stream, a learned model of "
                    "past attempts, and a human investigation triggered "
                    "the moment the model flags. Every correct answer in "
                    "this exercise is some rotation of that pattern with "
                    "the object swapped.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/08-ai-control-and-monitoring/README.md",
                    "Ch. 08",
                    "monitoring design under adversary pressure.",
                ),
                (
                    "../../chapters/12-adversarial-ml-and-robustness/README.md",
                    "Ch. 12",
                    "what adversarial robustness means for detectors.",
                ),
            ],
            "angle": (
                "Grades the function-matching judgment the video could only "
                "assert — the four tool families as a decision, not a "
                "list."
            ),
        },
        {
            "slug": "ch01-06-risks-of-ai-in-security",
            "n": 6,
            "title": "Risks of AI in security",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The second drill for the change-agent material: the risks "
                "of using AI in security — accountability and the ethical "
                "dilemmas — tested as discriminations."
            ),
            "beats": [
                (
                    "Accountability is hard when the reasoning is opaque",
                    "The video's claim to master for this exercise: because "
                    "it is difficult to understand how some systems make "
                    "decisions, it is hard to know who is responsible for "
                    "them. The exercise probes this with ownership "
                    "questions — vendor or deployer? operator or auditor? — "
                    "and the honest answer pattern is: whoever could "
                    "foresee and mitigate, which requires the decision "
                    "path to be inspectable. The repo's translation: no "
                    "monitorability, no accountability (its control and "
                    "reasoning-faithfulness chapters).",
                ),
                (
                    "The ethical dilemmas as a weighing, not a verdict",
                    "Facial recognition in surveillance producing unfair "
                    "results for specific groups and raising privacy "
                    "concerns is the video's example. The exercise tests "
                    "whether you can state BOTH sides of the weighing — "
                    "the security benefit and the fairness/privacy cost — "
                    "before concluding. Answers that carry only one side "
                    "are the ones marked wrong.",
                ),
                (
                    "The adoption rule",
                    "The closing principle the exercise wants applied to "
                    "every stem: AI must be adopted carefully — know and "
                    "mitigate the related risks BEFORE introducing AI into "
                    "security operations. In exercise terms: any answer "
                    "that deploys first and assesses later is wrong, which "
                    "is the EU AI Act's own logic two chapters later.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/19-multimodal-and-embodied-safety/README.md",
                    "Ch. 19",
                    "facial-recognition fairness at full depth.",
                ),
                (
                    "../../chapters/18-reasoning-faithfulness-and-monitorability/README.md",
                    "Ch. 18",
                    "why monitorability is the precondition for "
                    "accountability.",
                ),
                (
                    "../../chapters/23-governance-and-standards/README.md",
                    "Ch. 23",
                    "who answers when the reasoning is opaque.",
                ),
            ],
            "angle": (
                "Turns 'adopt carefully' from a slogan into graded "
                "weighings — the accountability drill this repository "
                "preaches but never quizzes."
            ),
        },
        {
            "slug": "ch01-07-security-catalyst-station",
            "n": 7,
            "title": "Security Catalyst Station",
            "xp": 100,
            "kind": "gamified",
            "situation": (
                "The chapter's closing scenario game: choose the right AI "
                "security application for a series of situations — the "
                "chapter-one judgment exam."
            ),
            "beats": [
                (
                    "The four-step decision the game embeds",
                    "For each situation: (1) what is the object — behavior, "
                    "adversary intelligence, workflows, or events? (2) what "
                    "is the latency requirement — real-time flags or "
                    "analyzed hindsight? (3) what must remain explainable "
                    "to humans, since accountability follows the "
                    "inspectable path? (4) does the benefit survive the "
                    "weighing against fairness and privacy costs? A choice "
                    "that survives all four is a defensible answer.",
                ),
                (
                    "The cost of a wrong catalyst",
                    "The game's stakes are the operational ones: picking "
                    "SOAR where SIEM was needed automates a process around "
                    "undetected events; picking anomaly detection where "
                    "threat intelligence was needed studies your own users "
                    "while the adversary walks past. The repo's phrase for "
                    "the underlying error: solving the problem one "
                    "instrument down the chain from where it lives.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/08-ai-control-and-monitoring/README.md",
                    "Ch. 08",
                    "choosing monitors under adversarial pressure.",
                ),
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "the assurance discipline behind every 'is it working'.",
                ),
            ],
            "angle": (
                "A graded judgment exam for security-operations choices — "
                "the kind of practice no video course can score."
            ),
        },
        {
            "slug": "ch01-08-the-ai-security-ecosystem",
            "n": 8,
            "title": "The AI security ecosystem",
            "xp": 50,
            "kind": "video",
            "situation": (
                "The chapter's second half opens: managing AI security means "
                "managing its ECOSYSTEM — the network of people, legal "
                "requirements, technologies, and processes whose elements "
                "must work together."
            ),
            "beats": [
                (
                    "Stakeholders: internal and external",
                    "Internal: IT professionals (technical operation of AI "
                    "systems), legal and compliance teams (understanding "
                    "and applying laws and regulations), data scientists "
                    "(creating and maintaining the robustness of "
                    "algorithms), and executives (strategic decisions "
                    "affecting the whole organization's approach). "
                    "External: customers (who trust the company with their "
                    "data), partners (who share interconnected systems), "
                    "and regulatory bodies (who enforce legal and "
                    "compliance standards). Each stakeholder has different "
                    "concerns which must be recognized and balanced.",
                ),
                (
                    "Why diverse perspectives cannot be overstated",
                    "The video's worked contrast: a data scientist focuses "
                    "on the precision of the model; a legal professional "
                    "worries about the implications of the model's "
                    "decisions for user privacy; an executive weighs return "
                    "on investment and reputational impact. These "
                    "perspectives must be acknowledged and reconciled — "
                    "that reconciliation is what produces balanced and "
                    "comprehensive security decisions. A thorough "
                    "stakeholder analysis maps who the stakeholders are, "
                    "their interests and concerns, and how AI security "
                    "decisions impact them; surveys, interviews, and "
                    "workshops provide the input and foster trust.",
                ),
                (
                    "Legal and compliance: ahead of the box-ticking",
                    "Regulators are scrambling to catch up with AI's "
                    "advances, so the regulatory landscape is unpredictable "
                    "— meeting current requirements is insufficient. New "
                    "regulation will be shaped by known risks AND public "
                    "opinion; proactively monitoring both, and committing "
                    "to best practices, helps companies anticipate new "
                    "rules. The emerging trend the video names: ethical use "
                    "of AI inside legal and compliance frameworks — "
                    "consumers and regulators increasingly expect "
                    "fairness, accountability, and transparency, and "
                    "building for them protects against fines and "
                    "reputational damage.",
                ),
                (
                    "Technology and processes: the other two pillars",
                    "The technology pillar is the security features within "
                    "AI systems, the infrastructure they run on, and the "
                    "networks they interact with — resilient against "
                    "hacking, data breaches, unauthorized access, yet "
                    "agile enough to adapt to emerging challenges. The "
                    "processes pillar is regular security assessments, "
                    "incident response planning, and continuous monitoring "
                    "— what keeps security practices consistent and "
                    "effective over time. The closing statement: effective "
                    "security is not only technology; it is people, laws, "
                    "ethics, and procedures working together.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/21-sociotechnical-and-systemic-risk/README.md",
                    "Ch. 21",
                    "the systemic layer: stakeholders and dynamics, "
                    "formally.",
                ),
                (
                    "../../chapters/23-governance-and-standards/README.md",
                    "Ch. 23",
                    "the governance instruments the legal pillar names.",
                ),
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "the process pillar as an engineering discipline.",
                ),
            ],
            "angle": (
                "The only lesson in the library that teaches the four-pillar "
                "ecosystem (people, legal, technology, processes) with the "
                "stakeholder reconciliation method — the layer the "
                "technical courses assume and never state."
            ),
        },
        {
            "slug": "ch01-09-the-importance-of-multiple-viewpoints",
            "n": 9,
            "title": "The importance of multiple viewpoints",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The drill for the ecosystem video's stakeholder half: "
                "recognizing which perspective is speaking and why the "
                "reconciliation matters."
            ),
            "beats": [
                (
                    "Identify the speaker before evaluating the claim",
                    "The exercise presents statements like 'the model is "
                    "precise enough' (data scientist), 'the decisions "
                    "implicate user privacy' (legal), 'what is the ROI and "
                    "the reputational exposure?' (executive). The skill "
                    "being graded: attribute the viewpoint FIRST, because "
                    "an unattributed claim cannot be reconciled with the "
                    "others — it just competes with them.",
                ),
                (
                    "Reconciliation is the deliverable",
                    "The video's standard, applied here: perspectives must "
                    "be acknowledged AND reconciled into balanced, "
                    "comprehensive security decisions. Exercise answers "
                    "that pick a winner between stakeholders are wrong by "
                    "construction; the correct pattern preserves each "
                    "legitimate concern in the decision record — the same "
                    "move as the repo recording disagreement instead of "
                    "averaging it away.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/21-sociotechnical-and-systemic-risk/README.md",
                    "Ch. 21",
                    "stakeholder dynamics as a formal subject.",
                ),
                (
                    "../../chapters/01-risk-models-and-research-epistemics/README.md",
                    "Ch. 01",
                    "recording disagreement, not laundering it.",
                ),
            ],
            "angle": (
                "Grades perspective attribution — a social skill no video "
                "course can score and no technical course even attempts."
            ),
        },
        {
            "slug": "ch01-10-balancing-stakeholder-interests",
            "n": 10,
            "title": "Balancing stakeholder interests",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The harder stakeholder drill: given two interests in "
                "tension, produce the balance — the exercise tests whether "
                "you can hold both concerns in one decision."
            ),
            "beats": [
                (
                    "Tension pairs the exercise uses",
                    "The recurring pairs from the video: precision versus "
                    "privacy (data scientist versus legal), speed versus "
                    "trustworthiness (executive growth agenda versus "
                    "customer trust), innovation versus compliance cost "
                    "(startup posture versus regulatory posture). Each "
                    "pair maps to the stakeholder analysis method: whose "
                    "interest, what concern, what impact on them — then "
                    "the balanced decision.",
                ),
                (
                    "The output format that scores",
                    "A balancing answer states both interests, the "
                    "trade-off accepted, and the mitigation for the "
                    "interest that lost ground ('we adopt the tool, and we "
                    "add the audit that answers the legal concern'). "
                    "Single-interest answers read as advocacy, not "
                    "analysis — the exact failure mode the repo's "
                    "governance chapter calls governance theater.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/23-governance-and-standards/README.md",
                    "Ch. 23",
                    "instruments that institutionalize the balancing.",
                ),
                (
                    "../../chapters/21-sociotechnical-and-systemic-risk/README.md",
                    "Ch. 21",
                    "why the balancing is systemic, not personal.",
                ),
            ],
            "angle": (
                "Practices the balance-as-deliverable pattern — the "
                "governance skill the frameworks courses teach only at "
                "the document level."
            ),
        },
        {
            "slug": "ch01-11-ecosystem-nexus",
            "n": 11,
            "title": "Ecosystem Nexus",
            "xp": 100,
            "kind": "gamified",
            "situation": (
                "The chapter's final scenario game: decisions made at the "
                "ecosystem level, where every choice touches several "
                "pillars at once — the chapter-one capstone."
            ),
            "beats": [
                (
                    "Run the four-pillar checklist on every scenario",
                    "For each decision the game presents: people (which "
                    "stakeholders' concerns are engaged?), legal (which "
                    "regulatory or ethical expectations?), technology "
                    "(which security features, infrastructure, networks?), "
                    "processes (which assessments, response plans, "
                    "monitoring?). A decision that touches only one pillar "
                    "and ignores the others it implicates is the wrong "
                    "answer in this game.",
                ),
                (
                    "The nexus lesson",
                    "The game's title is its thesis: at the nexus, "
                    "decisions are not technical or legal or social — they "
                    "are all three, and the effective ones are made by "
                    "teams that can hear all three registers. That is the "
                    "course's strategic claim, and the repository's "
                    "sociotechnical chapter is its formal treatment.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/21-sociotechnical-and-systemic-risk/README.md",
                    "Ch. 21",
                    "the formal sociotechnical treatment.",
                ),
                (
                    "../../chapters/23-governance-and-standards/README.md",
                    "Ch. 23",
                    "governance as the institutional memory of the nexus.",
                ),
            ],
            "angle": (
                "The chapter-one capstone as a graded game — ecosystem "
                "judgment under time pressure, which no lecture can score."
            ),
        },
    ],
}
