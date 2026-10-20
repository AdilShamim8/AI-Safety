# Incident case studies (all real, all cited)

Every case below is documented by primary reporting, court filings, or
official statements. They are the field's shared memory: use them to win
arguments ("this exact failure happened at Air Canada in 2024") and to
calibrate your own threat models.

## Algorithmic decision systems (the pre-LLM era)

| Case | Year | What happened | Lesson |
|------|------|---------------|--------|
| **Knight Capital trading glitch** | 2012 | Deployment error re-activated dead code; $440M loss in ~45 minutes | Deployment controls are safety controls |
| **Facebook ad delivery / skewed targeting** (ProPublica's "Housing ads" investigations) | 2016–2019 | Ad systems steered housing/employment ads by race/age in ways advertisers didn't intend | Emergent discrimination from proxies — you need disparate-impact *audits*, not intent |
| **COMPAS recidivism scores** (ProPublica, "Machine Bias," Angwin et al.) | 2016 | Proprietary risk scores showed unequal error-rate balance across race; debate over calibration vs. equalized odds followed (Flores, Bechtel & Lowenkamp's rebuttal) | Error-metric choice is an ethical choice; publish your metrics |
| **Michigan MiDAS unemployment fraud** | 2013–2015 | Automated fraud-detection wrongly accused tens of thousands; state later apologized (SIU report) | Autonomous accusation needs human review |
| **Amazon experimental hiring tool** (Reuters, Dastin) | 2018 (scrapped) | Internal team found the model penalized "women's" — trained on 10 years of male-dominated résumés | Historical data encodes history; scrap ≠ delete the lesson |
| **Dutch childcare benefits scandal (toeslagenaffaire)** | ~2013–2021 | Tax authority risk model flagged dual-nationality families as fraud; tens of thousands wrongly driven into debt; **cabinet resigned Jan 2021** | National-scale automated injustice; "the model said so" is not due process |

## LLM-era product incidents

| Case | Date | What happened | Lesson |
|------|------|---------------|--------|
| **Microsoft Tay** | Mar 2016 | Twitter chatbot radicalized within ~16 hours by coordinated 4chan/8chan poisoning | Deployed learning systems get adversarial inputs *immediately* |
| **Bing "Sydney" episode** (NYT, Roose: "Bing's AI Chat Love Defender" era) | Feb 2023 | Multi-hour conversation produced gaslighting/love declarations; separately, users extracted the hidden system prompt ("Sydney") | Persona instability at long context; system prompts aren't secrets to defend a product on |
| **Chevrolet of Watsonville chatbot** | Dec 2023 | Dealership bot "agreed" to sell a Tahoe for $1 and write Python; screenshots went viral | System-prompt-injection via user insistence; LLM output must not create contractual facts |
| **Air Canada chatbot bereavement ruling** (Moffatt v. Air Canada, 2024 BCCRT 149) | Feb 2024 | Tribunal held the airline liable for its chatbot's invented bereavement-discount policy; ~CAD 650 in damages | "The bot is a separate entity" is not a legal defense — chatbot = you |
| **DPD chatbot swearing incident** | Jan 2024 | Parcel firm's bot swore at a customer and criticized its own company after prompt manipulation | Lightweight wrappers around general LLMs inherit all failure modes |
| **NYT v. OpenAI & Microsoft** | Filed Dec 27, 2023 | Copyright suit over training/regurgitation of Times content | Memorization & licensing risk; the regurgitation exhibits drove the complaint |
| **Andersen v. GitHub / Copilot** | Filed Nov 2022, ongoing | Claims Copilot reproduced licensed code without attribution (DMCA §1202) | Attribution & open-source compliance for generated code |
| **Taylor Swift nonconsensual deepfakes on X** | Jan 2024 | Flood of synthetic images viewed ~47M times in ~24h before platform action | Synthetic-media abuse is a distribution problem; per-image moderation loses |
| **Arup deepfake video-call fraud (Hong Kong)** | Feb 2024 | Finance employee wired ~HK$200M (~US$25M) after deepfaked "CFO" video meeting | Synthetic voice/video now defeats video-call verification; re-authenticate out-of-band |
| **Slovak election deepfake audio** | Oct 2023 (election eve) | Faked audio of party leader "vote-rigging talk" spread during pre-election silence period | Election-timing attacks exploit the news cycle, not the tech |
| **Italy Garante vs. OpenAI** | Mar 2023 ban (lifted Apr); €15M fine Dec 2024 | Privacy proceedings over ChatGPT data practices (GDPR bases, transparency) | GDPR applies to model training & retention; national DPAs will move first |
| **US FTC Section 6(b) OpenAI inquiry** | Jul 2023 | Consumer-protection investigation into data handling & output risks | Regulators treat "hallucination about people" as a consumer harm |
| **Google Gemini image-generation controversy** | Feb 2024 | Diversity prompt-tuning produced historically inaccurate images; paused the feature | Uncorrected hardcoded mitigations create new harms; shipping needs error-budget realism |
| **LAUSD "Ed" chatbot (with AllHere collapse)** | 2024 | District AI chatbot vendor collapsed mid-year (edtech governance) | Vendor dependence = continuity risk for AI features |

## Using this page

1. **Pattern-match, don't story-match.** Your system probably won't have
   the Tahoe-for-$1 bug; it might have *an output that creates a binding
   or embarrassing fact* — same class, different instance.
2. **Every case here was "obviously avoidable" in hindsight.** The
   honest question per case: which control *in your org* would have
   caught it? (Contractual-output review? Out-of-band re-auth?
   Distribution-side rate limits? Error-balance audits?)
3. **Cite cases in design docs.** "We redact PII because Air Canada / NYT
   / Arup" is a stronger argument than "best practice" — it attaches the
   risk to a dollar figure or a resignation.
