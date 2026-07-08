# Accessibility Fixer Script for Arena.Twin templates
import bs4
import re

def fix_html_accessibility():
    filepath = "templates/index.html"
    with open(filepath, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = bs4.BeautifulSoup(html_content, "html.parser")

    # 1. Ensure HTML root has lang="en" (Done via base.html, but let's check)
    # 2. Add aria-hidden="true" to all <i> tags
    icons = soup.find_all("i")
    print(f"Auditing {len(icons)} FontAwesome icon tags...")
    for icon in icons:
        if not icon.has_attr("aria-hidden"):
            icon["aria-hidden"] = "true"

    # 3. Add descriptive aria-label to icon-only buttons
    buttons_map = {
        "btn-toggle-sim-panel": "Show simulation control panel",
        "btn-toggle-mute": "Toggle voice assistant narration",
        "langDropdown": "Change dashboard display language",
        "btn-close-sim": "Close simulation control panel",
        "chat-voice-btn": "Speak question using voice input",
        "chat-send-btn": "Send message to assistant",
        "btn-speak-announcement": "Read public announcement aloud",
        "btn-reset-operations": "Reset emergency command center",
        "btn-trigger-emergency": "Trigger simulation safety alert",
        "btn-sim-crowd-inc": "Increase crowd volume by 20 percent",
        "btn-sim-crowd-dec": "Decrease crowd volume by 20 percent",
        "btn-sim-temp-inc": "Increase climate temperature by 3 degrees",
        "btn-sim-temp-dec": "Decrease climate temperature by 3 degrees",
        "btn-sim-power-cut": "Trigger power grid failure",
        "btn-lc-search": "Initialize lost child search grid",
        "btn-acc-generate": "Generate step-free transit route",
        "btn-queue-apply": "Balance concession stand registers",
        "brand-logo-btn": "Arena Twin Home logo link"
    }

    for bid, label in buttons_map.items():
        btn = soup.find(id=bid)
        if btn:
            btn["aria-label"] = label
            # Also ensure it has a tab index for keyboard accessibility
            if not btn.has_attr("tabindex"):
                btn["tabindex"] = "0"

    # 4. Add aria-label to inputs and select tags
    inputs_map = {
        "lc-name": "Missing spectator name input field",
        "lc-shirt": "Missing spectator shirt color input field",
        "lc-last-seen": "Select last seen location of missing spectator",
        "acc-source": "Select transit departure parking or hub location",
        "acc-dest": "Select transit arrival stands tier location",
        "chat-input-text": "Type query or question for the fan chatbot helper"
    }

    for iid, label in inputs_map.items():
        inp = soup.find(id=iid)
        if inp:
            inp["aria-label"] = label
            if not inp.has_attr("tabindex"):
                inp["tabindex"] = "0"

    # 5. Auditing remaining buttons inside button lists
    # Weather scenario buttons: .btn-sim-weather
    weather_buttons = soup.find_all("button", class_=re.compile("btn-sim-weather"))
    for btn in weather_buttons:
        weather_val = btn.get("data-weather", "Clear")
        btn["aria-label"] = f"Set weather scenario to {weather_val}"
        btn["tabindex"] = "0"

    # Accessibility type buttons: .btn-acc-type
    acc_type_buttons = soup.find_all("button", class_=re.compile("btn-acc-type"))
    for btn in acc_type_buttons:
        acc_val = btn.get("data-type", "wheelchair")
        btn["aria-label"] = f"Set transit routing guidelines for {acc_val.replace('_', ' ')}"
        btn["tabindex"] = "0"

    # Navigation pills: .nav-shortcut
    nav_links = soup.find_all("a", class_=re.compile("nav-shortcut"))
    for link in nav_links:
        view_val = link.get("data-view", "overview")
        link["aria-label"] = f"Switch dashboard panel view to {view_val}"
        link["tabindex"] = "0"

    # Write back the corrected HTML template
    # We use format = False or default output to maintain formatting and Jinja tags
    output_html = str(soup)
    
    # Restore Jinja2 block variables formatting (Jinja blocks sometimes get slightly escaped or modified by bs4 if formatted, but raw soup str keeps them intact)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(output_html)

    print("[OK] Templates Accessibility attributes injected successfully.")

if __name__ == "__main__":
    fix_html_accessibility()
