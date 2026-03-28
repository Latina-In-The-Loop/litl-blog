---
layout: post
title: "The Hardest Part of Building an AI App Isn't the AI"
subtitle: "What a weeknight building GigOps taught me about credentials, architecture, and the real cost of just ship it"
date: 2026-03-24
tags: [agentic-ai, building, gigops, systems-thinking, product-management, automation]
---

There's a moment in every build where the fantasy collides with the file system.

You've been sketching on whiteboards, or in your head, or in a ChatGPT thread. You've got a name for the thing. You've described it to friends and they nodded enthusiastically. The idea has that rare quality of feeling both obvious in retrospect and genuinely useful — the kind that makes you think: why doesn't this exist yet?

Then you open your terminal and the clock starts.

This is what happened next.

## The Idea: GigOps

My husband plays in a working band. Not a famous one (yet). The kind that does weddings, corporate events, private parties — the kind where someone emails a booking inquiry on a Tuesday and by Friday you've exchanged seventeen messages, checked four calendars, negotiated a rate, confirmed a setlist, and still somehow forgot to ask about parking.

The coordination overhead is absurd. And it's almost entirely mechanical: the same questions, the same back-and-forth, the same status tracking. A human shouldn't be doing this. An AI should.

So I started building GigOps: an agentic AI coordinator that takes a booking inquiry and moves it through every stage of the process, from first contact to confirmed gig, without anyone manually herding it along. The dream version runs quietly in the background, sends the right emails at the right time, checks the calendar, and only surfaces something to a human when a real decision needs to be made. Everything else: handled.

## What I'm Actually Building

GigOps is a booking coordinator for a working band. That's the specific use case. But the pattern it represents is much broader.

There are hundreds of small service businesses — bands, photographers, caterers, DJs, videographers, event planners — where a significant fraction of the owner's time goes to coordination overhead. Email chains. Calendar checks. Follow-up messages. Status tracking. None of this requires judgment. All of it requires attention.

AI agents are well suited to this class of problem. The tasks are structured enough to automate but varied enough that rules-based systems break down. The cost of errors is low enough to tolerate occasional mistakes. And the humans involved, the clients, the vendor contacts, the band members, don't need to know an agent is coordinating. They just need to get the right message at the right time.

This is what agentic AI looks like in practice right now: not the flashy demos, but the quiet automation of the coordination layer in small businesses that can't afford operations staff. GigOps is my first version of that. The pattern shows up in a lot of places once you start looking for it.

## The Architecture Decision That Will Save Me Later

The first thing I did, before writing a single line of business logic, was make a structural decision that felt almost too boring to make.

I built a layer of separation between the application and everything it depends on.

Here's why that matters: every piece of application code talks to a single interface, not directly to any specific database, email provider, or calendar API. That interface is the only thing that knows what's actually running underneath. If I decide tomorrow that my current infrastructure choices are wrong, swapping them out is a small, contained change. The rest of the codebase is untouched.

This is the kind of decision that feels unnecessary when you're just trying to get something running. It adds maybe 30 minutes of overhead up front. And it will save dozens of hours later, not because you'll definitely change anything, but because knowing you could is what keeps you from making irreversible decisions under pressure.

> **Your architecture is a bet on what will change. Make the bet explicit.**

## Choosing the Right Infrastructure for Right Now

Early in a build, you're constantly making tradeoffs between speed and scalability. The temptation is to start with the proper solution, the one you'd use if you already had a thousand users. But that almost always costs more time and complexity than the project warrants at this stage.

I made a deliberately pragmatic infrastructure choice for this first version. It's not what I'd use at scale. But it has three things going for it right now: zero setup overhead, the ability for non-technical people to look at the data directly, and a clear migration path when the time comes. That last point is what makes the architecture decision above worth it. Boring infrastructure is fine, as long as you've built a door to walk out of later.

The one rule I imposed on myself: log every event before doing anything else. Whatever storage you're using, always write to the log first. It's a poor man's transaction record. If something goes wrong, you have a trail to follow.

This isn't a permanent choice. It's a right-now choice. Future me will swap it out when it stops being the right call.

## The Part Nobody Writes About: Credential Hell

This is where the build slowed down more than I expected.

Setting up the authentication and credential stack took longer than scaffolding the entire application. And it's not because it's hard. It's because the failure modes are subtle and the error messages are unhelpful.

The system I'm building needs to touch several Google services: calendar, email, and data storage. Each one has its own authentication model. Most of them are straightforward. One of them is not.

Sending email from a personal Gmail address is genuinely annoying to set up. The standard approach for server-to-server Google authentication doesn't work for personal Gmail accounts. You need a different flow entirely: set up an OAuth consent screen, register yourself as a test user, run a local authorization process, and capture a token you can store and reuse.

> There's an ordering dependency early in this process that isn't documented anywhere obvious. Skip it, and you get a cryptic error with no useful signal. Do it in the right order, and it works immediately.

If you're building anything that integrates with Google services and you're running on Windows, there's also a PowerShell configuration step that will silently block your scripts from running until you fix it. One command, run once, and it's done — but only if you know to look for it.

> I’ll write up the full setup separately. It’s the kind of thing you only understand after you’ve tripped over it once.

## On Using AI Tools to Build AI Tools

I used an AI coding tool for most of this build, one that takes a prompt and runs with it inside your terminal and codebase.

What this build made clear is that the tool matters less than the prompt. Whether you use Claude Code, Cursor, Windsurf, Gemini Code Assist, or any of the others, if you give it a clear, structured brief that specifies how the code should be organized, what conventions to follow, and what behavior you want, the output is remarkably similar across tools. The brief is the artifact. The tool is interchangeable.

I'm not loyal to a tool. I'm loyal to the brief.

The brief I wrote for GigOps is broken into sequenced parts. Each one gives the model a focused slice of the problem without overwhelming it. Each part has a clear completion condition before moving to the next. This isn't just good practice for working with AI. It's good practice for working with yourself. Breaking a build into sequenced parts with clear completion criteria is how you stay out of the weeds.

## The Honest Part

I'm writing this after a session that went well but not perfectly.

The email integration is more fragile than I'd like. I've confirmed the authorization works, but I haven't tested it end-to-end with a real message yet. That's a known risk I'm carrying into the next session. The data layer is stubbed out but not fully implemented. The scaffolding is there, the structure is right, but the core read/write logic isn't wired up yet. The app won't crash, but it won't do anything useful either. And the part where the actual intelligence lives, the coordination logic, is still to come.

None of this is failure. It's just the honest shape of a build in progress. The structural decisions are made. The hard infrastructure work is done. The foundation will hold.

What I expected going in was that the challenge would be getting the system to work.

What I ran into instead was everything around it: structure, sequencing, constraints, and the parts no demo shows.

The model was the easiest part. So far.

*The structure is in place. The foundation will hold.*

---

*If you're building something in this space, AI-powered coordination for small service businesses, where in the stack are you finding the friction you didn't expect?*

*This is **Latina-in-the-Loop** — a running exploration of what it means to build, question, and steward intelligent systems in real time. Follow along.*
