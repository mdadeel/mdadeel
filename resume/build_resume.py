#!/usr/bin/env python3
"""Build Shahnawas Adeel's one page resume PDF with ReportLab."""

import os

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import (
    Spacer,
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Table,
    TableStyle,
)

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

INK = HexColor("#15181D")
MUTED = HexColor("#525A66")
ACCENT = HexColor("#1B3B5F")
LINK = HexColor("#1B3B5F")
RULE = HexColor("#C9CFD8")

PAGE_W, PAGE_H = A4
SIDE = 40
TOP = 30
BOTTOM = 30
CONTENT_W = PAGE_W - 2 * SIDE

# ---------------------------------------------------------------- fonts
pdfmetrics.registerFont(TTFont("Plex", os.path.join(FONT_DIR, "IBMPlexSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Plex-It", os.path.join(FONT_DIR, "IBMPlexSans-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Plex-Med", os.path.join(FONT_DIR, "IBMPlexSans-Medium.ttf")))
pdfmetrics.registerFont(TTFont("Plex-Semi", os.path.join(FONT_DIR, "IBMPlexSans-SemiBold.ttf")))
pdfmetrics.registerFont(TTFont("Plex-Bold", os.path.join(FONT_DIR, "IBMPlexSans-Bold.ttf")))
pdfmetrics.registerFontFamily("Plex", normal="Plex", bold="Plex-Bold", italic="Plex-It", boldItalic="Plex-Bold")


# ---------------------------------------------------------------- styles
def st(name, **kw):
    base = dict(fontName="Plex", fontSize=8.5, leading=10.75, textColor=INK, alignment=TA_LEFT, spaceBefore=0, spaceAfter=0)
    base.update(kw)
    return ParagraphStyle(name, **base)


S_BODY = st("body")
S_BULLET = st("bullet", leftIndent=9, bulletIndent=0, bulletFontName="Plex", bulletFontSize=6.9, bulletColor=ACCENT, spaceBefore=1.25)
S_PROJ = st("proj", fontSize=9.4, leading=11.2, fontName="Plex-Bold", textColor=INK)
S_PROJ_TAIL = st("projtail", fontSize=8.5, leading=10.9, textColor=MUTED)
S_LINKS = st("links", fontSize=7.9, leading=11.2)
S_SUMMARY = st("summary", fontSize=8.8, leading=11.9)


class SectionHeading(Flowable):
    """Small caps style section label with a hairline rule across the page."""

    def __init__(self, text, space_before=5.6, space_after=2.8):
        Flowable.__init__(self)
        self.text = text.upper()
        self.sb = space_before
        self.sa = space_after
        self.width = CONTENT_W
        self.height = 10

    def wrap(self, aw, ah):
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        c.setFillColor(ACCENT)
        c.setFont("Plex-Semi", 8.0)
        c._charSpace = 1.15
        c.drawString(0, 1.6, self.text)
        c._charSpace = 0
        label_w = c.stringWidth(self.text, "Plex-Semi", 8.0) + 1.15 * (len(self.text) - 1) + 1.5
        hair = HexColor("#A9B2BE")
        c.setStrokeColor(hair)
        c.setLineWidth(0.6)
        c.line(label_w + 8, 3.4, self.width, 3.4)

    def getSpaceBefore(self):
        return self.sb

    def getSpaceAfter(self):
        return self.sa


class Header(Flowable):
    H = 50.0

    def __init__(self):
        Flowable.__init__(self)
        self.width = CONTENT_W
        self.height = self.H

    def wrap(self, aw, ah):
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        c.setFillColor(INK)
        c.setFont("Plex-Bold", 20.5)
        c._charSpace = 1.5
        c.drawString(0, self.H - 15.5, "SHAHNAWAS ADEEL")
        c._charSpace = 0

        y = self.H - 28.0
        c.setFillColor(ACCENT)
        c.setFont("Plex-Semi", 9.0)
        c.drawString(0, y, "Full-Stack Software Engineer")
        role_w = c.stringWidth("Full-Stack Software Engineer", "Plex-Semi", 9.0)
        c.setFillColor(HexColor("#9AA3B0"))
        c.drawString(role_w + 7, y, "|")
        c.setFillColor(MUTED)
        c.setFont("Plex", 9.0)
        c.drawString(role_w + 15, y, "TypeScript, React, Node.js, PostgreSQL, Python")

        y = self.H - 41.0
        parts = [
            ("Chattogram, Bangladesh", None),
            ("+880 1533 970377", None),
            ("shahnawasadeel@gmail.com", "mailto:shahnawasadeel@gmail.com"),
            ("mdadeel.vercel.app", "https://mdadeel.vercel.app/"),
            ("github.com/mdadeel", "https://github.com/mdadeel"),
            ("linkedin.com/in/shahnawasadee1", "https://www.linkedin.com/in/shahnawasadee1/"),
        ]
        sep = "  |  "
        # shrink to fit the text column, never below 7.0pt
        size = 7.8
        while size > 7.0:
            w_total = sum(c.stringWidth(t, "Plex", size) for t, _ in parts) + c.stringWidth(sep, "Plex", size) * (len(parts) - 1)
            if w_total <= CONTENT_W:
                break
            size -= 0.1
        x = 0
        for text, url in parts:
            if x > 0:
                c.setFillColor(HexColor("#9AA3B0"))
                c.setFont("Plex", size)
                c.drawString(x, y, sep)
                x += c.stringWidth(sep, "Plex", size)
            c.setFillColor(LINK if url else MUTED)
            c.setFont("Plex", size)
            c.drawString(x, y, text)
            w = c.stringWidth(text, "Plex", size)
            if url:
                c.linkURL(url, (x, y - 1.8, x + w, y + 8.2), relative=0, thickness=0)
            x += w


def rule(space_before=5.0, space_after=0.0, color=RULE, width=0.8):
    class R(Flowable):
        def __init__(self):
            Flowable.__init__(self)
            self.width = CONTENT_W
            self.height = 0.6
            self.sb = space_before
            self.sa = space_after

        def wrap(self, aw, ah):
            return (self.width, self.height)

        def draw(self):
            self.canv.setStrokeColor(color)
            self.canv.setLineWidth(width)
            self.canv.line(0, 0, self.width, 0)

        def getSpaceBefore(self):
            return self.sb

        def getSpaceAfter(self):
            return self.sa

    return R()


def bullet(text, style=None):
    return Paragraph(text, style or S_BULLET, bulletText="\u25AA")


def project(title, tail, links):
    """Title on the left, live and code links flush right."""
    left = Paragraph(f"{title}", S_PROJ)
    right = Paragraph(links, S_LINKS)
    t = Table([[left, right]], colWidths=[CONTENT_W * 0.70, CONTENT_W * 0.30])
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ]
        )
    )
    out = [Spacer(1, 3.5), t]
    if tail:
        out.append(Paragraph(tail, S_PROJ_TAIL))
    return out


