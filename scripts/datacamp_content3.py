"""DataCamp companion content — Chapter 3 (Strategic Integration of AI Security).

Shared content for scripts/gen_datacamp_companion.py. One entry per
lesson of the course's chapter 3 (17 lessons: 5 videos, 11 interactive
exercises, 1 gamified scenario, 1 wrap-up video). See
datacamp_content.py for the field contract and the honesty basis.
"""

CH3 = {
    "number": 3,
    "title": "Strategic Integration of AI Security",
    "purpose": (
        "Aligning security with organizational goals: connecting security "
        "efforts to tangible business value, fostering a security-aware "
        "culture, and keeping up with evolving risks and opportunities."
    ),
    "lessons": [
        {
            "slug": "ch03-01-from-insights-to-action",
            "n": 1,
            "title": "From insights to action",
            "xp": 50,
            "kind": "video",
            "situation": (
                "Chapter 3 opens: risk-assessment findings range from minor "
                "vulnerabilities to major threats, and leadership must "
                "decide what to do under limited resources and conflicting "
                "priorities. The video names the strategic considerations."
            ),
            "beats": [
                (
                    "Threat prioritization",
                    "Ranking risks by potential severity and probability — "
                    "similar to a risk matrix in a different format: groups "
                    "from high-impact high-likelihood down to low-impact "
                    "low-likelihood. The higher the severity and "
                    "probability, the higher the priority for a solution — "
                    "which is how resources reach the risks that pose the "
                    "greatest danger to the organization.",
                ),
                (
                    "Risk appetite",
                    "The level of risk an organization can accept — unique "
                    "per company, depending on industry, financial "
                    "strength, strategic goals, and risk management "
                    "capabilities. The video's contrast: a startup may "
                    "accept more risk because it strategically prioritizes "
                    "growth above all else; banks have stronger finances "
                    "and risk management capabilities but prioritize "
                    "trustworthiness.",
                ),
                (
                    "The innovation–security spectrum and cost versus benefit",
                    "There is always a compromise between pursuing "
                    "innovation and ensuring security — a spectrum with "
                    "innovation on one end and security on the other; "
                    "companies position differently, and the position "
                    "directly shapes how identified risks are managed. "
                    "Cost versus benefit weighs the expense of mitigation "
                    "against the potential cost of damage: security "
                    "measures are worth investing in when the cost of "
                    "reducing the risk is lower than the expected potential "
                    "losses (positive ROI).",
                ),
                (
                    "Low-hanging fruits and stakeholder interests",
                    "Look for actions implementable quickly that "
                    "significantly reduce risk — the video's example: an AI "
                    "loan-approval system overly reliant on a single data "
                    "point. Prioritizing them in the first wave shows "
                    "progress, boosts morale, and builds the base for "
                    "tackling more complex risks. Stakeholder interests "
                    "then rank risks by real-world impact: security "
                    "vulnerabilities may top the technical team's list "
                    "while legal emphasizes unmanaged bias — conflicting "
                    "viewpoints are collected and reconciled, and feeling "
                    "heard makes people more collaborative, increasing "
                    "transparency and trust.",
                ),
                (
                    "The strategic action plan",
                    "All steps combine into a plan with many levels: "
                    "high-level strategic considerations down to detailed "
                    "implementation plans for security initiatives. The "
                    "high-level perspective is key to seeing how mitigation "
                    "plans align with the organization's strategy.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "prioritization under budget as an assurance problem.",
                ),
                (
                    "../../chapters/01-risk-models-and-research-epistemics/README.md",
                    "Ch. 01",
                    "severity and likelihood as separate quantities.",
                ),
                (
                    "../../chapters/23-governance-and-standards/README.md",
                    "Ch. 23",
                    "risk appetite as a written instrument.",
                ),
            ],
            "angle": (
                "The only lesson in the library that teaches threat "
                "prioritization, risk appetite, the innovation–security "
                "spectrum, cost-versus-benefit, low-hanging fruits, and "
                "stakeholder reconciliation as one strategic toolkit — the "
                "management layer no technical course provides."
            ),
        },
        {
            "slug": "ch03-02-risk-appetite",
            "n": 2,
            "title": "Risk appetite",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The drill for the appetite concept: given an organization "
                "profile, reason about how much risk it can accept — the "
                "exercise tests the determinants, not the label."
            ),
            "beats": [
                (
                    "The four determinants",
                    "Industry, financial strength, strategic goals, and "
                    "risk management capabilities — the video's list. The "
                    "exercise pairs profiles with appetites: the startup "
                    "accepting more risk because growth is the strategic "
                    "priority; the bank with stronger finances and "
                    "capabilities but trustworthiness as the priority. "
                    "Answers must cite the determinant, not the vibe: 'it "
                    "accepts more risk BECAUSE its strategy prioritizes "
                    "growth'.",
                ),
                (
                    "Appetite is a position, not a virtue",
                    "The graded insight: neither end of the spectrum is "
                    "'more correct' — the position follows from the "
                    "organization's circumstances, and the exercise scores "
                    "consistency between profile and position. The repo's "
                    "glossary row on risk appetite is the same claim in "
                    "expert register.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/23-governance-and-standards/README.md",
                    "Ch. 23",
                    "risk appetite as a governance instrument.",
                ),
            ],
            "angle": (
                "Grades determinant-based reasoning — the management "
                "judgment the frameworks courses only describe."
            ),
        },
        {
            "slug": "ch03-03-balancing-innovation-and-security",
            "n": 3,
            "title": "Balancing innovation and security",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The drill for the spectrum: position decisions on the "
                "innovation–security line and read the consequences for "
                "risk management."
            ),
            "beats": [
                (
                    "Position determines response",
                    "Companies tending toward the innovation end accept "
                    "and manage risk differently from those tending toward "
                    "security — the video's rule that the position "
                    "directly impacts how identified risks are managed. "
                    "The exercise tests the inference both ways: from "
                    "position to management style, and from management "
                    "style back to position.",
                ),
                (
                    "The compromise is always there",
                    "The video is explicit: there is ALWAYS a compromise "
                    "between pursuing innovation and ensuring security. "
                    "Exercise answers claiming a position escapes the "
                    "compromise (innovation with no security cost, "
                    "security with no agility cost) are the marked-wrong "
                    "ones — the honest answer names both prices.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "the trade-off at engineering depth.",
                ),
                (
                    "../../chapters/21-sociotechnical-and-systemic-risk/README.md",
                    "Ch. 21",
                    "why the compromise is structural, not personal.",
                ),
            ],
            "angle": (
                "Grades two-way inference on the trade-off — the judgment "
                "layer the video asserts and the exercise confirms."
            ),
        },
        {
            "slug": "ch03-04-general-landora-implementor",
            "n": 4,
            "title": "General Landora Implementor",
            "xp": 100,
            "kind": "gamified",
            "situation": (
                "The chapter's scenario game: implement a security action "
                "plan for the fictional organization Landora — "
                "prioritizing findings, sequencing mitigation, and "
                "communicating the plan: the strategy chapter's capstone in "
                "play form."
            ),
            "beats": [
                (
                    "The implementor's sequence",
                    "The winning procedure: prioritize by severity times "
                    "likelihood under the budget; take the low-hanging "
                    "fruit first to show progress and boost morale; weigh "
                    "cost against expected loss for the expensive items; "
                    "reconcile stakeholder interests in the plan's "
                    "wording; and publish the multi-level plan — strategic "
                    "level down to implementation detail.",
                ),
                (
                    "What the game actually grades",
                    "Not the plan's cleverness but its alignment: every "
                    "round scores whether the chosen action serves "
                    "Landora's stated goals at its stated appetite — the "
                    "chapter's title claim (strategic INTEGRATION) made "
                    "playable. A brilliant action misaligned with the "
                    "strategy loses to a modest action aligned with it.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "the assurance view of sequencing.",
                ),
                (
                    "../../chapters/23-governance-and-standards/README.md",
                    "Ch. 23",
                    "plans as governance instruments.",
                ),
            ],
            "angle": (
                "A graded strategy-implementation game — the "
                "management-judgment layer no lecture can score."
            ),
        },
        {
            "slug": "ch03-05-aligning-with-organizational-goals",
            "n": 5,
            "title": "Aligning with organizational goals",
            "xp": 50,
            "kind": "video",
            "situation": (
                "The chapter's second video: security goes beyond "
                "protecting systems — it supports broader goals including "
                "ethical and social responsibility. Security decisions "
                "ripple into customer trust, brand reputation, and legal "
                "standing."
            ),
            "beats": [
                (
                    "Different strategies, different measures",
                    "Integrating security activities with business values "
                    "— responsible AI development, ethical principles, "
                    "corporate social responsibility — creates a solid "
                    "foundation. Market growth may dictate one approach; a "
                    "conservative strategy is essential where privacy and "
                    "trust are part of the business model.",
                ),
                (
                    "Two sides to every decision",
                    "The video's worked example: advanced encryption for "
                    "data protection creates strong safeguards, supporting "
                    "a goal of market leadership in customer trust — yet "
                    "the same decision can limit the agility of AI "
                    "systems and slow innovation. Every security choice "
                    "carries both faces, and the point is to SEE both "
                    "before choosing.",
                ),
                (
                    "The start-up versus the bank, in depth",
                    "The start-up: innovation is the lifeblood and "
                    "competitive edge, so security measures support rapid "
                    "development and deployment — agile threat modeling "
                    "for emerging technologies, emphasizing speed and "
                    "adaptability, open-source tools for flexibility, "
                    "accepting higher risks; security practices help "
                    "rather than hinder innovation, reflecting the focus "
                    "on breaking new ground and capturing market "
                    "opportunities. The bank: security and reliability "
                    "above all — sensitive financial data and the "
                    "regulatory landscape demand strict protocols; "
                    "comprehensive threat modeling to reduce data "
                    "integrity and privacy risks; objectives of trust, "
                    "customer loyalty, and regulatory compliance demand a "
                    "cautious approach to innovation.",
                ),
                (
                    "The link, stated as a rule",
                    "The start-up sees AI security as ENABLING innovation, "
                    "willing to navigate higher risks for speed and market "
                    "capture; the bank sees it as a critical FOUNDATION of "
                    "trust and regulatory compliance, prioritizing "
                    "robustness and reliability even if innovation slows. "
                    "The rule: start from a clear understanding of the "
                    "goals (innovation? speed to market? customer trust? "
                    "compliance?), let security strategy support those "
                    "objectives by balancing risk, innovation, and "
                    "responsibility — and never treat security as a "
                    "stand-alone item; it is an integral part of how the "
                    "organization does business.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/23-governance-and-standards/README.md",
                    "Ch. 23",
                    "strategy as the governance frame.",
                ),
                (
                    "../../chapters/21-sociotechnical-and-systemic-risk/README.md",
                    "Ch. 21",
                    "trust and reputation as systemic quantities.",
                ),
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "the engineering reading of 'align with goals'.",
                ),
            ],
            "angle": (
                "The start-up-versus-bank contrast is the course's "
                "signature strategic instrument — taught here as a full "
                "worked comparison, the management twin of the repo's "
                "technical trade-off chapters."
            ),
        },
        {
            "slug": "ch03-06-connecting-security-with-business-goals",
            "n": 6,
            "title": "Connecting security with business goals",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The drill for the alignment video: map security measures "
                "to the business goals they serve — the exercise tests "
                "direction of fit."
            ),
            "beats": [
                (
                    "Measure serves goal, never the reverse",
                    "The mapping the exercise grades: encryption serves a "
                    "trust or compliance goal (and prices agility); agile "
                    "threat modeling serves a speed-to-market goal (and "
                    "prices assurance depth); strict protocols serve "
                    "loyalty and regulatory goals (and prices innovation "
                    "speed). The wrong answers reverse the direction — "
                    "choosing a goal to fit a favorite measure.",
                ),
                (
                    "Every correct answer prices the second face",
                    "The video's two-sides rule carries into the exercise: "
                    "a mapping that states the benefit without the cost "
                    "is incomplete. Full credit answers carry both — "
                    "'this measure advances that goal at this price'.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/23-governance-and-standards/README.md",
                    "Ch. 23",
                    "goal alignment as a governance discipline.",
                ),
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "the assurance view of measures.",
                ),
            ],
            "angle": (
                "Grades the direction of fit — the alignment skill that "
                "turns security from a cost center into a strategy "
                "instrument."
            ),
        },
        {
            "slug": "ch03-07-health-care-versus-social-media",
            "n": 7,
            "title": "Health care versus social media",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The sector-pair drill: two industries with opposite "
                "profiles — the exercise the video's start-up-versus-bank "
                "template was built for, now across sectors."
            ),
            "beats": [
                (
                    "Sector profiles fix the posture",
                    "Health care: sensitive personal data, safety-critical "
                    "decisions, heavy regulation — a conservative posture, "
                    "privacy and trust as part of the business model, "
                    "security as foundation. Social media: growth and "
                    "engagement as the strategy, data volume as the asset, "
                    "lighter-touch regulation — an innovation-leaning "
                    "posture with higher accepted risk. The exercise "
                    "grades whether the chosen measures follow from the "
                    "profile: minimization and strict access for the "
                    "former; rapid iteration with monitoring for the "
                    "latter.",
                ),
                (
                    "The transferable skill",
                    "The point of the pairing: once you can run "
                    "profile-to-posture in two opposite sectors, you can "
                    "run it in any sector — the exercise's later stems "
                    "bring new industries, and the procedure (data "
                    "sensitivity, decision criticality, regulatory "
                    "weight, strategy) still answers them.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/16-privacy-provenance-and-supply-chains/README.md",
                    "Ch. 16",
                    "the data-protection weight the health-care side " "carries.",
                ),
                (
                    "../../chapters/21-sociotechnical-and-systemic-risk/README.md",
                    "Ch. 21",
                    "sector as a risk context.",
                ),
            ],
            "angle": (
                "The sector-pairing drill — industry-specific judgment the "
                "library's research courses never touch."
            ),
        },
        {
            "slug": "ch03-08-alignment-avenue",
            "n": 8,
            "title": "Alignment Avenue",
            "xp": 100,
            "kind": "gamified",
            "situation": (
                "The alignment scenario game: steer an organization's "
                "security decisions down its own strategic avenue — every "
                "round a decision, every decision scored against the "
                "strategy it must serve."
            ),
            "beats": [
                (
                    "Score against the strategy, not the textbook",
                    "The game's rule: a measure is right when it fits the "
                    "organization's goals and appetite, wrong when it "
                    "imports another organization's posture. The "
                    "innovation-heavy firm gets agile threat modeling and "
                    "accepted risk; the trust-heavy firm gets strict "
                    "protocols and slower innovation — and swapping the "
                    "playbooks between them is the losing move the game "
                    "grades hardest.",
                ),
                (
                    "The avenue is the strategy",
                    "The title's claim: alignment is a road you stay ON, "
                    "not a destination — the game's final round tests "
                    "whether, under a strategy shift mid-game, the "
                    "security posture shifts with it. Rigidity is the last "
                    "failure mode.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/23-governance-and-standards/README.md",
                    "Ch. 23",
                    "strategy-following as governance.",
                ),
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "posture shifts as assurance events.",
                ),
            ],
            "angle": (
                "A graded strategy-consistency game — alignment under "
                "change, which no static document can teach."
            ),
        },
        {
            "slug": "ch03-09-a-security-aware-culture",
            "n": 9,
            "title": "A security-aware culture",
            "xp": 50,
            "kind": "video",
            "situation": (
                "The culture video: an environment where employees "
                "recognize the importance of protecting data and "
                "understand their role in safeguarding the organization's "
                "digital assets. AI's complexity and evolving threats "
                "demand vigilance from everyone — security measures must "
                "evolve with the AI systems."
            ),
            "beats": [
                (
                    "The role map, team by team",
                    "IT and Security: the first line of defense against "
                    "external attacks, using the latest cybersecurity "
                    "tools and techniques; they identify risks from "
                    "inadequate protections or vulnerabilities. Data "
                    "Science: monitor the health and integrity of models "
                    "so they perform as expected without bias or error; "
                    "they identify model drift, unreliable outputs, and "
                    "correct vulnerabilities in algorithms that could be "
                    "exploited. Compliance and Legal: ensure efforts follow "
                    "laws and regulations; they recognize that personal "
                    "data in AI models needs more protection, or that "
                    "decision-making is insufficiently transparent. "
                    "Senior leadership: set the tone, decide which "
                    "measures are taken, allocate resources; they identify "
                    "strategic risks like an AI project misaligned with "
                    "organizational goals.",
                ),
                (
                    "The second half of the role map",
                    "Operations: real-world feedback on AI system "
                    "performance; they flag downtime or malfunctioning "
                    "systems, and their day-to-day experience helps "
                    "identify hallucinations in outputs. Human Resources: "
                    "cultivate a security-aware workforce through "
                    "training, keeping staff aware of best practices and "
                    "vigilance against external threats, avoiding "
                    "unintentional insider threats or data breaches. "
                    "Customer Service and Support: direct interaction with "
                    "users collects insights about external perception "
                    "and functionality; they spot user dissatisfaction or "
                    "trust concerns, particularly when AI decisions seem "
                    "biased or opaque — vital for uncovering hidden "
                    "vulnerabilities. External partners and vendors: align "
                    "with the organization's security culture by adhering "
                    "to agreed standards, and help identify "
                    "supply-chain vulnerabilities.",
                ),
                (
                    "The unified-culture claim",
                    "AI security is not the job of the tech team alone. A "
                    "unified culture built by diverse roles ensures "
                    "constant monitoring and protection over time; "
                    "everyone understands the unique value they bring, is "
                    "empowered to play an active role, and the company "
                    "stays resilient in a changing threat landscape — "
                    "security functions preserved and enhanced over time.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "safety culture as an engineering discipline (the "
                    "aviation/nuclear lineage).",
                ),
                (
                    "../../chapters/23-governance-and-standards/README.md",
                    "Ch. 23",
                    "the governance layer of culture.",
                ),
                (
                    "../../chapters/21-sociotechnical-and-systemic-risk/README.md",
                    "Ch. 21",
                    "culture as the systemic immune response.",
                ),
            ],
            "angle": (
                "The only lesson in the library that maps EIGHT roles plus "
                "external partners to the specific risks each catches — "
                "the organization chart of security this repository had "
                "no entry for until this companion."
            ),
        },
        {
            "slug": "ch03-10-responsible-for-identifying-risks",
            "n": 10,
            "title": "Responsible for identifying risks",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The first culture drill: given a risk, name the team whose "
                "job it is to catch it — the exercise tests the role map "
                "in both directions."
            ),
            "beats": [
                (
                    "Route the risk to its natural catcher",
                    "The mapping: drift and unreliable outputs → Data "
                    "Science; inadequate protections and vulnerabilities → "
                    "IT/Security; personal-data exposure and insufficient "
                    "transparency → Compliance/Legal; misaligned AI "
                    "projects → Senior leadership; downtime and "
                    "malfunctioning systems → Operations; workforce "
                    "vigilance and insider-threat avoidance → HR; user "
                    "dissatisfaction and trust concerns → Customer "
                    "Service; supply-chain vulnerabilities → external "
                    "partners under agreed standards.",
                ),
                (
                    "The 'not my job' answer is always wrong",
                    "The video's thesis is the exercise's trap: unified "
                    "culture means every risk has a named catcher, and "
                    "stems describing a risk nobody claims are the ones "
                    "the exercise marks wrong — the culture failure is "
                    "the answer's content.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "safety culture as engineering.",
                ),
                (
                    "../../chapters/21-sociotechnical-and-systemic-risk/README.md",
                    "Ch. 21",
                    "the systemic view of who catches what.",
                ),
            ],
            "angle": (
                "Grades the role-to-risk routing — the culture map as an "
                "operational skill, not a poster."
            ),
        },
        {
            "slug": "ch03-11-role-of-data-science-team-in-security",
            "n": 11,
            "title": "Role of data science team in security",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The deep drill on one role: the data science team's "
                "specific duties in the security culture — the exercise "
                "the course's own emphasis on DS teams earns."
            ),
            "beats": [
                (
                    "The DS team's three duties",
                    "Monitor model health and integrity so systems perform "
                    "as expected without bias or error over time; identify "
                    "model drift and unreliable outputs; identify and "
                    "correct vulnerabilities in AI algorithms that could "
                    "be exploited. The exercise discriminates these from "
                    "neighboring duties: infrastructure vulnerabilities "
                    "are IT/Security's; legal exposure is Compliance's; "
                    "the DS line is the MODEL's behavior and its "
                    "algorithms.",
                ),
                (
                    "Why the course singles this role out",
                    "Because the DS team owns the model lifecycle, it is "
                    "the only role that can run the chapter-2 monitoring "
                    "posture — bias testing, drift watching — inside the "
                    "chapter-3 culture. The exercise is the join point of "
                    "the two chapters.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/17-distribution-shift-and-deployment-reliability/README.md",
                    "Ch. 17",
                    "the monitoring duties in depth.",
                ),
                (
                    "../../chapters/09-mechanistic-interpretability-foundations/README.md",
                    "Ch. 09",
                    "algorithm transparency as an research duty.",
                ),
            ],
            "angle": (
                "A dedicated drill for one role — the DS-team emphasis the "
                "course makes and no other lesson in the library matches."
            ),
        },
        {
            "slug": "ch03-12-culture-citadel",
            "n": 12,
            "title": "Culture Citadel",
            "xp": 100,
            "kind": "gamified",
            "situation": (
                "The culture capstone game: build and defend a "
                "security-aware culture through scenario rounds — the "
                "chapter's organizational judgment in playable form."
            ),
            "beats": [
                (
                    "The citadel's walls are the roles",
                    "Each round tests one wall: is the risk routed to its "
                    "natural catcher? is the workforce trained (HR)? is "
                    "leadership resourcing the measures it demands? is "
                    "feedback from operations and customer service "
                    "reaching the model teams? The game grades the "
                    "routing, not the heroics — one role cannot hold the "
                    "citadel alone.",
                ),
                (
                    "Culture under attack",
                    "The losing rounds are culture failures: a risk "
                    "everyone assumed someone else owned; a leadership "
                    "tone that security is a tech-team matter; partners "
                    "outside the agreed standards. The game's thesis is "
                    "the video's: unified culture is the structure that "
                    "keeps monitoring and protection running over time.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "safety culture as the engineering inheritance.",
                ),
                (
                    "../../chapters/21-sociotechnical-and-systemic-risk/README.md",
                    "Ch. 21",
                    "the systemic reading of culture.",
                ),
            ],
            "angle": (
                "A graded culture-building game — organizational judgment "
                "no technical course even attempts."
            ),
        },
        {
            "slug": "ch03-13-ai-security-for-the-future",
            "n": 13,
            "title": "AI security for the future",
            "xp": 50,
            "kind": "video",
            "situation": (
                "The course's final teaching video: a mindset of constant "
                "change. Regular advances in AI mean security must "
                "constantly adapt; the video examines regulation, "
                "synthetic data, and AGI as the emerging trends that "
                "impact AI security."
            ),
            "beats": [
                (
                    "Evolving regulation",
                    "Governments balance allowing innovation, respecting "
                    "public concerns, ensuring responsible and ethical AI, "
                    "and fair use of intellectual property. Regulation "
                    "influences how organizations can collect, store, and "
                    "use data within AI systems; ongoing litigations under "
                    "existing legislation will influence best practices; "
                    "companies must be ready to adapt to new regulations.",
                ),
                (
                    "Synthetic data",
                    "Artificial data sets that resemble real-world "
                    "information without containing personal details or "
                    "using others' intellectual property. Organizations "
                    "explore synthetic data to ease privacy and ownership "
                    "concerns — a range of benefits, but new security "
                    "challenges: measures must be designed to ensure the "
                    "integrity and robustness of synthetic data.",
                ),
                (
                    "AGI — the potential game changer",
                    "AGI refers to AI systems that can understand and "
                    "learn any intellectual task a human can. There is "
                    "disagreement about how likely the technology is, but "
                    "awareness of the possibility is essential. Experts "
                    "predict it could revolutionize aspects of our lives; "
                    "its immense potential power requires robust security "
                    "considerations built in from the beginning, "
                    "safeguarding against potential misuse.",
                ),
                (
                    "Explainability, transparency, continuous improvement, adaptive leadership",
                    "With developments like these, explainability and "
                    "transparency become increasingly important: "
                    "explaining how AI systems work allows quicker "
                    "adaptation of security measures as new threats arise, "
                    "and transparency alleviates concerns about misuse or "
                    "bias while helping avoid legal issues. Organizations "
                    "must foster continuous improvement — without it, AI "
                    "security falls behind, and outdated defenses are more "
                    "vulnerable to attacks, data breaches, and compliance "
                    "issues, eroding trust, costing money, and hindering "
                    "innovation. Adaptive leadership proactively enables a "
                    "long-term security strategy instead of reacting to "
                    "threats; an agile leadership approach makes it easier "
                    "to keep up with new regulations, technologies, and "
                    "threats.",
                ),
                (
                    "Staying on top of new developments",
                    "Not only threats change quickly — new developments "
                    "can also IMPROVE a company's security position. Ways "
                    "to stay up to date: attending industry conferences, "
                    "following security researchers' work, subscribing to "
                    "relevant publications, connecting with the broader AI "
                    "security community, participating in online forums. "
                    "As AI advances, organizations must cultivate a "
                    "'security in motion' mindset — staying informed and "
                    "adaptable for secure AI development and risk "
                    "management.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/23-governance-and-standards/README.md",
                    "Ch. 23",
                    "the regulation chapter — instruments and regimes.",
                ),
                (
                    "../../chapters/16-privacy-provenance-and-supply-chains/README.md",
                    "Ch. 16",
                    "synthetic data in the provenance treatment.",
                ),
                (
                    "../../chapters/01-risk-models-and-research-epistemics/README.md",
                    "Ch. 01",
                    "AGI as a hypothesis with conditions, not a fact.",
                ),
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "continuous improvement as an assurance obligation.",
                ),
            ],
            "angle": (
                "The only lesson in the library that teaches regulation, "
                "synthetic data, and AGI as one forward-looking set at "
                "beginner level — the future-facing gloss this "
                "repository's working surfaces lacked."
            ),
        },
        {
            "slug": "ch03-14-staying-up-to-date",
            "n": 14,
            "title": "Staying up-to-date",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The drill for the forward-looking material: the "
                "staying-current toolbox and the cost of falling behind — "
                "the exercise tests the maintenance posture."
            ),
            "beats": [
                (
                    "The toolbox and what each channel is for",
                    "Conferences (the field's state of the art, in person); "
                    "security researchers' work (the earliest warnings); "
                    "relevant publications (the curated record); the "
                    "broader AI security community and online forums (the "
                    "ongoing conversation). The exercise matches needs to "
                    "channels: 'earliest signal on a new attack' → "
                    "researchers; 'structured ongoing education' → "
                    "publications; 'community verification' → forums.",
                ),
                (
                    "The price of stagnation",
                    "The video's cost list, as the exercise's wrong-answer "
                    "engine: outdated defenses are more vulnerable to "
                    "attacks, data breaches, and compliance issues — "
                    "eroding trust, costing money, hindering innovation. "
                    "Any stem where an organization stops updating and "
                    "expects security to hold is the marked failure.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "continuous improvement as discipline.",
                ),
                (
                    "../../chapters/23-governance-and-standards/README.md",
                    "Ch. 23",
                    "the regulatory watch as governance.",
                ),
            ],
            "angle": (
                "Grades the maintenance posture — the habit layer of "
                "security that the one-shot courses never revisit."
            ),
        },
        {
            "slug": "ch03-15-it-takes-a-village",
            "n": 15,
            "title": "It takes a village",
            "xp": 50,
            "kind": "exercise",
            "situation": (
                "The ecosystem-recall drill: apply the chapter-1 ecosystem "
                "frame to the future-facing material — the exercise that "
                "closes the loop between the course's first and last "
                "chapters."
            ),
            "beats": [
                (
                    "Future topics are ecosystem topics",
                    "Regulation, synthetic data, and AGI each implicate "
                    "the four pillars: people (who tracks them?), legal "
                    "(what do they require?), technology (what do they "
                    "change?), processes (what must be updated?). The "
                    "exercise grades whether the learner routes each "
                    "future topic through the pillars rather than treating "
                    "it as a technical curiosity.",
                ),
                (
                    "The village, again",
                    "The title repeats the culture video's thesis in the "
                    "future tense: staying current is a collective act — "
                    "the channels in the previous exercise are people, and "
                    "the exercise marks answers that assign the future to "
                    "one team.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/21-sociotechnical-and-systemic-risk/README.md",
                    "Ch. 21",
                    "the systemic frame for future topics.",
                ),
                (
                    "../../chapters/23-governance-and-standards/README.md",
                    "Ch. 23",
                    "the regulatory watch.",
                ),
            ],
            "angle": (
                "The loop-closing drill — first-chapter frames applied to "
                "last-chapter topics, the course's own design move made "
                "gradable."
            ),
        },
        {
            "slug": "ch03-16-throne-of-stagnation",
            "n": 16,
            "title": "Throne of Stagnation",
            "xp": 100,
            "kind": "gamified",
            "situation": (
                "The course's final scenario game: the kingdom that stops "
                "adapting — the cost of stagnation played out against the "
                "cost of change, the whole course's argument in one last "
                "game."
            ),
            "beats": [
                (
                    "Stagnation versus adaptation, scored",
                    "Each round pairs a change (new regulation, new "
                    "threat, new capability) with a response (adapt or "
                    "hold). The game scores the HOLD moves by their "
                    "compounding costs — vulnerability, breach, "
                    "compliance, trust — and the ADAPT moves by their "
                    "trade-off prices. The winning line is the video's: "
                    "adaptive leadership, proactive strategy, security in "
                    "motion.",
                ),
                (
                    "The throne is the trap",
                    "The title's warning: the throne is comfortable — "
                    "stagnation feels like stability and prices like "
                    "fragility. The game's final rounds make the "
                    "accumulated cost visible at once, which is the "
                    "argument the entire course has been building: "
                    "constant change is the condition, not the exception.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/22-safety-engineering-and-assurance/README.md",
                    "Ch. 22",
                    "continuous improvement as the counter-posture.",
                ),
                (
                    "../../chapters/17-distribution-shift-and-deployment-reliability/README.md",
                    "Ch. 17",
                    "the world moves; systems must follow.",
                ),
            ],
            "angle": (
                "The course's closing game — stagnation priced as a "
                "playable collapse, the argument no summary can land like "
                "a score can."
            ),
        },
        {
            "slug": "ch03-17-wrap-up-ai-security-and-risk-management",
            "n": 17,
            "title": "Wrap-up: AI Security and Risk Management",
            "xp": 50,
            "kind": "video",
            "situation": (
                "The course's closing video: a recap of the three chapters "
                "and pointers for further learning — the course's own "
                "statement of what it believes a beginner should carry "
                "forward."
            ),
            "beats": [
                (
                    "The recap, chapter by chapter",
                    "Chapter 1: AI has its own unique set of security "
                    "risks; due to AI's complexity and unexpected "
                    "outcomes, it is crucial to consider and involve "
                    "different perspectives. Chapter 2: risk-management "
                    "fundamentals — AI development and deployment risks, "
                    "external threats, and methods for discovering and "
                    "countering vulnerabilities. Chapter 3: the "
                    "integration of AI risk management with organizational "
                    "strategy, taught through the start-up-versus-bank "
                    "example.",
                ),
                (
                    "What next, per the instructor",
                    "Staying up to date matters in a dynamic field. The "
                    "recommended follow-ons: AI Ethics, Artificial "
                    "Intelligence (AI) Strategy, Explainable Artificial "
                    "Intelligence (XAI) Concepts, and the instructor's "
                    "other course, Introduction to Data Security. The "
                    "instructor also invites learners to the Data Girl and "
                    "Friends initiative — empowering young people through "
                    "activities supporting awareness and critical thinking "
                    "in an AI-driven digital world.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/24-research-practice-and-capstone-execution/README.md",
                    "Ch. 24",
                    "the repo's own capstone: where a beginner goes after " "the survey courses.",
                ),
                (
                    "../../roadmaps/careers-index.md",
                    "the careers index",
                    "the routes the follow-on courses gesture at, mapped "
                    "with entry mechanisms and progress ladders.",
                ),
            ],
            "angle": (
                "The course's own closing claim — the survey is the "
                "invitation, and the follow-on list is the instructor's "
                "map of the field; this repository is the deeper ladder "
                "each rung of that map points toward."
            ),
        },
    ],
}
