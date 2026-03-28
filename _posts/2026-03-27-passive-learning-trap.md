---
layout: post
title: "The Passive Learning Trap"
subtitle: "What a Remote Pilot License taught me about governing AI systems, and why your past expertise is more valuable than you think"
date: 2026-03-27
tags: [agentic-ai, building, gigops, systems-thinking, product-management, governance, learning]
---

There's a version of learning that feels productive but isn't.

You're reading. Watching. Taking courses. Chatting with LLMs. Collecting certificates. Absorbing a genuinely staggering amount of information. And still feeling like something is missing.

I spent most of 2023 and 2024 in that loop. I understood the concepts. I could hold a conversation about Generative AI. I could see the value and understand the potential. But I hadn’t built anything that worked in the real world. That was the point where understanding AI stopped being enough. There’s plenty of information about what AI is, and much less about how to design the systems around it.

## The Side Quest That Wasn't

At some point I did something that felt completely unrelated. I stepped away from AI entirely and earned my Remote Pilot License. On the surface: a break. A hobby. A side quest.

Getting my Remote Pilot License forced me to think differently.

A pilot doesn’t control everything directly. They operate inside a changing environment with rules, constraints, and incomplete information. Weather shifts. Conditions change. What looked straightforward a few minutes ago can become a bad decision once you factor in airspace, visibility, battery life, or what is happening on the ground.

The job is not to force certainty where there isn’t any. The job is to make sound decisions with the information you have, while staying inside the boundaries that keep people safe.

That changed the way I think about systems.

Flying a drone is not just about knowing how to move it. It is about judgment, restraint, and situational awareness. You are constantly assessing what matters, what might change, and whether the conditions still support the decision you were about to make. Sometimes the right move is to continue. Sometimes it is to pause. Sometimes it is not to fly at all.

That feels much closer to the challenge of building AI systems than I expected.

With agentic systems, a model response is only one part of the decision. The system still has to determine whether there is enough information to continue. What is the system allowed to do? What should trigger escalation? Where does human review belong? What happens when the information is incomplete, the output is shaky, or the environment changes halfway through the task?

That is the shift I’m starting to see more clearly. In both cases, the work is not just execution. It is governance.

> "I'd been practicing it at altitude. I just didn't have the vocabulary for it yet."

## The Misconception Running the Market

When I came back to AI, the conversation had shifted from Generative AI to Agentic AI. My first reaction: I'm behind. My second reaction, about two weeks later: actually, no. This is exactly the entry point I was waiting for.

Here's the misconception I keep seeing everywhere: that AI product success is a function of the model. That the team with access to the most powerful, highest-benchmark model wins. It's the wrong frame, and I think it's sending a lot of people in the wrong direction.

The model is one component. It's not even the hardest component. The true differentiators are the layers underneath:

- **Orchestration** how multiple models and data sources are coordinated
- **Guardrails** the operational constraints that keep the system reliable
- **Decision points** the logic that navigates non-linear, messy real-world workflows
- **Human-in-the-loop** knowing exactly where to place human oversight, and why

Think of it this way: the model is the engine. The systems around it are everything else, the airframe, the instruments, the checklist, the pilot. An engine sitting on the ground doesn't go anywhere.

## The Shift I Had to Make

Getting from traditional systems thinking to agentic AI required a real shift in how I think, not just what I know. Three things specifically had to change.

<div class="shift-table">
  <div class="shift-row">
    <div class="shift-inline">
      <span class="shift-from">Deterministic</span>
      <span class="shift-arrow">→</span>
      <span class="shift-to">Probabilistic</span>
    </div>
    <div class="shift-desc">I spent years building workflows with clear if-then logic: rigid, predictable, auditable. Agentic systems don't work that way. They generate. They hallucinate. They drift. I'm no longer writing rules; I'm managing uncertainty and building the boundaries that keep unpredictability inside acceptable limits.</div>
  </div>
  <div class="shift-row">
    <div class="shift-inline">
      <span class="shift-from">Execution</span>
      <span class="shift-arrow">→</span>
      <span class="shift-to">Governance</span>
    </div>
    <div class="shift-desc">I'm no longer the operator of a process. I'm the regulator of one. The system runs. My job is to define how it's allowed to run, what it's allowed to touch, when it has to stop and ask.</div>
  </div>
  <div class="shift-row">
    <div class="shift-inline">
      <span class="shift-from">Tools</span>
      <span class="shift-arrow">→</span>
      <span class="shift-to">Orchestration</span>
    </div>
    <div class="shift-desc">A single tool does a task. An orchestrated system manages the interaction between tools, and that interaction is where most of the complexity lives.</div>
  </div>
</div>

People with backgrounds in workflow automation and systems thinking are unusually well-positioned to make this shift. The foundation is already there. The new skills are real, but they're not starting from zero.

## What Building Actually Looks Like

It was 2 a.m. when I found Mahesh Yadav’s Agentic AI Product Management program. I watched one of his videos, liked his teaching style immediately, and realized this was the kind of hands-on work I’d been looking for. It was a little out of my budget, but I signed up that night anyway. I had already been connecting the dots. I just needed something that would force me to build.

The program started the following week and ran for six intense weeks. That’s where my thinking started to sharpen. Writing PRDs became a way to define an agent’s boundaries: what it could do, what it could not do, and what needed escalation. Workflow design meant planning for slow APIs, information that changes underneath you, and the reality that both people and systems behave less neatly than the workflow assumes. It also meant thinking through failure early and treating cost per run as part of the design, because pulling information from a request is not the same as taking an action based on it.

> "True clarity doesn't come from more reading. It comes from designing a system and watching it fail."

## The Expertise You Already Have

If you’ve worked in operations, workflow automation, legal tech, or any environment where processes carry real consequences, I don’t think you’re starting from scratch. You’ve probably already developed an instinct for where things break once they meet real conditions.

In my experience, the breakdown shows up in edge cases, ambiguous inputs, people who respond late or unpredictably, and external systems that technically return a success while still giving you something unusable. Agentic AI doesn’t remove those problems. It adds a new layer on top of them.

That’s part of why experience with deterministic systems still matters. You already know what silent failure looks like. You know how much damage a small assumption can do once it gets embedded in a workflow.

## Where I Am Now

I’m building now. Not perfectly, but for real. GigOps, the agentic booking coordinator I wrote about in the last post, is the first agentic system I’ve shipped using these principles. It has decision logic, human approval gates, and an architecture I can keep changing without having to rebuild the whole thing each time. The program gave me a framework and language for what I was doing. The build showed me where that thinking held up and where it didn’t.

If you’ve been stuck in the passive learning loop, reading, absorbing, waiting to feel ready, I don’t think the problem is a lack of effort. In some cases, it may be that your preparation has been aimed at understanding instead of application. What starts to change things is building something that has to operate under real conditions. Once that happens, the questions get more concrete very quickly. What can the system do on its own? Where does it need oversight? What happens when the input is incomplete or the workflow stops behaving the way you expected?

That’s the part that feels familiar to me. Governing a system under real conditions is not new. A lot of us have been doing some version of that for years.

*What changed my thinking wasn’t more material. It was having something real to govern.*

---

*If you've been learning but not yet building, what expertise from your past is waiting to be applied to the systems of the future?*

*This is **Latina-in-the-Loop** — a running exploration of what it means to build, question, and steward intelligent systems in real time. Follow along.*
