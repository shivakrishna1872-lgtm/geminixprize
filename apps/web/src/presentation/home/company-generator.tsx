"use client";

import { useMemo, useState } from "react";
import type { CompanyBlueprint } from "@antigravity/contracts";

type GenerationState =
  | { status: "idle"; blueprint?: never; message?: never }
  | { status: "authenticating"; blueprint?: never; message?: never }
  | { status: "generating"; blueprint?: never; message?: never }
  | { status: "ready"; blueprint: CompanyBlueprint; message?: never }
  | { status: "error"; blueprint?: never; message: string };

export function CompanyGenerator() {
  const [idea, setIdea] = useState(() => {
    if (typeof window === "undefined") {
      return "build me a waterbottle company";
    }

    return new URLSearchParams(window.location.search).get("business-idea") ?? "build me a waterbottle company";
  });
  const [password, setPassword] = useState("");
  const [geminiApiKey, setGeminiApiKey] = useState("");
  const [openaiApiKey, setOpenaiApiKey] = useState("");
  const [secretsConfigured, setSecretsConfigured] = useState(false);
  const [state, setState] = useState<GenerationState>({ status: "idle" });

  const isWorking = state.status === "authenticating" || state.status === "generating";

  const buttonLabel = useMemo(() => {
    if (state.status === "authenticating") {
      return "Authenticating";
    }
    if (state.status === "generating") {
      return "Generating";
    }
    return "Generate company";
  }, [state.status]);

  async function handleGenerate() {
    setState({ status: "authenticating" });

    const authResponse = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
    });

    if (!authResponse.ok) {
      setState({ status: "error", message: "Enter the founder passcode to unlock generation." });
      return;
    }

    setState({ status: "generating" });

    if (geminiApiKey.trim() || openaiApiKey.trim()) {
      const secretsResponse = await fetch("/api/auth/secrets", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          geminiApiKey: geminiApiKey.trim() || undefined,
          openaiApiKey: openaiApiKey.trim() || undefined,
        }),
      });

      if (!secretsResponse.ok) {
        setState({ status: "error", message: "Could not save API keys for this browser session." });
        return;
      }

      setSecretsConfigured(Boolean(geminiApiKey.trim()));
      setGeminiApiKey("");
      setOpenaiApiKey("");
    }

    const generationResponse = await fetch("/api/company/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ idea }),
    });

    if (!generationResponse.ok) {
      setState({ status: "error", message: "Generation failed. Check that the API server and Gemini key are configured." });
      return;
    }

    const blueprint = (await generationResponse.json()) as CompanyBlueprint;
    setState({ status: "ready", blueprint });
  }

  return (
    <div className="generator-shell">
      <form className="idea-console" aria-label="Business idea prompt">
            <label htmlFor="business-idea">What should MadeThis build?</label>
        <div>
          <input
            id="business-idea"
            name="business-idea"
            onChange={(event) => setIdea(event.target.value)}
            placeholder="A premium desk setup brand for remote engineers"
            type="text"
            value={idea}
          />
          <button
            disabled={isWorking}
            onClick={() => {
              void handleGenerate();
            }}
            type="button"
          >
            {buttonLabel}
          </button>
        </div>
        <label htmlFor="founder-passcode">Founder passcode</label>
        <input
          id="founder-passcode"
          name="founder-passcode"
          onChange={(event) => setPassword(event.target.value)}
          placeholder="Enter passcode"
          type="password"
          value={password}
        />
        <label htmlFor="gemini-api-key">Gemini API key</label>
        <input
          id="gemini-api-key"
          name="gemini-api-key"
          onChange={(event) => setGeminiApiKey(event.target.value)}
          placeholder={secretsConfigured ? "Gemini key saved for this session" : "Paste Gemini API key"}
          type="password"
          value={geminiApiKey}
        />
        <label htmlFor="openai-api-key">OpenAI API key, optional</label>
        <input
          id="openai-api-key"
          name="openai-api-key"
          onChange={(event) => setOpenaiApiKey(event.target.value)}
          placeholder="Stored for future features, not used by generation"
          type="password"
          value={openaiApiKey}
        />
      </form>

      {state.status === "error" ? <p className="generator-error">{state.message}</p> : null}

      {state.status === "ready" ? (
        <section className="mission-control" aria-label="Generated company blueprint">
          <div className="mission-control__header">
            <span>{state.blueprint.status}</span>
            <h2>{state.blueprint.company_name}</h2>
            <p>{state.blueprint.tagline}</p>
          </div>

          <div className="blueprint-grid">
            <article>
              <span>Audience</span>
              <p>{state.blueprint.audience}</p>
            </article>
            <article>
              <span>Category</span>
              <p>{state.blueprint.category}</p>
            </article>
            <article className="blueprint-grid__wide">
              <span>Positioning</span>
              <p>{state.blueprint.positioning}</p>
            </article>
            <BlueprintList title="Starter Products" items={state.blueprint.starter_products} />
            <BlueprintList title="Storefront" items={state.blueprint.storefront_sections} />
            <BlueprintList title="Marketing" items={state.blueprint.marketing_plan} />
            <BlueprintList title="Launch Checklist" items={state.blueprint.launch_checklist} />
            <article className="blueprint-grid__wide">
              <span>Pricing Strategy</span>
              <p>{state.blueprint.pricing_strategy}</p>
            </article>
            <BlueprintList title="Agent Reasoning Log" items={state.blueprint.agent_log} wide />
          </div>
        </section>
      ) : null}
    </div>
  );
}

function BlueprintList({
  items,
  title,
  wide = false,
}: Readonly<{
  items: readonly string[];
  title: string;
  wide?: boolean;
}>) {
  return (
    <article className={wide ? "blueprint-grid__wide" : undefined}>
      <span>{title}</span>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </article>
  );
}