def role(left_html, right_html):
    t = Table([[Paragraph(left_html, S_BODY), Paragraph(right_html, S_PROJ_TAIL)]],
              colWidths=[CONTENT_W * 0.74, CONTENT_W * 0.26])
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ]
        )
    )
    return t


def link(url, text, bold=False):
    color = "#1B3B5F"
    face = "Plex-Semi" if bold else "Plex"
    return f'<link href="{url}" color="{color}"><font name="{face}">{text}</font></link>'


# ---------------------------------------------------------------- content
story = []
story.append(Header())
story.append(SectionHeading("Profile", space_before=5.0))

story.append(
    Paragraph(
        "Full-stack engineer who takes products from schema to shipped interface. Built and deployed Arbor, a "
        "codebase audit platform that parses real repositories; easyui, a 36-component React design system with a "
        "design token pipeline; and Preen, an MIT-licensed Linux desktop utility with six tagged releases. Works "
        "end to end in TypeScript and Python, including background job processing, packaging and release tooling.",
        S_SUMMARY,
    )
)

# ---- skills
story.append(SectionHeading("Technical Skills"))
skills = [
    ("Languages", "TypeScript, JavaScript (ES2024), Python 3, SQL, Bash"),
    ("Frontend", "React 19, Next.js (App Router), Vite, Tailwind CSS, Radix UI, TanStack Query, React Flow, Recharts"),
    ("Backend", "Node.js, tRPC v11, Express, BullMQ, Socket.IO, NextAuth, Firebase Auth, Stripe, REST APIs"),
    ("Data", "PostgreSQL 16, Prisma, MongoDB, Redis 7 (ioredis), schema design and migrations"),
    ("Tooling", "Docker and Compose, Playwright, Vitest, pnpm workspaces, GitHub Actions, Vercel, Cloudflare Workers, Git"),
    ("Systems", "Python 3, GTK 3, PyGObject, Debian packaging, AppImage, systemd, apt and flatpak"),
    ("Spoken", "Bangla (native), English (professional), Hindi (conversational)"),
]
rows = [[Paragraph(f"<font name='Plex-Semi' color='#1B3B5F'>{k}</font>", st("k", fontSize=8.2, leading=10.4)),
         Paragraph(v, st("v", fontSize=8.2, leading=10.4))] for k, v in skills]
