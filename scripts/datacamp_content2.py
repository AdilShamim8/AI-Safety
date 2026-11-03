"""DataCamp companion content — Chapter 2 (Risk Management Fundamentals).

Shared content for scripts/gen_datacamp_companion.py. One entry per
lesson of the course's chapter 2 (16 lessons: 5 videos, 8 interactive
exercises, 3 gamified scenarios). See datacamp_content.py for the
field contract and the honesty basis (owner-supplied synopsis +
public catalog page, both 2026-11-03; interactive content never
reproduced).
"""

CH2 = {
    "number": 2,
    "title": "Risk Management Fundamentals",
    "purpose": (
        "The operational side: risks broken down by internal and external "
        "categories, secure development practices, and risk assessment — "
        "including the EU AI Act's risk-tier logic."
    ),
    "lessons": [
        {
            "slug": "ch02-01-model-risks",
            "n": 1,
            "title": "Model risks",
            "xp": 50,
            "kind": "video",
            "situation": (
                "Chapter 2 opens on the model lifecycle: watching risks "
                "during development reduces the harm of deploying a flawed "
                "system, but risks must ALSO be monitored after deployment "
                "— models drift over time as the real world and the data "
                "change, producing biased or inaccurate outputs if not "
                "monitored and addressed."
            ),
            "beats": [
                (
                    "The seven common model risks",
                    "The video's list: lack of model transparency and "
                    "interpretability, bias, hallucination, model drift, "
                    "overfitting, underfitting, and data leakage. The first "
                    "two are about the ability to understand the model: a "
                    "non-transparent model's inner workings are not "
                    "accessible and clear to those who use it; "
                    "non-interpretable means people cannot understand WHY "
                    "the model produces certain outputs from specific "
                    "inputs. Both matter most in sensitive areas like "
                    "healthcare or finance, where understanding the "
                    "decision process is as important as the decision.",
                ),
                (
                    "Bias and hallucination, where they enter",
                    "Bias: unfair preferences or prejudices arising at "
                    "various stages — biased training data, algorithm "
                    "choice and configuration, unrepresentative or flawed "
                    "data, human assumptions during development. "
                    "Hallucination: errors from insufficient training data, "
                    "incorrect assumptions made by the model, and biases "
                    "in the data. The repo's split for the same ground: "
                    "bias is systematic across groups; hallucination is "
                    "confident fabrication on outputs.",
                ),
                (
                    "Drift: the model gets confused by the present",
                    "Model drift is previously accurate models losing "
                    "relevance and accuracy because the data they see now "
                    "does not follow the patterns they learned — the "
                    "video's example is spam filters becoming less accurate "
                    "as new deceptive tactics arrive. The repo's chapter on "
                    "distribution shift is the formal treatment, and its "
                    "glossary row is the discriminating version of this "
                    "beat.",
                ),
                (
                    "Overfitting, underfitting, and data leakage",
                    "The learning-quality triple: overfitting is learning "
                    "the details and noise of the training data so much "
                    "that future performance suffers; underfitting is a "
                    "model too simple to learn the underlying patterns; "
                    "leakage is outside data mistakenly included in the "
                    "training set. Each damages the model's ability to make "
                    "accurate predictions — and leakage is the quiet one, "
                    "because it inflates validation scores before it ever "
                    "shows up in production.",
                ),
                (
                    "XAI as the management technique",
                    "The video's closing tool: Explainable AI (XAI), a set "
                    "of methods that make models more understandable and "
                    "transparent to humans by providing clear explanations "
                    "of the reasoning behind outputs. It builds trust and "
                    "aids identifying and correcting errors or biases "
                    "within the model. Controlled across the lifecycle, "
                    "these risks decide whether AI applications succeed; "
                    "the repo's interpretability arc is the deep version.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/02-evaluation-science-and-experimental-design/README.md",
                    "Ch. 02",
                    "leakage and overfitting as evaluation-science "
                    "subjects (grouped splits, contamination).",
                ),
                (
                    "../../chapters/17-distribution-shift-and-deployment-reliability/README.md",
                    "Ch. 17",
                    "drift and continuous monitoring at full depth.",
                ),
                (
                    "../../chapters/09-mechanistic-interpretability-foundations/README.md",
                    "Ch. 09",
                    "transparency and interpretability as research "
                    "programs.",
                ),
                (
                    "../../chapters/06-honesty-uncertainty-and-selective-prediction/README.md",
                    "Ch. 06",
                    "hallucination as a measured behavioral quantity.",
                ),
            ],
            "angle": (
                "The only lesson in the library that teaches the seven "
                "model risks as one lifecycle picture — underfitting and "
                "data leakage had no working definition anywhere in this "
                "repository before this companion."
            ),
        },
        {
            "slug": "ch02-02-common-risks-of-ai-models",
            "n": 2,
            "title": "Common risks of AI models",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The drill for the seven model risks: discriminate them by "
                "symptom, since several present with the same complaint — "
                "'the model performs badly'."
            ),
            "beats": [
                (
                    "Symptom-to-risk mapping",
                    "The discriminations the exercise probes: great on "
                    "training data, poor in the world → overfitting; poor "
                    "everywhere, missing the pattern → underfitting; "
                    "validation too good to be true, then production "
                    "disappoints → leakage; accurate last quarter, "
                    "degrading now → drift; right on average, skewed "
                    "across groups → bias; confident falsehoods on "
                    "specific prompts → hallucination; predictions fine "
                    "but no one can say why → transparency/interpretability "
                    "gap.",
                ),
                (
                    "The overfit-versus-underfit boundary",
                    "The cleanest discriminator is WHERE the error lives: "
                    "overfitting's error concentrates on unseen data, "
                    "underfitting's on all data including the training set. "
                    "An exercise stem that reports training-set performance "
                    "versus held-out performance is handing you the "
                    "answer.",
                ),
                (
                    "Leakage's tell",
                    "Leakage almost always presents as an evaluation "
                    "surprise, not a behavior surprise: metrics that "
                    "cannot be reproduced by an independent evaluator. The "
                    "repo's evaluation-science chapter builds its grouped "
                    "splits and contamination checks on exactly this "
                    "observation.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/02-evaluation-science-and-experimental-design/README.md",
                    "Ch. 02",
                    "the evaluation discipline that catches leakage and "
                    "overfitting.",
                ),
                (
                    "../../chapters/17-distribution-shift-and-deployment-reliability/README.md",
                    "Ch. 17",
                    "drift detection as deployment engineering.",
                ),
            ],
            "angle": (
                "Grades symptom diagnosis — the triage skill that turns the "
                "seven-item list into usable clinical judgment."
            ),
        },
        {
            "slug": "ch02-03-continuous-monitoring",
            "n": 3,
            "title": "Continuous monitoring",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The drill for the lifecycle half of the model-risks video: "
                "what to monitor after deployment, and why the watching "
                "never stops."
            ),
            "beats": [
                (
                    "The monitorables and their signals",
                    "Post-deployment, the watch-list is: drift (the "
                    "spam-filter pattern — accuracy decaying as the world "
                    "moves), bias emergence (unfair outputs appearing as "
                    "populations or usage patterns shift), and "
                    "hallucination rates on live traffic. Each needs a "
                    "baseline from deployment time, or the degradation "
                    "cannot be measured — the repo's rule: a number "
                    "without a pre-deployment referent has no meaning.",
                ),
                (
                    "Monitoring is an early-warning system",
                    "The video's framing from the assessmentFrameworks "
                    "lesson applies here: ongoing checks catch emerging "
                    "risks and unexpected model behavior before they "
                    "escalate — regular bias testing to identify unfair "
                    "outputs, performance monitoring to catch degradation. "
                    "In exercise terms: any answer that treats monitoring "
                    "as a one-time check is wrong; the correct pattern is "
                    "cadence plus thresholds plus a named owner.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/17-distribution-shift-and-deployment-reliability/README.md",
                    "Ch. 17",
                    "the monitoring chapter — dashboards, alerts, "
                    "subgroup reliability.",
                ),
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "monitoring as an assurance obligation.",
                ),
            ],
            "angle": (
                "Drills the post-deployment watch — the habit the video "
                "courses never operationalize because they end when the "
                "model ships."
            ),
        },
        {
            "slug": "ch02-04-model-risk-abyss",
            "n": 4,
            "title": "Model Risk Abyss",
            "xp": 100,
            "kind": "gamified",
            "situation": (
                "The chapter's first scenario game: diagnose a failing "
                "model from its symptoms in a live story — the "
                "differential-diagnosis capstone for the model-risk "
                "family."
            ),
            "beats": [
                (
                    "Diagnose like the exercise, but under story noise",
                    "The game serves narrative clues with distractors "
                    "(deadlines, opinions, vendor promises). The "
                    "procedure from the drill holds: locate where the "
                    "error lives (training set? held-out? live traffic? "
                    "specific groups?), then name the risk. The game "
                    "rewards the same two-step the repo's threat-hypothesis "
                    "form demands: mechanism first, story second.",
                ),
                (
                    "The abyss is the unmonitored gap",
                    "The game's title names the real failure: models sink "
                    "in the gap between deployment and the next audit. "
                    "Every winning move in the game is some version of "
                    "closing that gap — a baseline taken at launch, a "
                    "threshold with an owner, a re-check cadence.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/17-distribution-shift-and-deployment-reliability/README.md",
                    "Ch. 17",
                    "the deployment-reliability treatment.",
                ),
                (
                    "../../chapters/01-risk-models-and-research-epistemics/README.md",
                    "Ch. 01",
                    "threat-hypothesis discipline for the diagnosis.",
                ),
            ],
            "angle": (
                "A graded differential-diagnosis game — the clinical "
                "judgment layer on top of the seven-item list."
            ),
        },
        {
            "slug": "ch02-05-external-risks-in-ai",
            "n": 5,
            "title": "External risks in AI",
            "xp": 50,
            "kind": "video",
            "situation": (
                "The external-threats video: internal risks live within a "
                "model's design or data; external risks are attacks from "
                "outside actors trying to manipulate the model. Threats are "
                "diverse and target different aspects of AI systems, so the "
                "video organizes them into five groups."
            ),
            "beats": [
                (
                    "Adversarial input attacks (inference phase)",
                    "Attackers influence the deployed model's "
                    "decision-making by manipulating input data: an image "
                    "altered slightly makes a computer-vision system "
                    "misclassify — not recognizing a stop sign. The target "
                    "is the decision, the phase is inference.",
                ),
                (
                    "Data corruption and poisoning (training phase)",
                    "Attackers insert false or malicious data into the "
                    "training dataset so the AI learns incorrectly. Like "
                    "adversarial input attacks, this manipulates data — "
                    "but the target is the integrity of the model's "
                    "LEARNING, not its decisions. Example: fake product "
                    "reviews steering an e-commerce recommender. The "
                    "poisoning-versus-adversarial boundary is the phase "
                    "boundary: training versus inference.",
                ),
                (
                    "Model theft and inversion",
                    "Attacks aimed at stealing sensitive information FROM "
                    "the model: exploiting it to access or reconstruct its "
                    "confidential training data — manipulated inputs "
                    "uncovering private data used in training, like "
                    "personal photos from a facial-recognition system. "
                    "The target is neither the outputs nor the learning; "
                    "it is the training data itself.",
                ),
                (
                    "Infrastructure attacks",
                    "Targets the physical and virtual environments hosting "
                    "AI systems — the supporting infrastructure rather "
                    "than the models. The common example: flooding AI "
                    "servers with overwhelming requests from many sources "
                    "to overload them and make them inaccessible (the "
                    "denial-of-service family).",
                ),
                (
                    "Supply chain attacks and the best-practice set",
                    "Attacks on the components and libraries used in "
                    "development — a vulnerability injected into a widely "
                    "used AI library is present in every system built on "
                    "that library. The defense set the video names: "
                    "regular security audits; data validation and "
                    "sanitization to guard the integrity of training and "
                    "inference data; strong access controls restricting "
                    "system access; encryption of sensitive information "
                    "and anonymization where possible; continuous "
                    "monitoring for immediate response; a more secure "
                    "supply chain via trusted development tools, updated "
                    "regularly; and ongoing education and training for "
                    "staff. Risks evolve quickly — new threats emerge as "
                    "AI advances, so continuous learning, proactive risk "
                    "management, and vigilance are a must.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/12-adversarial-ml-and-robustness/README.md",
                    "Ch. 12",
                    "adversarial inputs and robustness at full depth.",
                ),
                (
                    "../../chapters/13-llm-application-security/README.md",
                    "Ch. 13",
                    "the application-security surface (inference-time "
                    "attacks).",
                ),
                (
                    "../../chapters/16-privacy-provenance-and-supply-chains/README.md",
                    "Ch. 16",
                    "model inversion, supply chain, and the "
                    "data-protection practices.",
                ),
                (
                    "../../chapters/14-agent-tool-memory-mcp-security/README.md",
                    "Ch. 14",
                    "infrastructure attacks on agentic systems.",
                ),
            ],
            "angle": (
                "The five-group external-risk taxonomy organized by attack "
                "target (decision, learning, data, infrastructure, supply "
                "chain) — the cleanest beginner statement of the "
                "outside-actor surface in this library."
            ),
        },
        {
            "slug": "ch02-06-types-of-external-risks",
            "n": 6,
            "title": "Types of external risks",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The drill for the five external-risk groups: classify by "
                "the attack's target and phase — the exercise the taxonomy "
                "was built for."
            ),
            "beats": [
                (
                    "Target-and-phase as the sorting key",
                    "The five groups sort cleanly on two axes: WHAT the "
                    "attack targets (decisions, learning, training data, "
                    "infrastructure, components) and WHEN it strikes "
                    "(inference, training, data handling, hosting, "
                    "development). A stem naming the target gives you the "
                    "group: 'misclassify a stop sign' → adversarial input; "
                    "'fake reviews' → poisoning; 'reconstruct personal "
                    "photos' → model inversion; 'flood the servers' → "
                    "infrastructure; 'vulnerability in a library' → supply "
                    "chain.",
                ),
                (
                    "The two confusions the exercise plants",
                    "Poisoning versus adversarial input (both manipulate "
                    "data; the phase differs), and inversion versus "
                    "theft (inversion reconstructs the training data; "
                    "theft copies the model — the exercise treats them as "
                    "one group with two aims, exactly as the video does).",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/12-adversarial-ml-and-robustness/README.md",
                    "Ch. 12",
                    "the inference-phase attack surface.",
                ),
                (
                    "../../chapters/16-privacy-provenance-and-supply-chains/README.md",
                    "Ch. 16",
                    "the data-phase attacks and their defenses.",
                ),
            ],
            "angle": (
                "Grades the two-axis classification — the sorting skill the "
                "video sets up and only an exercise can confirm."
            ),
        },
        {
            "slug": "ch02-07-keeping-up-with-external-ai-risks",
            "n": 7,
            "title": "Keeping up with external AI risks",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The drill for the defense half of the external-risks "
                "video: map each best practice to the risk group it "
                "counters — the exercise where the toolbox becomes a "
                "matching skill."
            ),
            "beats": [
                (
                    "The practice-to-group mapping",
                    "Audits → surface vulnerabilities across groups; "
                    "validation and sanitization → guard training and "
                    "inference data integrity (poisoning, adversarial "
                    "inputs); access controls → prevent unauthorized use "
                    "(theft, breaches); encryption and anonymization → "
                    "protect sensitive information (inversion, exposure); "
                    "continuous monitoring → catch emerging threats "
                    "(drift plus attacks); trusted, regularly updated "
                    "development tools → secure the supply chain; ongoing "
                    "staff education → the human layer every group "
                    "exploits first.",
                ),
                (
                    "The rule the exercise encodes",
                    "Defense is layered because attacks are phased: no "
                    "single practice covers two groups, and every answer "
                    "that claims one practice closes the whole surface is "
                    "the distractor. The repo's control chapter states the "
                    "same as 'defense in depth against a phased adversary'.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/16-privacy-provenance-and-supply-chains/README.md",
                    "Ch. 16",
                    "the data-protection practices in depth.",
                ),
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "layered defense as an engineering discipline.",
                ),
            ],
            "angle": (
                "Turns the defense list into a matching skill graded "
                "per-answer — practice the lecture format cannot give."
            ),
        },
        {
            "slug": "ch02-08-perimeter-peril-point",
            "n": 8,
            "title": "Perimeter Peril Point",
            "xp": 100,
            "kind": "gamified",
            "situation": (
                "The external-risks capstone game: an attack arrives; "
                "triage it under pressure and choose the response — the "
                "chapter's blue-team scenario."
            ),
            "beats": [
                (
                    "Triage = classify, then counter by group",
                    "The winning procedure is the drill's two-step with a "
                    "response bolted on: name the target and phase, then "
                    "pick the practice that counters THAT group — "
                    "sanitization for poisoning, input hardening for "
                    "adversarial, isolation and rotation for theft, "
                    "absorption and filtering for infrastructure floods, "
                    "provenance and patching for supply chain.",
                ),
                (
                    "The peril is the misread",
                    "Every losing move in the game is a misread of the "
                    "phase — responding to a poisoning incident with input "
                    "filters, or to a flood with model retraining. The "
                    "game makes the cost of the misread immediate, which "
                    "is the point of grading it.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/13-llm-application-security/README.md",
                    "Ch. 13",
                    "incident triage on the application surface.",
                ),
                (
                    "../../chapters/12-adversarial-ml-and-robustness/README.md",
                    "Ch. 12",
                    "robustness responses at full depth.",
                ),
            ],
            "angle": (
                "A graded blue-team triage game — response judgment the "
                "video courses describe but never score."
            ),
        },
        {
            "slug": "ch02-09-secure-development-practices",
            "n": 9,
            "title": "Secure development practices",
            "xp": 50,
            "kind": "video",
            "situation": (
                "The secure-development video: regular security measures "
                "are castle walls repelling basic attacks; secure "
                "development practices are the additional defense layer "
                "BUILT by the teams that create and maintain the systems — "
                "data practices first, then coding, access, and "
                "infrastructure."
            ),
            "beats": [
                (
                    "The four data practices",
                    "Data provenance and traceability: understanding the "
                    "origin of data and tracking its journey through the "
                    "AI system — provenance combats data poisoning by "
                    "pinpointing and removing corrupted data. Data "
                    "validation: checking and cleaning data before it is "
                    "fed to the system, ensuring accuracy, relevance, and "
                    "freedom from malicious tampering. Data minimization: "
                    "limiting collection and processing to only what is "
                    "absolutely necessary — significantly reducing the "
                    "risk of privacy breaches and data theft. Encryption "
                    "and anonymization: transforming sensitive data into a "
                    "secure format only authorized parties can access; "
                    "anonymization removes personally identifiable "
                    "information, protecting against model inversion "
                    "attacks aimed at extracting sensitive information "
                    "from the system.",
                ),
                (
                    "Secure coding, access management, secure infrastructure",
                    "Beyond data: secure coding practices (regular code "
                    "reviews, vulnerability scanning, coding standards "
                    "designed to prevent security flaws) shield against "
                    "infrastructure attacks by keeping the underlying "
                    "software robust against exploitation. Access controls "
                    "limit who can interact with the system and its data — "
                    "only trusted, verified individuals or entities may "
                    "modify the model or its data, which is what reduces "
                    "external attacks exploiting the system. Secure "
                    "infrastructure safeguards the hardware and software "
                    "environments: firewalls, intrusion detection systems, "
                    "secure cloud services — the solid foundation against "
                    "infrastructure-targeted threats.",
                ),
                (
                    "Security is not for the tech team alone",
                    "The video's closing move: business leaders fund the "
                    "security tools and training; legal experts check that "
                    "practices respect user privacy; regulators define "
                    "additional checks and balances. The teamwork is what "
                    "makes the systems not only secure but trusted and "
                    "reliable — the same four-pillar logic as chapter 1, "
                    "now applied to the development lifecycle.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/16-privacy-provenance-and-supply-chains/README.md",
                    "Ch. 16",
                    "provenance, minimization, anonymization — the deep "
                    "treatment.",
                ),
                (
                    "../../chapters/13-llm-application-security/README.md",
                    "Ch. 13",
                    "secure coding for the AI application layer.",
                ),
                (
                    "../../chapters/14-agent-tool-memory-mcp-security/README.md",
                    "Ch. 14",
                    "access control for agents with tools.",
                ),
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "the engineering discipline behind the practices.",
                ),
            ],
            "angle": (
                "The four data practices (provenance, validation, "
                "minimization, encryption/anonymization) named as a "
                "sequence — the beginner's data-protection ladder this "
                "repository taught only at expert depth."
            ),
        },
        {
            "slug": "ch02-10-secure-ai-development",
            "n": 10,
            "title": "Secure AI development",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The drill for the data practices: given a risk or a "
                "requirement, choose the practice — the exercise tests "
                "purpose-matching across the four."
            ),
            "beats": [
                (
                    "Match the practice to its purpose",
                    "The four data practices sort by what they are FOR: "
                    "provenance/traceability answers 'where did this data "
                    "come from and what happened to it' (the "
                    "anti-poisoning practice); validation answers 'is this "
                    "data accurate, relevant, untampered' (the "
                    "pre-ingestion gate); minimization answers 'do we need "
                    "this much' (the breach-surface reducer); "
                    "encryption/anonymization answers 'what happens if it "
                    "leaks anyway' (the last line against exposure and "
                    "inversion).",
                ),
                (
                    "The distractor pattern",
                    "Exercise stems that pair a practice with the WRONG "
                    "purpose are the graded content: minimization does not "
                    "detect tampering; validation does not remove "
                    "identifiers; encryption does not tell you the data's "
                    "origin. If the purpose sentence does not follow from "
                    "the practice's mechanism, reject the pairing.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/16-privacy-provenance-and-supply-chains/README.md",
                    "Ch. 16",
                    "the full data-protection treatment.",
                ),
                (
                    "../../chapters/02-evaluation-science-and-experimental-design/README.md",
                    "Ch. 02",
                    "data hygiene as evaluation hygiene.",
                ),
            ],
            "angle": (
                "Grades purpose-matching for the data-practice family — "
                "the step between knowing the names and deploying the "
                "right one."
            ),
        },
        {
            "slug": "ch02-11-secure-access",
            "n": 11,
            "title": "Secure access",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The drill for the access-management half of the video: "
                "who may interact with the AI system and its data, and "
                "under what verification."
            ),
            "beats": [
                (
                    "The access question has two sides",
                    "The video's rule: limit who can interact with the "
                    "system, and allow only trusted, verified individuals "
                    "or entities to MODIFY the model or its data. The "
                    "exercise probes both sides: read-access decisions "
                    "(who sees data) and write-access decisions (who may "
                    "change the model) — and the second is the "
                    "security-critical one, because every external attack "
                    "group that targets learning or data is looking for a "
                    "write path.",
                ),
                (
                    "The principle to apply in every stem",
                    "Access is granted by role and verification, not by "
                    "convenience: any stem where access is granted because "
                    "someone asked, is in a hurry, or is senior is the "
                    "wrong answer. The repo's phrase: authorization "
                    "follows verification; the course's phrase: trusted "
                    "and verified — same rule, different register.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/14-agent-tool-memory-mcp-security/README.md",
                    "Ch. 14",
                    "access control for AI systems with tools.",
                ),
                (
                    "../../chapters/13-llm-application-security/README.md",
                    "Ch. 13",
                    "the application layer's access surface.",
                ),
            ],
            "angle": (
                "Grades the modify-versus-read distinction — the access "
                "decision the security courses state and this exercise "
                "scores."
            ),
        },
        {
            "slug": "ch02-12-fortified-code-forge",
            "n": 12,
            "title": "Fortified Code Forge",
            "xp": 100,
            "kind": "gamified",
            "situation": (
                "The secure-development capstone game: build a system's "
                "defenses under constraints — choosing which practices to "
                "deploy with limited resources, the chapter's engineering "
                "trade-off scenario."
            ),
            "beats": [
                (
                    "Constrained choice is the real skill",
                    "The game presents a budget and a threat profile; the "
                    "winning play covers the highest-probability attack "
                    "groups first with the cheapest effective practice — "
                    "provenance against poisoning, input validation "
                    "against adversarial, minimization where the data is "
                    "sensitive, access control where modification is "
                    "possible. This is the course's preview of chapter 3's "
                    "threat prioritization: severity times likelihood "
                    "under budget.",
                ),
                (
                    "The forge's lesson",
                    "The title's claim: security is built, not bought — "
                    "the practices are the blacksmith's anvil, and the "
                    "game grades whether you can forge the right four bars "
                    "for the door that is actually under attack, not the "
                    "door you wish were under attack.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "the engineering trade-offs at full depth.",
                ),
                (
                    "../../chapters/16-privacy-provenance-and-supply-chains/README.md",
                    "Ch. 16",
                    "the practice menu in detail.",
                ),
            ],
            "angle": (
                "A graded resource-allocation game — the trade-off judgment "
                "chapter 3 will formalize, previewed here as play."
            ),
        },
        {
            "slug": "ch02-13-ai-risk-assessment-frameworks",
            "n": 13,
            "title": "AI risk assessment frameworks",
            "xp": 50,
            "kind": "video",
            "situation": (
                "The chapter's final video: formal risk assessments "
                "combined with ongoing internal checks and balances — the "
                "two-pronged approach — with the EU AI Act as the "
                "regulatory anchor."
            ),
            "beats": [
                (
                    "Why formal assessments, and what they contain",
                    "They establish a baseline understanding of potential "
                    "risks; involving diverse stakeholders gives a "
                    "comprehensive perspective; regular assessments let "
                    "the system adapt as circumstances change; and they "
                    "support legal and regulatory compliance, minimizing "
                    "losses, penalties, and reputational damage. The "
                    "elements: identify possible risks (privacy issues, "
                    "biases, security vulnerabilities); analyze how "
                    "likely and how impactful; evaluate against severity "
                    "and the company's risk tolerance; then develop the "
                    "strategy to manage, reduce, or eliminate.",
                ),
                (
                    "The EU AI Act's risk tiers",
                    "In the EU AI Act adopted in March 2024, risk "
                    "assessment is the cornerstone of regulating AI "
                    "development and deployment. Systems are grouped by "
                    "riskiness: unacceptable risk, high risk, limited "
                    "risk, minimal risk — and mitigation strategy follows "
                    "the classification. High-risk AI systems require a "
                    "risk assessment and risk management system; "
                    "low-risk systems allow alternative measures such as "
                    "following relevant codes of conduct.",
                ),
                (
                    "Internal checks and balances",
                    "The other prong: continuous monitoring to catch "
                    "emerging risks or unexpected model behavior, with "
                    "checks set from the formal assessment's results. "
                    "Named examples: regular bias testing to identify "
                    "unfair outputs, and monitoring for unexpected "
                    "behavior to catch performance degradation. These "
                    "ongoing checks act as an early warning system — "
                    "issues identified and addressed before they escalate "
                    "— fostering a safety-conscious culture.",
                ),
                (
                    "Not ticking boxes",
                    "The video's closing argument: formal assessments "
                    "provide the path for responsible development; "
                    "internal checks are the guardrails that keep you on "
                    "it. Effective AI risk management is a culture of "
                    "continuous vigilance supported by formal controls — "
                    "compliance with current regulation such as the EU AI "
                    "Act, adaptability to emerging challenges, and the "
                    "combination of formal assessment with day-to-day "
                    "monitoring that builds resilient, trustworthy AI "
                    "applications.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/23-governance-and-standards/README.md",
                    "Ch. 23",
                    "the EU AI Act from unacceptable to minimal risk, "
                    "obligation by obligation.",
                ),
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "assessment as an assurance document.",
                ),
                (
                    "../../chapters/01-risk-models-and-research-epistemics/README.md",
                    "Ch. 01",
                    "the risk-analysis method behind the four steps.",
                ),
            ],
            "angle": (
                "The only lesson in the library that teaches the EU AI "
                "Act's four-tier logic AND the two-pronged "
                "(formal-plus-continuous) assessment posture together, at "
                "beginner level."
            ),
        },
        {
            "slug": "ch02-14-the-eu-ai-act",
            "n": 14,
            "title": "The EU AI Act",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The drill for the risk tiers: classify systems into "
                "unacceptable / high / limited / minimal risk, and attach "
                "the obligations that follow."
            ),
            "beats": [
                (
                    "Classify by use, then attach the duty",
                    "The exercise gives system descriptions; the task is "
                    "the tier, then the consequence: unacceptable-risk "
                    "systems are banned; high-risk systems require a risk "
                    "assessment and risk management system; limited/minimal "
                    "risk systems take alternative measures such as codes "
                    "of conduct. The repo's governance chapter carries the "
                    "same tier table with the Act's own categories and "
                    "examples.",
                ),
                (
                    "The trap: capability words",
                    "Stems describing what a system CAN do are bait — the "
                    "tier follows the USE and the riskiness of the "
                    "deployment context, not the capability. An exercise "
                    "answer that tiers a system on its model size or its "
                    "cleverness is the distractor; the Act's logic (as the "
                    "video states) puts risk assessment at the cornerstone "
                    "for development AND deployment.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/23-governance-and-standards/README.md",
                    "Ch. 23",
                    "the full tier table and provider duties.",
                ),
            ],
            "angle": (
                "Grades tier classification — the regulatory judgment the "
                "governance courses teach at document level only."
            ),
        },
        {
            "slug": "ch02-15-risk-assessment-steps",
            "n": 15,
            "title": "Risk assessment steps",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The drill for the four-step assessment sequence: "
                "identify, analyze, evaluate, strategize — in order, with "
                "the right output at each step."
            ),
            "beats": [
                (
                    "The four steps and their outputs",
                    "Identify → the list of possible risks (privacy "
                    "issues, biases, security vulnerabilities). Analyze → "
                    "likelihood and impact per risk. Evaluate → ranking "
                    "against seriousness and the company's tolerance. "
                    "Strategize → the plan to manage, reduce, or eliminate. "
                    "The exercise grades the ORDER and the output type per "
                    "step; a strategize output at the analyze step is the "
                    "classic wrong answer.",
                ),
                (
                    "Why order matters",
                    "Each step's output is the next step's input: "
                    "evaluation without analysis has no likelihoods; "
                    "strategy without evaluation spends on the wrong "
                    "risks. The video's own framing — assessments must be "
                    "combined with checks set FROM their results — "
                    "requires the sequence to have run once, correctly, "
                    "before anything downstream can be set.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/01-risk-models-and-research-epistemics/README.md",
                    "Ch. 01",
                    "the analysis method the steps assume.",
                ),
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "assessment documents as assurance artifacts.",
                ),
            ],
            "angle": (
                "Grades the sequence — process discipline that the "
                "standards courses assert and only an exercise can drill."
            ),
        },
        {
            "slug": "ch02-16-assessment-framework-enclave",
            "n": 16,
            "title": "Assessment Framework Enclave",
            "xp": 100,
            "kind": "gamified",
            "situation": (
                "The chapter's final scenario game: design a risk "
                "assessment for a fictional organization — tier the "
                "system, choose the checks, set the cadence — the "
                "chapter-two capstone."
            ),
            "beats": [
                (
                    "Assemble the whole chapter",
                    "The game requires: the four steps in order (with "
                    "stakeholder input), the EU tier classification with "
                    "its duties, the internal checks set from the "
                    "assessment's results (bias testing, behavior "
                    "monitoring), and the culture posture — vigilance, "
                    "not box-ticking. Each round scores one of these; the "
                    "full run is the chapter in one playable pass.",
                ),
                (
                    "The enclave's lesson",
                    "An enclave is a protected space with a purpose — the "
                    "game's claim is that assessment design is exactly "
                    "that: a constructed, guarded procedure that produces "
                    "trust as its output. The repo's assurance chapter is "
                    "the formal version of the same claim.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/23-governance-and-standards/README.md",
                    "Ch. 23",
                    "the governance frame the game teaches.",
                ),
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "assurance as the discipline of evidence.",
                ),
            ],
            "angle": (
                "A graded assessment-design game — the two-pronged posture "
                "as playable judgment, the chapter's whole argument in one "
                "scenario."
            ),
        },
    ],
}
