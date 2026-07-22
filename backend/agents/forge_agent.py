"""
Forge Agent — Engineer
======================
Forge simulates website creation via Duda MCP (mock mode).  It generates:
  • Full site architecture (pages with content and structure)
  • Hero copy based on the brand identity
  • A live-style URL in the antigravity.store namespace

In production this would call the Duda API to scaffold and publish a real
site.  In mock mode (no API key) it returns a realistic site structure that
the frontend renders as a completed website.
"""

import os
import sys
import re
import uuid

# ---------------------------------------------------------------------------
# Path setup — reach shared/types/models.py two directories above agents/
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from backend.models.schemas import (
    AgentId,
    AgentStatus,
    Business,
)
from base_agent import BaseAgent


class ForgeAgent(BaseAgent):
    """
    Forge is the Engineer agent.  It translates brand identity and product
    strategy into a live website structure.
    """

    def __init__(self, business: Business):
        super().__init__(AgentId.FORGE, business)

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    @staticmethod
    def _slugify(text: str) -> str:
        slug = text.lower()
        slug = re.sub(r"[^a-z0-9]+", "-", slug)
        return slug.strip("-")

    def _get_brand_name(self) -> str:
        if self.business.brand:
            return self.business.brand.name
        # Derive from prompt as fallback
        words = self.business.prompt.split()
        return words[0].capitalize() if words else "Store"

    def _get_niche(self) -> str:
        if self.business.blueprint:
            return self.business.blueprint.niche
        return self.business.prompt

    # -----------------------------------------------------------------------
    # Main entry point
    # -----------------------------------------------------------------------

    async def run(self) -> dict:
        """
        Execute Forge's website generation workflow:
          1. Design site architecture and page structure
          2. Generate hero copy
          3. Apply brand theme to all pages
          4. Publish (mock) and return URL
        """
        brand_name = self._get_brand_name()
        brand_name_slug = self._slugify(brand_name)
        niche = self._get_niche()

        tagline = ""
        primary_color = "#1A1A2E"
        accent_color = "#3B82F6"
        font_heading = "Space Grotesk"
        font_body = "Inter"
        if self.business.brand:
            tagline = self.business.brand.tagline
            primary_color = self.business.brand.primary_color
            accent_color = self.business.brand.accent_color
            font_heading = self.business.brand.font_heading
            font_body = self.business.brand.font_body

        target_audience = ""
        value_proposition = ""
        if self.business.blueprint:
            target_audience = self.business.blueprint.target_audience
            value_proposition = self.business.blueprint.value_proposition

        website_url = f"https://{brand_name_slug}.antigravity.store"
        site_id = f"site_{uuid.uuid4().hex[:12]}"

        # -- Step 1: Site architecture --------------------------------------
        await self._set_status(AgentStatus.WORKING, task="Designing site architecture...", progress=15)
        await self._emit_log("🏗️  Designing site architecture...")
        await self._emit_log(f"📐 Planning pages for {brand_name}...")

        site_structure = await self.think_json(
            prompt=f"""You are a senior e-commerce web architect and UX designer.

Brand name: {brand_name}
Brand tagline: {tagline}
Business niche: {niche}
Target audience: {target_audience}
Value proposition: {value_proposition}
Website URL: {website_url}

Design a complete 4-page e-commerce website structure. Return JSON:
{{
  "pages": [
    {{
      "id": "home",
      "title": "Home",
      "slug": "/",
      "meta_description": "SEO-optimized meta description under 160 chars",
      "sections": [
        {{
          "type": "hero",
          "heading": "Powerful hero headline (max 8 words)",
          "subheading": "Compelling subheading sentence",
          "cta_primary": "Primary button text",
          "cta_secondary": "Secondary button text"
        }},
        {{
          "type": "features",
          "heading": "Section heading",
          "items": [
            {{"icon": "⚡", "title": "Feature title", "description": "Feature description"}},
            {{"icon": "🎯", "title": "Feature title", "description": "Feature description"}},
            {{"icon": "🌟", "title": "Feature title", "description": "Feature description"}}
          ]
        }},
        {{
          "type": "testimonials",
          "heading": "Section heading",
          "items": [
            {{"quote": "Customer testimonial text", "author": "Customer Name", "role": "Verified Buyer"}},
            {{"quote": "Customer testimonial text", "author": "Customer Name", "role": "Verified Buyer"}},
            {{"quote": "Customer testimonial text", "author": "Customer Name", "role": "Verified Buyer"}}
          ]
        }},
        {{
          "type": "cta_banner",
          "heading": "Final conversion CTA heading",
          "subheading": "Supporting text",
          "cta": "Button text"
        }}
      ]
    }},
    {{
      "id": "products",
      "title": "Shop",
      "slug": "/shop",
      "meta_description": "SEO-optimized meta description under 160 chars",
      "sections": [
        {{
          "type": "product_grid",
          "heading": "Products section heading",
          "filter_categories": ["All", "Category1", "Category2"]
        }},
        {{
          "type": "guarantee",
          "items": ["Guarantee item 1", "Guarantee item 2", "Guarantee item 3"]
        }}
      ]
    }},
    {{
      "id": "about",
      "title": "About",
      "slug": "/about",
      "meta_description": "SEO-optimized meta description under 160 chars",
      "sections": [
        {{
          "type": "story",
          "heading": "Our story heading",
          "body": "2-3 paragraph brand story that connects emotionally with the target audience"
        }},
        {{
          "type": "values",
          "heading": "Our values heading",
          "items": [
            {{"title": "Value 1", "description": "Description"}},
            {{"title": "Value 2", "description": "Description"}},
            {{"title": "Value 3", "description": "Description"}}
          ]
        }}
      ]
    }},
    {{
      "id": "contact",
      "title": "Contact",
      "slug": "/contact",
      "meta_description": "SEO-optimized meta description under 160 chars",
      "sections": [
        {{
          "type": "contact_form",
          "heading": "Get in Touch",
          "subheading": "We respond within 24 hours",
          "fields": ["name", "email", "subject", "message"]
        }},
        {{
          "type": "contact_info",
          "email": "hello@{brand_name_slug}.com",
          "support_hours": "Monday–Friday, 9am–6pm EST",
          "response_time": "Within 24 hours"
        }}
      ]
    }}
  ]
}}

Make all copy specific to {brand_name} and the {niche} niche. Do NOT use placeholder text.""",
            task_description="Generating site page structure and content",
        )

        pages = site_structure.get("pages", [])
        await self._emit_log(f"✅ Site architecture planned: {len(pages)} pages")
        for page in pages:
            await self._emit_log(f"   📄 {page.get('title', 'Page')} — {page.get('slug', '/')}")

        # -- Step 2: Hero copy ----------------------------------------------
        await self._set_status(AgentStatus.WORKING, task="Generating page layouts...", progress=40)
        await self._emit_log("✍️  Generating hero copy...")

        hero_data = await self.think_json(
            prompt=f"""You are a conversion-focused copywriter for e-commerce.

Brand name: {brand_name}
Tagline: {tagline}
Niche: {niche}
Target audience: {target_audience}
Value proposition: {value_proposition}

Write high-converting above-the-fold copy. Return JSON:
{{
  "hero_headline": "Bold headline — 6-9 words, emotional hook",
  "hero_subheadline": "1-2 sentence that expands on the headline and mentions the value proposition",
  "hero_cta_primary": "Primary CTA button text (action-oriented, 2-4 words)",
  "hero_cta_secondary": "Secondary CTA button text",
  "social_proof_line": "Trust signal line (e.g., 'Loved by 12,000+ customers')",
  "announcement_bar": "Top-of-page announcement text (promo or brand statement)"
}}

Make it impossible to ignore. Use power words, urgency, and specificity.""",
            task_description="Generating hero copy",
        )

        await self._emit_log(f"📣 Hero headline: \"{hero_data.get('hero_headline', '')}\"")
        await self._emit_log(f"🎯 CTA: \"{hero_data.get('hero_cta_primary', '')}\"")

        # -- Step 3: Apply brand theme -------------------------------------
        await self._set_status(AgentStatus.WORKING, task="Applying brand theme...", progress=70)
        await self._emit_log("🎨 Applying brand theme across all pages...")
        await self._emit_log(f"   Primary color: {primary_color}")
        await self._emit_log(f"   Heading font: {font_heading}")
        await self._emit_log(f"   Body font: {font_body}")
        await self._emit_log("   Generating responsive layouts...")
        await self._emit_log("   Optimizing for mobile-first design...")

        theme_config = {
            "primary_color": primary_color,
            "accent_color": accent_color,
            "font_heading": font_heading,
            "font_body": font_body,
            "border_radius": "12px",
            "button_style": "rounded",
            "layout": "full-width",
            "dark_mode": True,
        }

        # -- Step 4: Publish ------------------------------------------------
        await self._set_status(AgentStatus.WORKING, task="Publishing store...", progress=95)
        await self._emit_log("🚀 Publishing store to antigravity.store CDN...")
        await self._emit_log(f"🌐 Site live at: {website_url}")
        await self._emit_log("⚡ Edge caching enabled across 47 regions")
        await self._emit_log("🔒 SSL certificate provisioned")
        await self._emit_log("✅ Forge website creation complete!")

        # Inject hero data into home page
        if pages and len(pages) > 0:
            for section in pages[0].get("sections", []):
                if section.get("type") == "hero":
                    section["heading"] = hero_data.get("hero_headline", section.get("heading", ""))
                    section["subheading"] = hero_data.get("hero_subheadline", section.get("subheading", ""))
                    section["cta_primary"] = hero_data.get("hero_cta_primary", section.get("cta_primary", "Shop Now"))
                    section["cta_secondary"] = hero_data.get("hero_cta_secondary", section.get("cta_secondary", "Learn More"))
                    section["social_proof_line"] = hero_data.get("social_proof_line", "")
                    break

        return {
            "website_url": website_url,
            "site_id": site_id,
            "pages": pages,
            "hero_copy": hero_data,
            "theme_config": theme_config,
            "brand_name_slug": brand_name_slug,
            "announcement_bar": hero_data.get("announcement_bar", ""),
            "deployment": {
                "status": "live",
                "cdn": "antigravity-edge",
                "ssl": True,
                "regions": 47,
                "platform": "duda-mock",
            },
        }
