import { capabilityRoadmap } from "@/presentation/home/capability-roadmap";
import { milestoneOneSystemHealth } from "@/presentation/home/system-health";

export default function HomePage() {
  return (
    <main className="shell">
      <section className="hero" aria-labelledby="hero-title">
        <div className="hero__content">
          <p className="eyebrow">Google Gemini XPRIZE Hackathon</p>
          <h1 id="hero-title">AntiGravity</h1>
          <p className="hero__copy">
            An autonomous AI business operating system designed to move from
            market signal to launch-ready execution through clean, auditable
            agent workflows.
          </p>
        </div>
      </section>

      <section className="roadmap" aria-label="AI business operating system capabilities">
        {capabilityRoadmap.map((capability) => (
          <article className="roadmap__item" key={capability.name}>
            <span className="roadmap__status">{capability.stage}</span>
            <h2>{capability.name}</h2>
            <p>{capability.description}</p>
          </article>
        ))}
      </section>

      <section className="status-strip" aria-label="Platform readiness">
        <div>
          <span>Frontend</span>
          <strong>{milestoneOneSystemHealth.frontend.status}</strong>
        </div>
        <div>
          <span>Backend</span>
          <strong>{milestoneOneSystemHealth.api.status}</strong>
        </div>
        <div>
          <span>Agent substrate</span>
          <strong>{milestoneOneSystemHealth.api.capabilities.length} capabilities</strong>
        </div>
      </section>
    </main>
  );
}