tbl = Table(rows, colWidths=[54, CONTENT_W - 54])
tbl.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 1.1),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.1),
]))
story.append(tbl)

# ---- selected work
story.append(SectionHeading("Selected Projects"))

story.append(KeepTogether(project(
    "Arbor",
    "<font name='Plex-Med'>Codebase audit platform for GitHub repositories.</font> Parses a connected repo, "
    "draws its dependency graph, and scores six health dimensions with file and line evidence attached to every finding.",
    f"{link('https://arborgit.vercel.app/', 'Live site')} &nbsp;/&nbsp; {link('https://github.com/mdadeel/Arbor', 'Code')}",
)))
story.append(bullet(
    "Wrote the analysis layer in strict TypeScript: Babel AST parsing of JavaScript and TypeScript sources, import "
    "resolution into a React Flow module graph, cycle and hotspot detection, secret and env checks, and a "
    "schema-validated SARIF 2.1.0 export that uploads into GitHub Code Scanning."
))
story.append(bullet(
    "Modeled 30 Prisma models on PostgreSQL 16 across 11 migrations and exposed 19 tRPC v11 routers for projects, "
    "workspaces, billing, sharing and admin."
))
story.append(bullet(
    "Ran scans as BullMQ jobs on Redis 7: each job shallow clones into an isolated temp directory, streams progress, "
    "recovers stale jobs on worker restart, and deletes the clone when it finishes. Cache layer keeps scans "
    "under the per-workspace quota."
))
story.append(bullet(
    "Packaged self-hosting as one <font name='Plex-Med'>docker compose up</font>: bundled PostgreSQL and Redis, "
    "migration runner, health-checked Next.js app and a long-lived worker container. Added headless Chromium A4 "
    "audit PDFs and AES-256-GCM encryption for stored provider keys."
))
story.append(Paragraph(
    "<font name='Plex-Med'>Stack:</font> Next.js 15 App Router, React, tRPC, Prisma, PostgreSQL, Redis, BullMQ, "
    "Docker, Playwright, Vitest (68 test files). AGPL-3.0.",
    st("stack1", fontSize=8.2, leading=10.6, textColor=MUTED, spaceBefore=3.2, spaceAfter=1.0),
))

story.append(KeepTogether(project(
    "easyui",
    "<font name='Plex-Med'>React component library and design token pipeline.</font> Two published workspace "
    "packages and a live gallery of 44 examples, all themeable at runtime.",
    f"{link('https://easyui.mdadeel125.workers.dev/', 'Live site')} &nbsp;/&nbsp; {link('https://github.com/mdadeel/easyui', 'Code')}",
)))
story.append(bullet(
    "Split the system into <font name='Plex-Med'>@easyui/react</font> (36 accessible primitives, each with its own "
    "test file) and <font name='Plex-Med'>@easyui/tokens</font> (JSON design tokens compiled to CSS custom "
    "properties at build time), managed as a pnpm workspace monorepo."
))
story.append(bullet(
    "Built runtime theming through EasyUIProvider: accent, radius and font change over CSS variables with no rebuild, "
    "and preferences persist per device."
))
story.append(bullet(
    "Covered keyboard interaction, focus management and ARIA states with 44 Vitest and axe accessibility test files, "
    "then deployed the playground to Cloudflare Workers with prerendered routes, per-page metadata, structured data "
    "and a generated sitemap so pages stay crawlable without JavaScript."
))

