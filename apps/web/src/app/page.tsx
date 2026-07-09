import { agents, businessTypes, pricingPlans } from "@/presentation/home/landing-content";
import { CompanyGenerator } from "@/presentation/home/company-generator";

export default function HomePage() {
  return (
    <main>
      <header className="site-header" aria-label="Primary">
        <a className="brand-mark" href="#top" aria-label="MadeThis home">
          <span className="brand-mark__glyph" aria-hidden="true" />
          MadeThis
        </a>
        <nav className="nav-links" aria-label="Landing page sections">
          <a href="#agents">Agents</a>
          <a href="#process">Process</a>
          <a href="#pricing">Pricing</a>
          <a href="#launch">Launch</a>
        </nav>
        <a className="nav-action" href="#launch">
          Start free
        </a>
      </header>

      <section className="hero-world" id="top" aria-labelledby="hero-title">
        <div className="sky-layer sky-layer--back" aria-hidden="true" />
        <div className="sky-layer sky-layer--front" aria-hidden="true" />
        <div className="hero-world__copy">
          <p className="eyebrow">Google Gemini XPRIZE Hackathon</p>
          <h1 id="hero-title">Build a business that runs itself</h1>
          <p>
            MadeThis gives founders a Gemini-powered AI company team that
            researches markets, designs brands, creates products, launches
            storefronts, and operates the business from one prompt.
          </p>
          <CompanyGenerator />
        </div>

        <div className="pixel-stage" aria-hidden="true">
          <div className="sun" />
          <div className="cloud cloud--one" />
          <div className="cloud cloud--two" />
          <div className="mountains mountains--back" />
          <div className="mountains mountains--front" />
          <div className="world-track world-track--slow">
            <span className="building building--lab" />
            <span className="building building--shop" />
            <span className="building building--tower" />
            <span className="building building--studio" />
            <span className="building building--lab" />
            <span className="building building--shop" />
          </div>
          <div className="world-track world-track--fast">
            <span className="tree" />
            <span className="founder founder--one" />
            <span className="bot bot--one" />
            <span className="tree tree--gold" />
            <span className="founder founder--two" />
            <span className="bot bot--two" />
            <span className="tree" />
          </div>
          <div className="ground" />
        </div>
      </section>

      <section className="business-rail" aria-label="Business types">
        <div className="rail-track">
          {[...businessTypes, ...businessTypes].map((business, index) => (
            <article className="business-chip" key={`${business.label}-${index}`}>
              <span className={`pixel-icon pixel-icon--${business.icon}`} aria-hidden="true" />
              {business.label}
            </article>
          ))}
        </div>
      </section>

      <section className="stat-band" aria-label="Platform stats">
        <article>
          <strong>9</strong>
          <span>specialized agents</span>
        </article>
        <article>
          <strong>1</strong>
          <span>founder prompt</span>
        </article>
        <article>
          <strong>24/7</strong>
          <span>mission control</span>
        </article>
      </section>

      <section className="section-shell agent-section" id="agents" aria-labelledby="agents-title">
        <div className="section-heading">
          <p className="eyebrow">Introducing your AI company team</p>
          <h2 id="agents-title">Every department, orchestrated by Gemini</h2>
          <p>
            Each agent owns a narrow responsibility and reports progress through
            auditable execution logs, cost controls, retries, and safety policy checks.
          </p>
        </div>
        <div className="agent-grid">
          {agents.map((agent) => (
            <article className="agent-card" key={agent.name}>
              <span className="agent-avatar" aria-hidden="true" />
              <span>{agent.role}</span>
              <h3>{agent.name}</h3>
              <p>{agent.output}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="side-by-side" id="process" aria-labelledby="process-title">
        <div>
          <p className="eyebrow">Three steps to launch</p>
          <h2 id="process-title">From idea to operating company</h2>
        </div>
        <ol className="process-list">
          <li>
            <strong>Describe the business</strong>
            <span>Submit the market, audience, offer, and constraints.</span>
          </li>
          <li>
            <strong>Approve the operating plan</strong>
            <span>The CEO agent assigns research, brand, product, store, and marketing work.</span>
          </li>
          <li>
            <strong>Watch mission control</strong>
            <span>Track reasoning, execution logs, storefront status, revenue, and business health.</span>
          </li>
        </ol>
      </section>

      <section className="feature-band" aria-labelledby="features-title">
        <div className="section-heading">
          <p className="eyebrow">What MadeThis handles</p>
          <h2 id="features-title">A real business stack, wired for autonomy</h2>
        </div>
        <div className="feature-grid">
          {[
            "Market research",
            "Brand identity",
            "Product assets",
            "Storefront generation",
            "Checkout configuration",
            "SEO and ads",
            "Customer support",
            "Finance telemetry",
          ].map((feature) => (
            <article key={feature}>
              <span className="feature-spark" aria-hidden="true" />
              <h3>{feature}</h3>
              <p>Built behind clean service interfaces for MCP providers and Google Cloud services.</p>
            </article>
          ))}
        </div>
      </section>

      <section className="pricing" id="pricing" aria-labelledby="pricing-title">
        <div className="section-heading">
          <p className="eyebrow">Cost to automate your business</p>
          <h2 id="pricing-title">Plans for every stage of company building</h2>
        </div>
        <div className="pricing-grid">
          {pricingPlans.map((plan) => (
            <article className={plan.featured ? "pricing-card pricing-card--featured" : "pricing-card"} key={plan.name}>
              <span>{plan.name}</span>
              <strong>{plan.price}</strong>
              <p>{plan.summary}</p>
              <ul>
                {plan.highlights.map((highlight) => (
                  <li key={highlight}>{highlight}</li>
                ))}
              </ul>
              <a href="#launch">Start for free</a>
            </article>
          ))}
        </div>
        <p className="pricing-note">
          Enterprise AI business operations start at $5,000/mo with a free automation audit.
        </p>
      </section>

      <section className="final-cta" id="launch" aria-labelledby="launch-title">
        <div className="mini-city" aria-hidden="true">
          <span />
          <span />
          <span />
          <span />
        </div>
        <p className="eyebrow">Start your business in minutes</p>
        <h2 id="launch-title">Describe the company. Let the agents build the launch path.</h2>
        <a href="#top">Open mission console</a>
      </section>
    </main>
  );
}
