# LangChain and LangGraph Practice Problems: Beginner to Hero

These 10 problems progress from basic LangChain usage to production-style, multi-agent LangGraph systems. Build them in order and keep each solution in a separate folder.

## 1. Beginner: Prompt-Powered Text Generator

Build a command-line application that accepts a topic and uses a prompt template plus a chat model to generate a short explanation of that topic for a beginner.

### Requirements

- Use a LangChain chat model.
- Create a reusable `ChatPromptTemplate`.
- Accept the topic and desired response length as inputs.
- Parse the model response into a plain string.
- Compose the components using LangChain Expression Language (LCEL).

### Done when

Running the application with `topic="recursion"` returns a clear, length-appropriate explanation without changing the prompt code.

## 2. Beginner: Structured Movie Recommendation

Create an application that recommends three movies based on a user's preferred genre, mood, and decade. Return each recommendation as structured data rather than free-form text.

### Requirements

- Define a Pydantic model for a movie recommendation.
- Request the title, release year, short reason, and content warning.
- Use structured output or an output parser.
- Validate the returned values.
- Handle malformed model output gracefully.

### Done when

The application consistently returns a validated list of three movie objects that can be serialized to JSON.

## 3. Easy: Conversation with Memory

Build a chatbot that remembers facts shared earlier in the same conversation, such as the user's name, favorite programming language, and current learning goal.

### Requirements

- Store messages using an appropriate LangChain chat history mechanism.
- Include conversation history in subsequent model calls.
- Support multiple sessions without mixing their histories.
- Add commands to start a new session and clear the current session.
- Demonstrate that the assistant can recall an earlier fact after at least five turns.

### Done when

Two users can chat under different session IDs, and each receives answers based only on their own conversation history.

## 4. Easy: Tool-Calling Utility Assistant

Create an assistant that can decide when to answer directly and when to call tools for arithmetic, current date/time, and unit conversion.

### Requirements

- Implement at least three tools with clear names, descriptions, and typed arguments.
- Bind the tools to a tool-capable chat model.
- Execute requested tool calls and return their results to the model.
- Prevent invalid tool arguments from crashing the application.
- Log which tool was selected for each request.

### Done when

The assistant correctly handles a mix of general questions, multi-step calculations, and unit conversions without calling unnecessary tools.

## 5. Intermediate: Document Question-Answering with RAG

Build a retrieval-augmented generation system that answers questions from a small collection of your own Markdown or PDF notes.

### Requirements

- Load and split the documents into useful chunks.
- Generate embeddings and store them in a vector store.
- Retrieve relevant chunks for each question.
- Instruct the model to answer only from retrieved context.
- Return citations containing the source filename and page or section where possible.
- Respond clearly when the documents do not contain the answer.

### Done when

You can show grounded answers for in-scope questions, useful citations, and an honest refusal for an out-of-scope question.

## 6. Intermediate: Stateful Support Workflow with LangGraph

Model a customer-support workflow as a LangGraph state machine. It should classify a request, gather missing information, produce a response, and escalate sensitive or unresolved cases.

### Requirements

- Define a typed graph state.
- Create separate nodes for classification, information gathering, response generation, and escalation.
- Use conditional edges to route requests.
- Include a loop when required customer information is missing.
- Add a recursion or retry limit so the graph cannot loop forever.
- Visualize or export the final graph structure.

### Done when

Billing, technical, incomplete, and high-risk requests each follow the expected path through the graph.

## 7. Advanced: Persistent Research Assistant

Create a LangGraph research assistant that plans a topic, searches a provided local knowledge base or search API, summarizes findings, and writes a final cited report. Its state must survive application restarts.

### Requirements

- Separate planning, research, synthesis, and review into graph nodes.
- Use a checkpointer with thread IDs for persistence.
- Allow a paused thread to resume after restarting the program.
- Keep research notes and cited sources in graph state.
- Add a reviewer node that can send weak reports back for another research pass.
- Cap the number of revision cycles.

### Done when

A partially completed research thread resumes successfully and produces a cited report after passing an explicit quality check.

## 8. Advanced: Human-in-the-Loop Approval Agent

Build an agent that drafts actions such as sending an email, issuing a refund, or modifying a record, but pauses for human approval before executing any consequential action.

### Requirements

- Represent proposed actions with structured data.
- Use LangGraph interrupts to pause before execution.
- Let a reviewer approve, reject, or edit the action.
- Resume the same graph thread with the review decision.
- Record an audit trail of proposals, edits, decisions, and results.
- Make execution idempotent so resuming cannot repeat an already completed action.

### Done when

You can demonstrate approved, rejected, and edited actions, including safe recovery from an application restart during approval.

## 9. Expert: Multi-Agent Software Team

Design a multi-agent system that takes a small feature request and coordinates a planner, developer, test engineer, and reviewer to produce a proposed code change.

### Requirements

- Give every agent a focused role and limited tools.
- Use a supervisor or explicit graph routing to coordinate handoffs.
- Store the plan, implementation notes, test results, and review feedback in shared state.
- Route failed tests back to the developer.
- Route serious review findings back for revision.
- Define termination conditions and maximum iteration counts.
- Isolate code execution in a safe sandbox or simulate execution if no sandbox is available.

### Done when

The workflow completes a small feature, passes its tests, addresses review feedback, and stops without uncontrolled agent-to-agent loops.

## 10. Hero: Production-Ready Adaptive Agent Platform

Build a deployable agent service that combines conversational memory, retrieval, tools, human approval, persistence, streaming, evaluation, and observability. The system should dynamically route each request to the simplest capable workflow.

### Requirements

- Expose the system through an API with streaming responses.
- Use LangGraph to route between direct answers, RAG, tool use, and approval-required actions.
- Persist threads and support resumable execution.
- Add authentication or per-user isolation for conversation data.
- Implement timeouts, retries, fallbacks, rate limits, and idempotency safeguards.
- Trace model calls, tool calls, latency, token usage, cost, errors, and graph paths.
- Create an evaluation dataset covering accuracy, groundedness, tool selection, safety, and regression cases.
- Run automated evaluations and report results before deployment.
- Defend against prompt injection in retrieved documents and tool inputs.
- Document the architecture, threat model, operational runbook, and key trade-offs.

### Done when

The service passes its evaluation thresholds, keeps different users' data isolated, safely resumes interrupted work, and provides enough traces and documentation to diagnose a failed request.

## Optional Rules for Every Problem

- Write unit tests for deterministic components.
- Keep prompts in dedicated modules or files.
- Store secrets in environment variables, never in source code.
- Add a README containing setup steps, an architecture summary, and example inputs and outputs.
- Record assumptions and explain important design decisions.
