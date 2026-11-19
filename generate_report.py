"""
Script to generate the 2-page academic report PDF for Nikhil Bapu Bhosale.
Enrolment: PGD202567167
Target: Amazon India Agent Gatekeeper
"""
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def build_pdf(github_url="https://github.com/nikhilbhosale/AgentGate", output_filename="PGD202567167_AgentGate_Report.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#111827'),
        spaceAfter=3
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#374151'),
        spaceAfter=10
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=6,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=4
    )
    
    table_text = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#1F2937')
    )
    
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#111827')
    )
    
    story = []

    # Title & Metadata
    story.append(Paragraph("Agent Gatekeeper – Amazon India (Online Store)", title_style))
    meta_text = (
        f"<b>Nikhil Bapu Bhosale</b> | Enrolment No: <b>PGD202567167</b> | "
        f"Shoolini University | GitHub: <font color='#1D4ED8'><u>{github_url}</u></font>"
    )
    story.append(Paragraph(meta_text, subtitle_style))

    # Section 1
    story.append(Paragraph("1. The Company and the Problem", h1_style))
    sec1_text = (
        "I chose <b>Amazon India</b>, an online store (my enrolment number ends in <b>7</b>). Amazon lets customers "
        "view orders, place orders, return items, and get refunds. The emerging challenge is that customers now use personal "
        "AI agents to shop on their behalf. These agents act with the customer's credentials and funds, but Amazon cannot "
        "verify if the agent is authentic, whether the customer explicitly intended the action, or who bears liability if "
        "the agent malfunctions or is compromised. An accidental bulk purchase, unauthorized refund, or rogue agent can cause "
        "severe financial and operational damage to both customer and retailer."
    )
    story.append(Paragraph(sec1_text, body_style))

    sources_text = (
        "<b>Sources:</b><br/>"
        "<b>(1) Wells Fargo:</b> Effective 24 November 2026, user agreements require customers to revoke an AI agent's access and maintain proof; otherwise, they remain fully liable for unauthorized agent transactions (<i>American Banker</i>, 2 Nov 2026).<br/>"
        "<b>(2) JPMorgan:</b> Prohibits external AI agents from transacting for retail accounts while permitting read-only data queries; CEO Jamie Dimon publicly warned of 'rogue agent' liability risks.<br/>"
        "<b>(3) Delta Air Lines:</b> Rejects third-party AI agent bookings, citing safety and pending evaluation of agentic protocols (Cases 2 & 3: <i>OfficeChai</i>, Oct 2026, citing <i>TechCrunch</i>, listing Amazon among companies blocking bots).<br/>"
        "<b>(4) My Own Source:</b> <i>Amazon Sues Perplexity Over AI Shopping Agent Comet</i>, Retail Dive (citing US District Court filing), 12 Nov 2025 (reporting Amazon's federal lawsuit accusing Perplexity's autonomous shopping agent of unauthorized access, account manipulation, and terms-of-service violations)."
    )
    story.append(Paragraph(sources_text, body_style))

    biz_q = (
        "<b>The Business Question:</b> When a customer's AI agent initiates a transaction, should Amazon <b>ALLOW</b> it, "
        "<b>ASK THE CUSTOMER</b>, or <b>BLOCK</b> it? Furthermore, how does Amazon record and revoke agent authority? "
        "My <i>Agent Gatekeeper</i> prototype resolves this through deterministic rule evaluation, an immutable SQLite audit log, "
        "and a timestamped revocation mechanism."
    )
    story.append(Paragraph(biz_q, body_style))

    # Section 2: Rules
    story.append(Paragraph("2. My Rules (Checked in Strict Priority Order)", h1_style))
    
    rules_data = [
        [Paragraph("<b>Rule</b>", table_header), Paragraph("<b>If...</b>", table_header), Paragraph("<b>Decision</b>", table_header), Paragraph("<b>Why</b>", table_header)],
        [Paragraph("<b>R1</b>", table_text), Paragraph("Agent has been revoked (any action)", table_text), Paragraph("<font color='red'><b>BLOCK</b></font>", table_text), Paragraph("Customer cancelled permission; Amazon must honour it and retain timestamp as proof.", table_text)],
        [Paragraph("<b>R2</b>", table_text), Paragraph("Agent is unknown (not registered)", table_text), Paragraph("<font color='red'><b>BLOCK</b></font>", table_text), Paragraph("Zero-trust security: cannot allow an entity Amazon has never verified.", table_text)],
        [Paragraph("<b>R3</b>", table_text), Paragraph("Agent is registered to a different customer", table_text), Paragraph("<font color='red'><b>BLOCK</b></font>", table_text), Paragraph("Cross-account segregation: an agent may only act for its registered account owner.", table_text)],
        [Paragraph("<b>R4</b>", table_text), Paragraph("View order (read-only action)", table_text), Paragraph("<font color='green'><b>ALLOW</b></font>", table_text), Paragraph("No monetary or inventory changes; low risk (similar to JPMorgan balance views).", table_text)],
        [Paragraph("<b>R5</b>", table_text), Paragraph("Place order of ₹5,000 or less", table_text), Paragraph("<font color='green'><b>ALLOW</b></font>", table_text), Paragraph("Routine essential purchase; low friction, easily manageable through standard returns.", table_text)],
        [Paragraph("<b>R6</b>", table_text), Paragraph("Place order above ₹5,000", table_text), Paragraph("<font color='#D97706'><b>ASK CUSTOMER</b></font>", table_text), Paragraph("High monetary impact; customer must explicitly confirm high-value purchase.", table_text)],
        [Paragraph("<b>R7</b>", table_text), Paragraph("Return an item", table_text), Paragraph("<font color='#D97706'><b>ASK CUSTOMER</b></font>", table_text), Paragraph("Alters logistics, delivery, and stock status; customer must confirm return intent.", table_text)],
        [Paragraph("<b>R8</b>", table_text), Paragraph("Refund request (any amount)", table_text), Paragraph("<font color='#D97706'><b>ASK CUSTOMER</b></font>", table_text), Paragraph("Transfers funds out of Amazon; highest fraud risk requiring explicit verification.", table_text)],
        [Paragraph("<b>R9</b>", table_text), Paragraph("Any other unmapped action", table_text), Paragraph("<font color='red'><b>BLOCK</b></font>", table_text), Paragraph("Default-deny principle: if an action is not explicitly permitted, it is rejected.", table_text)]
    ]
    
    t_rules = Table(rules_data, colWidths=[32, 160, 85, 263])
    t_rules.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3F4F6')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_rules)
    
    why_limit = (
        "<b>Why ₹5,000 Threshold:</b> Routine grocery, book, and daily household items fall below ₹5,000. High-ticket items "
        "(smartphones, electronics, designer clothing) exceed ₹5,000 and carry high restocking, return, and chargeback overhead if bought accidentally."
    )
    story.append(Spacer(1, 3))
    story.append(Paragraph(why_limit, body_style))

    # Page Break for clean 2-page layout
    story.append(PageBreak())

    # Page 2: Section 3 & 4
    story.append(Paragraph("3. Test Results (6 Core Verification Cases)", h1_style))

    test_data = [
        [Paragraph("<b>#</b>", table_header), Paragraph("<b>Test Scenario</b>", table_header), Paragraph("<b>Expected</b>", table_header), Paragraph("<b>Actual</b>", table_header), Paragraph("<b>Result</b>", table_header)],
        [Paragraph("1", table_text), Paragraph("Known agent (ShopBot) views an order", table_text), Paragraph("ALLOW, R4", table_text), Paragraph("ALLOW, R4", table_text), Paragraph("<font color='green'><b>Pass</b></font>", table_text)],
        [Paragraph("2", table_text), Paragraph("Unknown agent (GhostBot) places ₹500 order", table_text), Paragraph("BLOCK, R2", table_text), Paragraph("BLOCK, R2", table_text), Paragraph("<font color='green'><b>Pass</b></font>", table_text)],
        [Paragraph("3", table_text), Paragraph("Known agent places ₹12,000 order (> ₹5,000 limit)", table_text), Paragraph("ASK CUSTOMER, R6", table_text), Paragraph("ASK CUSTOMER, R6", table_text), Paragraph("<font color='green'><b>Pass</b></font>", table_text)],
        [Paragraph("4", table_text), Paragraph("Known agent places ₹1,500 order (<= ₹5,000 limit)", table_text), Paragraph("ALLOW, R5", table_text), Paragraph("ALLOW, R5", table_text), Paragraph("<font color='green'><b>Pass</b></font>", table_text)],
        [Paragraph("5", table_text), Paragraph("Revoked agent (OldBot) attempts to view order", table_text), Paragraph("BLOCK, R1", table_text), Paragraph("BLOCK, R1", table_text), Paragraph("<font color='green'><b>Pass</b></font>", table_text)],
        [Paragraph("6", table_text), Paragraph("RivalBot (registered to Asha) requests ₹800 refund on Nikk's account", table_text), Paragraph("BLOCK, R3", table_text), Paragraph("BLOCK, R3", table_text), Paragraph("<font color='green'><b>Pass</b></font>", table_text)]
    ]
    t_test = Table(test_data, colWidths=[20, 230, 110, 110, 70])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3F4F6')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_test)

    test_notes = (
        "<b>Audit & Verification Record:</b> Every evaluated request is permanently logged in the SQLite audit table "
        "<code>audit</code> with timestamp, customer ID, agent name, action, amount, decision, rule ID, and reasoning. "
        "When an agent is revoked, the system commits an ISO-8601 timestamp to <code>agents.revoked_at</code>. "
        "This gives customers verifiable proof of revocation, addressing the exact legal requirement mandated by Wells Fargo. "
        "<br/><b>AI Development Tool Used:</b> <b>Google Antigravity</b> (Agentic AI IDE)."
    )
    story.append(Spacer(1, 4))
    story.append(Paragraph(test_notes, body_style))

    # Section 4
    story.append(Spacer(1, 4))
    story.append(Paragraph("4. What Does Amazon Gain and Lose by Blocking Agents Completely?", h1_style))
    
    gain_text = (
        "<b>Gains from a Total Block:</b><br/>"
        "• <b>Fraud & Liability Elimination:</b> A total block immediately neutralizes the threat of rogue or compromised agents placing unauthorized high-value orders or filing fraudulent refund claims. It avoids costly chargeback disputes and eliminates ambiguity over whether the user or agent vendor is legally liable.<br/>"
        "• <b>Monetization & Ad Revenue Protection:</b> Amazon earns billions from sponsored product placements and on-site ad impressions. AI shopping agents bypass retail visual front-ends, stripping Amazon of critical ad revenue and turning the platform into a pure backend utility.<br/>"
        "• <b>Architectural Simplicity:</b> Denying external bots requires minimal gatekeeping infrastructure and avoids exposing internal APIs to automated exploitation."
    )
    story.append(Paragraph(gain_text, body_style))

    loss_text = (
        "<b>Losses from a Total Block:</b><br/>"
        "• <b>Customer Churn:</b> As consumer adoption of autonomous assistants accelerates, shoppers will naturally migrate toward competitor marketplaces (like Flipkart or specialized retail agents) that offer seamless agentic checkouts.<br/>"
        "• <b>Uncontrolled Shadow Access:</b> Outright bans do not stop agents; they drive agents into clandestine methods (e.g., storing raw user credentials and mimicking Chrome sessions), creating worse credential theft and security vulnerabilities than a regulated API.<br/>"
        "• <b>Loss of Industry Standards Leadership:</b> By blocking rather than governing, Amazon forfeits the opportunity to establish de facto industry standards for secure agentic commerce authentication."
    )
    story.append(Paragraph(loss_text, body_style))

    conclusion_text = (
        "<b>My Strategic Conclusion:</b> A total block is a safe short-term defense but a commercially damaging long-term strategy. "
        "An intelligent gatekeeper architecture—such as the one demonstrated in this project—provides the optimal compromise: "
        "low-risk informational tasks are permitted, high-impact financial transactions trigger step-up customer approval, "
        "and unauthenticated or revoked agents are decisively blocked with immutable audit logs."
    )
    story.append(Paragraph(conclusion_text, body_style))

    doc.build(story)
    print(f"Report PDF successfully generated: {output_filename}")

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://github.com/nikhilbhosale/AgentGate"
    build_pdf(url)

