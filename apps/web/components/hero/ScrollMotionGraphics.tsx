'use client';

import React, { useEffect, useRef, useState } from "react";

export function ScrollMotionGraphics() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const targetScrollY = useRef(0);
  const currentScrollY = useRef(0);
  const lastRenderTime = useRef(0);
  const animationFrameId = useRef<number | null>(null);
  
  // Track window size for canvas resizing
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  useEffect(() => {
    if (typeof window === "undefined") return;

    const handleResize = () => {
      setDimensions({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };
    
    const handleScroll = () => {
      targetScrollY.current = window.scrollY;
    };

    window.addEventListener("resize", handleResize);
    window.addEventListener("scroll", handleScroll);
    
    // Set initial size
    handleResize();

    return () => {
      window.removeEventListener("resize", handleResize);
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || dimensions.width === 0 || dimensions.height === 0) return;
    
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    
    canvas.width = dimensions.width;
    canvas.height = dimensions.height;
    
    // Setup rendering loop at exactly 30 FPS
    const fpsInterval = 1000 / 30; // ~33.33ms
    lastRenderTime.current = performance.now();

    const drawPlanet = (ctx: CanvasRenderingContext2D, cx: number, cy: number, r: number, scrollOffset: number) => {
      // Draw Planet base circle (pixelated style)
      ctx.fillStyle = "#16213E";
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.fill();
      
      // Draw atmospheric glow
      ctx.strokeStyle = "rgba(124, 58, 237, 0.3)";
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.arc(cx, cy, r + 4, 0, Math.PI * 2);
      ctx.stroke();

      // Mask to clip surface features inside the planet circle
      ctx.save();
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.clip();

      // Draw continent bands moving with scroll (simulating planet rotation)
      ctx.fillStyle = "#7C3AED"; // purple continents
      const continentShift = (scrollOffset * 0.15) % (r * 4);
      
      // Continent 1
      ctx.fillRect(cx - r*2 + continentShift, cy - r/2, r, r/3);
      ctx.fillRect(cx - r*2 + continentShift + 10, cy - r/2 - 10, r - 20, 10);
      
      // Continent 2
      ctx.fillRect(cx - r*4 + continentShift + r*2.5, cy + r/4, r*1.2, r/4);
      ctx.fillRect(cx - r*4 + continentShift + r*2.5 - 15, cy + r/4 - 5, r*0.8, 5);

      // Continent 3 (wrap-around helper)
      ctx.fillRect(cx - r*2 + continentShift - r*3, cy - r/2, r, r/3);
      ctx.fillRect(cx - r*2 + continentShift - r*3 + 10, cy - r/2 - 10, r - 20, 10);

      ctx.restore();

      // Draw pixelated grid overlay on planet for high tech look
      ctx.strokeStyle = "rgba(10, 10, 15, 0.4)";
      ctx.lineWidth = 1;
      for (let i = cx - r; i < cx + r; i += 8) {
        ctx.beginPath();
        ctx.moveTo(i, cy - r);
        ctx.lineTo(i, cy + r);
        ctx.stroke();
      }
      for (let j = cy - r; j < cy + r; j += 8) {
        ctx.beginPath();
        ctx.moveTo(cx - r, j);
        ctx.lineTo(cx + r, j);
        ctx.stroke();
      }
    };

    const drawSatellite = (ctx: CanvasRenderingContext2D, cx: number, cy: number, prg: number) => {
      // Orbit Path
      const rx = 180;
      const ry = 40;
      const angle = prg * Math.PI * 2;
      
      // Satellite coordinates
      const sx = cx + Math.cos(angle) * rx;
      const sy = cy + Math.sin(angle) * ry;

      // Draw orbit line behind planet
      ctx.strokeStyle = "rgba(6, 182, 212, 0.1)";
      ctx.lineWidth = 2;
      ctx.save();
      ctx.beginPath();
      ctx.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();

      // Draw Satellite body
      ctx.fillStyle = "#EC4899"; // pink body
      ctx.fillRect(sx - 6, sy - 6, 12, 12);
      
      // Solar Panels
      ctx.fillStyle = "#06B6D4"; // cyan solar panels
      ctx.fillRect(sx - 18, sy - 3, 10, 6);
      ctx.fillRect(sx + 8, sy - 3, 10, 6);

      // Antennas & Blinking LED
      ctx.strokeStyle = "#FFFFFF";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(sx, sy - 6);
      ctx.lineTo(sx - 3, sy - 14);
      ctx.stroke();

      const ledOn = Math.floor(performance.now() / 250) % 2 === 0;
      if (ledOn) {
        ctx.fillStyle = "#EF4444"; // red blinking light
        ctx.beginPath();
        ctx.arc(sx - 3, sy - 14, 3, 0, Math.PI * 2);
        ctx.fill();
      }
    };

    const render = (timestamp: number) => {
      animationFrameId.current = requestAnimationFrame(render);

      const elapsed = timestamp - lastRenderTime.current;

      // Restrict rendering logic strictly to 30 frames per second
      if (elapsed >= fpsInterval) {
        // Adjust last render time
        lastRenderTime.current = timestamp - (elapsed % fpsInterval);

        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Smooth scroll interpolation (LERP)
        currentScrollY.current += (targetScrollY.current - currentScrollY.current) * 0.12;

        const scrollVal = currentScrollY.current;
        const maxScroll = Math.max(document.body.scrollHeight - window.innerHeight, 1);
        const scrollProgress = scrollVal / maxScroll;

        // Draw parallax starfield
        ctx.fillStyle = "rgba(255, 255, 255, 0.8)";
        const numStars = 40;
        for (let i = 0; i < numStars; i++) {
          const x = (i * 12345) % canvas.width;
          // Slowly move stars based on scroll
          const speed = (i % 3 === 0) ? 0.08 : (i % 2 === 0) ? 0.04 : 0.02;
          const y = ((i * 54321) - scrollVal * speed) % canvas.height;
          
          const adjustedY = y < 0 ? y + canvas.height : y;
          const starSize = (i % 4 === 0) ? 2 : 1;
          
          ctx.fillRect(x, adjustedY, starSize, starSize);
        }

        // Draw rotating pixel planet in top-right area
        const planetX = canvas.width * 0.8;
        const planetY = 160 + scrollVal * 0.1; // Slow vertical drift
        drawPlanet(ctx, planetX, planetY, 50, scrollVal);

        // Draw orbiting satellite linked to scroll position
        const satProgress = (scrollVal * 0.001) % 1;
        drawSatellite(ctx, planetX, planetY, satProgress);

        // Draw a rocket that lifts off when the user scrolls down
        const rocketX = canvas.width * 0.15;
        // Rocket rises up from below the screen as you scroll down
        const rocketY = canvas.height - 40 - (scrollProgress * canvas.height * 0.8);
        
        if (rocketY > -100 && rocketY < canvas.height + 100) {
          // Flame effect (flickering at 30 fps)
          const flameHeight = 12 + Math.sin(timestamp * 0.05) * 6;
          ctx.fillStyle = "#F59E0B"; // orange flame
          ctx.beginPath();
          ctx.moveTo(rocketX - 4, rocketY + 20);
          ctx.lineTo(rocketX, rocketY + 20 + flameHeight);
          ctx.lineTo(rocketX + 4, rocketY + 20);
          ctx.fill();

          // Rocket Body
          ctx.fillStyle = "#E2E8F0"; // grey body
          ctx.fillRect(rocketX - 6, rocketY - 20, 12, 40);

          // Rocket Nosecone
          ctx.fillStyle = "#EF4444"; // red tip
          ctx.beginPath();
          ctx.moveTo(rocketX - 6, rocketY - 20);
          ctx.lineTo(rocketX, rocketY - 32);
          ctx.lineTo(rocketX + 6, rocketY - 20);
          ctx.fill();

          // Rocket Fins
          ctx.fillStyle = "#7C3AED";
          ctx.fillRect(rocketX - 10, rocketY + 10, 4, 10);
          ctx.fillRect(rocketX + 6, rocketY + 10, 4, 10);
        }

        // Draw tech grid lines at bottom
        ctx.strokeStyle = "rgba(6, 182, 212, 0.04)";
        ctx.lineWidth = 1;
        const gridOffset = (scrollVal * 0.2) % 40;
        for (let y = canvas.height - 150; y < canvas.height; y += 20) {
          ctx.beginPath();
          ctx.moveTo(0, y + (scrollVal * 0.05) % 20);
          ctx.lineTo(canvas.width, y + (scrollVal * 0.05) % 20);
          ctx.stroke();
        }
      }
    };

    animationFrameId.current = requestAnimationFrame(render);

    return () => {
      if (animationFrameId.current) {
        cancelAnimationFrame(animationFrameId.current);
      }
    };
  }, [dimensions]);

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 w-full h-full pointer-events-none z-0"
      style={{ mixBlendMode: "screen" }}
    />
  );
}
