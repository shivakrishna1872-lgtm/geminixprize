"use client";

import { useMemo, useState } from "react";
import type { CompanyBlueprint } from "@antigravity/contracts";

type CartLine = Readonly<{
  name: string;
  priceUsd: number;
  quantity: number;
}>;

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
  const [cart, setCart] = useState<readonly CartLine[]>([]);
  const [checkoutEmail, setCheckoutEmail] = useState("");
  const [checkoutStatus, setCheckoutStatus] = useState<"idle" | "confirmed">("idle");

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
    setCart([]);
    setCheckoutStatus("idle");
    setState({ status: "ready", blueprint });
  }

  function addToCart(name: string, priceUsd: number) {
    setCart((currentCart) => {
      const existing = currentCart.find((item) => item.name === name);
      if (existing) {
        return currentCart.map((item) =>
          item.name === name ? { ...item, quantity: item.quantity + 1 } : item,
        );
      }
      return [...currentCart, { name, priceUsd, quantity: 1 }];
    });
  }

  function confirmLocalCheckout() {
    if (cart.length === 0 || !checkoutEmail.includes("@")) {
      setState({ status: "error", message: "Add a product and enter an email before checkout." });
      return;
    }

    setCheckoutStatus("confirmed");
  }

  const cartTotal = cart.reduce((total, item) => total + item.priceUsd * item.quantity, 0);

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

      {state.status === "authenticating" || state.status === "generating" ? (
        <BuildPipeline currentStatus={state.status} />
      ) : null}

      {state.status === "ready" ? (
        <>
          <MissionControl blueprint={state.blueprint} />
          <section className="storefront-preview" aria-label="Generated storefront preview">
            <div className="storefront-preview__hero">
              <span>/{state.blueprint.storefront_slug}</span>
              <h2>{state.blueprint.company_name}</h2>
              <p>{state.blueprint.positioning}</p>
              <a href="#checkout-preview">Shop launch products</a>
            </div>

            <div className="product-grid">
              {state.blueprint.product_catalog.map((product) => (
                <article className="product-card" key={product.name}>
                  <div className="product-card__image" aria-hidden="true">
                    <span />
                  </div>
                  <span>{product.inventory_status}</span>
                  <h3>{product.name}</h3>
                  <p>{product.description}</p>
                  <strong>${product.price_usd.toFixed(2)}</strong>
                  <small>{product.product_angle}</small>
                  <button
                    onClick={() => addToCart(product.name, product.price_usd)}
                    type="button"
                  >
                    Add to cart
                  </button>
                </article>
              ))}
            </div>

            <section className="checkout-panel" id="checkout-preview" aria-label="Local checkout preview">
              <div>
                <span>{state.blueprint.checkout_mode}</span>
                <h3>Checkout</h3>
                <p>
                  This checkout is functional in local test mode. Connect Stripe or
                  Commerce Layer credentials to switch from local orders to live payments.
                </p>
              </div>
              <div className="cart-box">
                {cart.length === 0 ? (
                  <p>Your cart is empty.</p>
                ) : (
                  <ul>
                    {cart.map((item) => (
                      <li key={item.name}>
                        <span>
                          {item.quantity} x {item.name}
                        </span>
                        <strong>${(item.priceUsd * item.quantity).toFixed(2)}</strong>
                      </li>
                    ))}
                  </ul>
                )}
                <div className="cart-total">
                  <span>Total</span>
                  <strong>${cartTotal.toFixed(2)}</strong>
                </div>
                <input
                  aria-label="Checkout email"
                  onChange={(event) => setCheckoutEmail(event.target.value)}
                  placeholder="customer@example.com"
                  type="email"
                  value={checkoutEmail}
                />
                <button onClick={confirmLocalCheckout} type="button">
                  Place local test order
                </button>
                {checkoutStatus === "confirmed" ? (
                  <p className="checkout-confirmation">
                    Test order confirmed. Provider credentials are required before charging a card.
                  </p>
                ) : null}
              </div>
            </section>
          </section>
        </>
      ) : null}
    </div>
  );
}

function BuildPipeline({
  currentStatus,
}: Readonly<{
  currentStatus: "authenticating" | "generating";
}>) {
  const stages = [
    "Authenticate founder",
    "Research market",
    "Discover launch products",
    "Price catalog",
    "Build storefront",
    "Prepare checkout",
  ];

  return (
    <section className="build-pipeline" aria-label="Storefront build progress">
      <span>{currentStatus === "authenticating" ? "Securing session" : "Building storefront"}</span>
      <ol>
        {stages.map((stage, index) => (
          <li key={stage} className={currentStatus === "generating" || index === 0 ? "is-active" : undefined}>
            {stage}
          </li>
        ))}
      </ol>
    </section>
  );
}

function MissionControl({ blueprint }: Readonly<{ blueprint: CompanyBlueprint }>) {
  return (
    <section className="mission-control" aria-label="Generated company blueprint">
      <div className="mission-control__header">
        <span>{blueprint.status}</span>
        <h2>{blueprint.company_name}</h2>
        <p>{blueprint.tagline}</p>
      </div>

      <div className="blueprint-grid">
        <article>
          <span>Audience</span>
          <p>{blueprint.audience}</p>
        </article>
        <article>
          <span>Category</span>
          <p>{blueprint.category}</p>
        </article>
        <article className="blueprint-grid__wide">
          <span>Positioning</span>
          <p>{blueprint.positioning}</p>
        </article>
        <BlueprintList title="Starter Products" items={blueprint.starter_products} />
        <BlueprintList title="Storefront" items={blueprint.storefront_sections} />
        <BlueprintList title="Marketing" items={blueprint.marketing_plan} />
        <BlueprintList title="Launch Checklist" items={blueprint.launch_checklist} />
        <article className="blueprint-grid__wide">
          <span>Pricing Strategy</span>
          <p>{blueprint.pricing_strategy}</p>
        </article>
        <BlueprintList title="Agent Reasoning Log" items={blueprint.agent_log} wide />
      </div>
    </section>
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