story.append(KeepTogether(project(
    "Preen",
    "<font name='Plex-Med'>Linux system utility in Python 3 and GTK 3.</font> Manages APT, Flatpak and AppImage "
    "packages, previews cleanup sizes, inspects systemd services and archives user configuration.",
    f"{link('https://github.com/mdadeel/Preen', 'Code')} &nbsp;/&nbsp; {link('https://github.com/mdadeel/Preen/releases', 'Releases')}",
)))
story.append(bullet(
    "Maintain an 8.6k-line desktop application for Debian and Ubuntu family systems, including a simulate mode that "
    "previews destructive commands, a blocked list of essential packages on uninstall paths, and polkit "
    "authorization for privileged actions."
))
story.append(bullet(
    "Automated .deb, AppImage and wheel builds through shell packaging scripts, cut six tagged releases up to v0.7.1, "
    "and kept 17 test modules with fakes for apt, flatpak and systemd so the suite runs without root."
))
story.append(bullet(
    "Wrote the security, privacy, user and architecture documentation a distro package needs. MIT licensed, with an "
    "external fork in use."
))

story.append(KeepTogether(project(
    "e-TuitionBD",
    "<font name='Plex-Med'>Multi-role tuition marketplace for Bangladesh.</font> Student, tutor, organization and "
    "admin dashboards on one React codebase.",
    f"{link('https://e-tuitionhub.vercel.app/', 'Live site')} &nbsp;/&nbsp; {link('https://github.com/mdadeel/etuitionhub-frontend', 'Code')}",
)))
story.append(bullet(
    "Built role-scoped dashboards and application flows in React 19 and Vite, with Firebase Auth, Stripe checkout, "
    "Socket.IO messaging, Bangla and English locales, and Playwright end-to-end tests for payment approval and "
    "tutor onboarding."
))

# ---- experience
story.append(SectionHeading("Experience"))
story.append(role("<font name='Plex-Bold'>Freelance Software Engineer</font> &nbsp;<font color='#525A66'>| Client and product work</font>",
                  "Remote &nbsp;|&nbsp; 2025 - Present"))
story.append(bullet(
    "Shipped <font name='Plex-Med'>Metro Optics</font>, an eyewear storefront in React and Tailwind CSS, covering "
    "catalog filtering, product detail, cart and checkout screens across mobile and desktop breakpoints."
))
story.append(bullet(
    "Delivered the Ayash Tech corporate site in React with React Hook Form validation, deployed and tuned on Vercel."
))
story.append(bullet(
    "Own delivery end to end: scoping with the client, component architecture, responsive QA and post-launch fixes."
))

# ---- education
story.append(SectionHeading("Education and Training"))
story.append(role("<font name='Plex-Bold'>MERN Stack Web Development</font> &nbsp;<font color='#525A66'>| Programming Hero</font>",
                  "2025 - 2026"))
story.append(bullet(
    "Coursework in React, Node.js, Express and MongoDB; 500+ JavaScript, data structure and problem-solving "
    "exercises."
))



# ---------------------------------------------------------------- build
def page_bg(canv, doc):
    canv.saveState()
    canv.setFillColor(HexColor("#1B3B5F"))
    canv.rect(0, PAGE_H - 6, PAGE_W, 6, stroke=0, fill=1)
    canv.restoreState()


def build(path):
    doc = BaseDocTemplate(
        path,
        pagesize=A4,
        leftMargin=SIDE,
        rightMargin=SIDE,
        topMargin=TOP,
        bottomMargin=BOTTOM,
        title="Shahnawas Adeel | Full-Stack Software Engineer",
        author="Shahnawas Adeel",
        subject="Resume of Shahnawas Adeel, full-stack software engineer",
        creator="Shahnawas Adeel",
    )
    frame = Frame(SIDE, BOTTOM, CONTENT_W, PAGE_H - TOP - BOTTOM, id="body",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=page_bg)])
    doc.build(story)
    return path


if __name__ == "__main__":
    out = build(os.path.join(HERE, "Shahnawas-Adeel-Resume.pdf"))
    print("wrote", out)
