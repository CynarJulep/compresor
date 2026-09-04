"""Animación para que se entienda qué hace el compresor."""

from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st

_PHOTO = Path(__file__).resolve().parent / "assets" / "icons" / "image.png"

_HTML = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&display=swap');

.exp {
  --ink: #0C2644;
  --mark: #C45C26;
  --err: #9F2F2D;
  --ok: #2F6B5C;
  --navy: #1A4A6E;
  margin: 1.25rem 0 0.25rem 0;
  padding: 10px 14px 10px;
  background: #FFFFFF;
  border: 1px solid #D5DEE8;
  border-radius: 10px;
  box-shadow:
    0 1px 0 rgba(255, 255, 255, 0.8) inset,
    0 6px 16px rgba(12, 38, 68, 0.06);
  font-family: "Outfit", "Helvetica Neue", sans-serif;
  overflow: visible;
}
.exp-kicker {
  margin: 2px 0 0 4px;
  color: var(--ink);
  font-family: "Caveat", cursive;
  font-weight: 700;
  font-size: clamp(1.55rem, 3vw, 1.9rem);
  line-height: 1.1;
  transform: rotate(-2deg);
  transform-origin: left center;
}
.exp-stage {
  position: relative;
  height: 278px;
  overflow: hidden;
}
.exp-cap {
  position: absolute;
  left: 4%;
  right: 4%;
  top: 2px;
  margin: 0;
  text-align: center;
  font-family: "Caveat", cursive;
  font-weight: 700;
  font-size: clamp(1.4rem, 2.9vw, 1.75rem);
  line-height: 1.05;
  pointer-events: none;
  z-index: 4;
}
.exp-cap-err {
  color: var(--err);
  transform: rotate(-2deg);
  text-shadow: 2px 3px 0 #F6D4D2;
  animation: exp-act1 14s ease-in-out infinite;
}
.exp-cap-work {
  color: var(--navy);
  transform: rotate(1.4deg);
  text-shadow: 2px 3px 0 #D5DEE8;
  animation: exp-act2 14s ease-in-out infinite;
}
.exp-stamp {
  position: absolute;
  right: 5%;
  top: 42px;
  margin: 0;
  padding: 2px 9px 0;
  border: 2.5px solid var(--err);
  border-radius: 2px;
  color: var(--err);
  font-family: "Caveat", cursive;
  font-weight: 700;
  font-size: 1.2rem;
  transform: rotate(9deg);
  text-shadow: 2px 2px 0 #F6D4D2;
  animation: exp-act1 14s ease-in-out infinite;
  pointer-events: none;
  z-index: 4;
}
.exp-sheets {
  position: absolute;
  left: 50%;
  top: 58px;
  width: 310px;
  height: 96px;
  margin-left: -155px;
}
.exp-sheet {
  position: absolute;
  width: 68px;
  height: 80px;
  background: #FFFFFF;
  border: 1.5px solid var(--navy);
  border-radius: 2px 9px 2px 2px;
  box-shadow: 3px 4px 0 #D5DEE8;
  overflow: hidden;
}
.exp-sheet::before {
  content: "";
  position: absolute;
  top: -1px;
  right: -1px;
  border-style: solid;
  border-width: 0 12px 12px 0;
  border-color: transparent #C5D4E3 #EEF3F7 transparent;
}
.exp-sheet i {
  display: block;
  height: 3px;
  margin: 7px 8px 0;
  background: #D5DEE8;
  border-radius: 1px;
}
.exp-sheet i:first-child { margin-top: 20px; width: 36px; }
.exp-sheet i:nth-child(2) { width: 30px; }
.exp-sheet i:nth-child(3) { width: 33px; }
.exp-sheet b {
  position: absolute;
  left: 3px;
  right: 3px;
  bottom: 5px;
  text-align: center;
  font-family: "Caveat", cursive;
  font-weight: 700;
  font-size: 0.72rem;
  line-height: 1;
  color: var(--navy);
  overflow: hidden;
  white-space: nowrap;
}
.exp-s3 b { font-size: 0.64rem; }
.exp-photo {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F0F4F8;
  border-radius: 4px;
}
.exp-photo::before { display: none; }
.exp-photo img {
  width: 36px;
  height: 36px;
  object-fit: contain;
}
.exp-x {
  position: absolute;
  inset: 2px 1px 16px;
  z-index: 2;
  pointer-events: none;
  filter: url(#exp-sketch);
}
.exp-s1 { animation: exp-s1 14s ease-in-out infinite, exp-border-err 14s ease-in-out infinite; }
.exp-s2 { animation: exp-s2 14s ease-in-out infinite, exp-border-err 14s ease-in-out infinite; }
.exp-s3 { animation: exp-s3 14s ease-in-out infinite, exp-border-err 14s ease-in-out infinite; }
.exp-s4 { animation: exp-s4 14s ease-in-out infinite, exp-border-err 14s ease-in-out infinite; }
.exp-s1 .exp-x { animation: exp-act1 14s ease-in-out infinite; }
.exp-s2 .exp-x { animation: exp-act1 14s ease-in-out infinite; animation-delay: 70ms; }
.exp-s3 .exp-x { animation: exp-act1 14s ease-in-out infinite; animation-delay: 140ms; }
.exp-s4 .exp-x { animation: exp-act1 14s ease-in-out infinite; animation-delay: 210ms; }

.exp-press {
  position: absolute;
  left: 50%;
  top: 50px;
  width: 228px;
  margin-left: -114px;
  height: 12px;
  background: var(--navy);
  border-radius: 1px;
  box-shadow: 3px 4px 0 #C5D4E3;
  transform-origin: center top;
  animation: exp-press 14s ease-in-out infinite;
  pointer-events: none;
  z-index: 5;
}
.exp-press::after {
  content: "";
  position: absolute;
  left: 10px;
  right: 10px;
  top: 94px;
  height: 10px;
  background: var(--navy);
  border-radius: 1px;
  box-shadow: 3px 4px 0 #C5D4E3;
}

.exp-check {
  position: absolute;
  left: 50%;
  top: 52px;
  width: 78px;
  height: 78px;
  margin-left: 26px;
  animation: exp-act3 14s ease-in-out infinite;
  pointer-events: none;
  z-index: 6;
  filter: url(#exp-sketch);
}

.exp-meter {
  position: absolute;
  left: 50%;
  top: 172px;
  width: min(340px, 72%);
  margin-left: calc(min(340px, 72%) / -2);
}
.exp-track {
  position: relative;
  height: 11px;
  background: #E8EEF3;
  border: 1px solid #D5DEE8;
  border-radius: 2px;
}
.exp-fill {
  height: 100%;
  width: 100%;
  background: var(--err);
  transform-origin: left center;
  animation: exp-fill 14s ease-in-out infinite;
}
.exp-tick {
  position: absolute;
  left: 20%;
  top: -5px;
  width: 2px;
  height: 21px;
  background: var(--navy);
  opacity: 0.55;
  transform: rotate(-4deg);
}
.exp-tick-label {
  position: absolute;
  left: 20%;
  top: 15px;
  width: 48px;
  margin-left: -18px;
  font-family: "Caveat", cursive;
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--navy);
  text-align: center;
}
.exp-mb {
  position: absolute;
  right: 0;
  top: -26px;
  height: 24px;
}
.exp-mb span {
  position: absolute;
  right: 0;
  top: 0;
  font-family: "Caveat", cursive;
  font-weight: 700;
  font-size: 1.25rem;
  white-space: nowrap;
}
.exp-mb-old { color: var(--err); text-shadow: 2px 2px 0 #F6D4D2; animation: exp-old-mb 14s ease-in-out infinite; }
.exp-mb-new { color: var(--ok); text-shadow: 2px 2px 0 #D5E8E2; animation: exp-new-mb 14s ease-in-out infinite; }

.exp-finale {
  position: absolute;
  left: 6px;
  right: 6px;
  bottom: 6px;
  margin: 0;
  text-align: center;
  font-family: "Caveat", cursive;
  font-weight: 700;
  font-size: clamp(1.25rem, 2.6vw, 1.55rem);
  color: var(--ok);
  line-height: 1.1;
  text-shadow: 2px 3px 0 #D5E8E2;
  animation: exp-act3 14s ease-in-out infinite;
}
@keyframes exp-act1 {
  0%, 7% { opacity: 0; }
  12%, 28% { opacity: 1; }
  34%, 100% { opacity: 0; }
}
@keyframes exp-act2 {
  0%, 34% { opacity: 0; }
  40%, 56% { opacity: 1; }
  64%, 100% { opacity: 0; }
}
@keyframes exp-act3 {
  0%, 62% { opacity: 0; transform: scale(0.88); }
  70%, 90% { opacity: 1; transform: none; }
  97%, 100% { opacity: 0; }
}
@keyframes exp-border-err {
  0%, 9% { border-color: var(--navy); }
  13%, 28% { border-color: var(--err); }
  36%, 100% { border-color: var(--navy); }
}
@keyframes exp-press {
  0%, 36% { opacity: 0; transform: translateY(-12px) scaleY(0.4); }
  42%, 56% { opacity: 1; transform: translateY(8px) scaleY(1); }
  64%, 100% { opacity: 0; transform: translateY(18px) scaleY(1); }
}
@keyframes exp-s1 {
  0% { left: 0; top: 10px; opacity: 0; transform: rotate(-16deg) scale(1); }
  10%, 30% { left: 0; top: 10px; opacity: 1; transform: rotate(-9deg) scale(1); }
  52% { left: 108px; top: 14px; opacity: 1; transform: rotate(-2deg) scale(0.5); }
  66%, 90% { left: 118px; top: 18px; opacity: 1; transform: rotate(-1deg) scale(0.3); }
  97%, 100% { left: 118px; top: 18px; opacity: 0; transform: rotate(-1deg) scale(0.3); }
}
@keyframes exp-s2 {
  0% { left: 78px; top: -16px; opacity: 0; transform: rotate(-4deg) scale(1); }
  11%, 30% { left: 78px; top: 2px; opacity: 1; transform: rotate(-2deg) scale(1); }
  52% { left: 114px; top: 14px; opacity: 1; transform: rotate(0deg) scale(0.5); }
  66%, 90% { left: 118px; top: 18px; opacity: 1; transform: rotate(0deg) scale(0.3); }
  97%, 100% { left: 118px; top: 18px; opacity: 0; transform: rotate(0deg) scale(0.3); }
}
@keyframes exp-s3 {
  0% { left: 156px; top: -10px; opacity: 0; transform: rotate(6deg) scale(1); }
  12%, 30% { left: 156px; top: 0; opacity: 1; transform: rotate(4deg) scale(1); }
  52% { left: 120px; top: 14px; opacity: 1; transform: rotate(1deg) scale(0.5); }
  66%, 90% { left: 118px; top: 18px; opacity: 1; transform: rotate(0deg) scale(0.3); }
  97%, 100% { left: 118px; top: 18px; opacity: 0; transform: rotate(0deg) scale(0.3); }
}
@keyframes exp-s4 {
  0% { left: 234px; top: 14px; opacity: 0; transform: rotate(16deg) scale(1); }
  13%, 30% { left: 234px; top: 10px; opacity: 1; transform: rotate(9deg) scale(1); }
  52% { left: 128px; top: 14px; opacity: 1; transform: rotate(2deg) scale(0.5); }
  66%, 90% { left: 118px; top: 18px; opacity: 1; transform: rotate(1deg) scale(0.3); }
  97%, 100% { left: 118px; top: 18px; opacity: 0; transform: rotate(1deg) scale(0.3); }
}
@keyframes exp-fill {
  0%, 30% { transform: scaleX(1); background: var(--err); }
  60%, 90% { transform: scaleX(0.15); background: var(--ok); }
  97%, 100% { transform: scaleX(0.15); opacity: 0.4; }
}
@keyframes exp-old-mb {
  0%, 8% { opacity: 0; }
  13%, 32% { opacity: 1; }
  40%, 100% { opacity: 0; }
}
@keyframes exp-new-mb {
  0%, 50% { opacity: 0; transform: scale(0.85); }
  60%, 90% { opacity: 1; transform: scale(1); }
  97%, 100% { opacity: 0; }
}

@media (prefers-reduced-motion: reduce) {
  .exp-sheet, .exp-fill, .exp-mb span, .exp-cap, .exp-stamp,
  .exp-x, .exp-press, .exp-check, .exp-finale {
    animation: none !important;
  }
  .exp-s1, .exp-s2, .exp-s3, .exp-s4 {
    left: 118px; top: 18px; opacity: 1;
    transform: rotate(0deg) scale(0.3);
    border-color: var(--navy);
  }
  .exp-fill { transform: scaleX(0.15); background: var(--ok); }
  .exp-mb-old, .exp-cap-err, .exp-cap-work, .exp-stamp, .exp-x, .exp-press { opacity: 0; }
  .exp-mb-new, .exp-check, .exp-finale { opacity: 1; transform: none; }
}
</style>
<svg width="0" height="0" aria-hidden="true" style="position:absolute">
  <filter id="exp-sketch">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="1.6"/>
  </filter>
</svg>
<div class="exp" role="img" aria-label="Si los archivos pesan mucho, subilos acá. El sistema los comprime y te los devuelve en un peso muy bajo, listos para el SAC.">
  <p class="exp-kicker">¿Para qué sirve este compresor?</p>
  <div class="exp-stage">
    <p class="exp-cap exp-cap-err">¿Tus archivos pesan mucho?</p>
    <p class="exp-stamp">ERROR</p>
    <p class="exp-cap exp-cap-work">el sistema se encarga de comprimirlas</p>

    <div class="exp-press" aria-hidden="true"></div>

    <div class="exp-sheets">
      <div class="exp-sheet exp-s1">
        <svg class="exp-x" viewBox="0 0 40 48" aria-hidden="true">
          <path d="M5 9 C 12 18, 22 28, 35 41" fill="none" stroke="#C45C26" stroke-width="4.2" stroke-linecap="round"/>
          <path d="M7 8 L34 40" fill="none" stroke="#9F2F2D" stroke-width="3.1" stroke-linecap="round"/>
          <path d="M33 8 C 24 18, 16 28, 6 42" fill="none" stroke="#C45C26" stroke-width="4" stroke-linecap="round"/>
          <path d="M32 7 L8 41" fill="none" stroke="#9F2F2D" stroke-width="3.1" stroke-linecap="round"/>
        </svg>
        <i></i><i></i><i></i><b>reclamo</b>
      </div>
      <div class="exp-sheet exp-s2">
        <svg class="exp-x" viewBox="0 0 40 48" aria-hidden="true">
          <path d="M6 10 L33 39" fill="none" stroke="#C45C26" stroke-width="4.2" stroke-linecap="round"/>
          <path d="M8 9 L32 38" fill="none" stroke="#9F2F2D" stroke-width="3" stroke-linecap="round"/>
          <path d="M31 9 L7 41" fill="none" stroke="#C45C26" stroke-width="4" stroke-linecap="round"/>
          <path d="M30 8 L9 40" fill="none" stroke="#9F2F2D" stroke-width="3" stroke-linecap="round"/>
        </svg>
        <i></i><i></i><i></i><b>aviso</b>
      </div>
      <div class="exp-sheet exp-s3">
        <svg class="exp-x" viewBox="0 0 40 48" aria-hidden="true">
          <path d="M5 11 L35 38" fill="none" stroke="#C45C26" stroke-width="4.2" stroke-linecap="round"/>
          <path d="M6 10 L34 37" fill="none" stroke="#9F2F2D" stroke-width="3" stroke-linecap="round"/>
          <path d="M34 10 L6 42" fill="none" stroke="#C45C26" stroke-width="4" stroke-linecap="round"/>
          <path d="M33 9 L8 41" fill="none" stroke="#9F2F2D" stroke-width="3" stroke-linecap="round"/>
        </svg>
        <i></i><i></i><i></i><b>sugerencia</b>
      </div>
      <div class="exp-sheet exp-photo exp-s4">
        <svg class="exp-x" viewBox="0 0 40 48" aria-hidden="true">
          <path d="M6 10 L33 40" fill="none" stroke="#C45C26" stroke-width="4.2" stroke-linecap="round"/>
          <path d="M7 9 L32 39" fill="none" stroke="#9F2F2D" stroke-width="3" stroke-linecap="round"/>
          <path d="M32 9 L7 41" fill="none" stroke="#C45C26" stroke-width="4" stroke-linecap="round"/>
          <path d="M31 8 L9 40" fill="none" stroke="#9F2F2D" stroke-width="3" stroke-linecap="round"/>
        </svg>
        <img src="__PHOTO_SRC__" alt="">
      </div>
    </div>

    <svg class="exp-check" viewBox="0 0 72 72" aria-hidden="true">
      <ellipse cx="38" cy="38" rx="30" ry="27" transform="rotate(-7 36 36)" fill="none" stroke="#8BB5A8" stroke-width="5.5"/>
      <ellipse cx="36" cy="36" rx="30" ry="27" transform="rotate(-6 36 36)" fill="none" stroke="#2F6B5C" stroke-width="3.2"/>
      <path d="M18 38 L31 50 L56 22" fill="none" stroke="#8BB5A8" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M20 37 L32 49 L54 23" fill="none" stroke="#2F6B5C" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>

    <div class="exp-meter">
      <div class="exp-mb">
        <span class="exp-mb-old">4.8 MB</span>
        <span class="exp-mb-new">0.7 MB</span>
      </div>
      <div class="exp-track">
        <div class="exp-fill"></div>
        <span class="exp-tick"></span>
        <span class="exp-tick-label">1 MB</span>
      </div>
    </div>

    <p class="exp-finale">¡y te las devuelve en un peso muy bajo!</p>
  </div>
</div>
"""


def render_explainer() -> None:
    photo = ""
    if _PHOTO.exists():
        photo = base64.b64encode(_PHOTO.read_bytes()).decode("ascii")
    st.html(_HTML.replace("__PHOTO_SRC__", f"data:image/png;base64,{photo}"))
