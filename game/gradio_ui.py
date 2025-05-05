import gradio as gr
from game.game_engine import GameEngine
from game.character import characters
from game.weapon import weapons
from game.mansion import rooms

# Initialize GameEngine
engine = GameEngine(num_players=2)

# Game turn state
global_state = {"turn": 0}

def end_turn():
    global_state["turn"] = (global_state["turn"] + 1) % 2
    return global_state["turn"]

def move(player_id, room):
    if player_id != global_state["turn"]:
        return "⛔ Not your turn"
    player = engine.players[player_id]
    if not player.active:
        return f"Player {player_id} has been eliminated."
    if room not in rooms:
        return "Invalid room."
    player.current_room = room
    return f"✅ Player {player_id} moved to {room}."

def suggest(player_id, character, weapon):
    if player_id != global_state["turn"]:
        return "⛔ Not your turn"
    player = engine.players[player_id]
    if not player.active:
        return f"Player {player_id} is eliminated."
    if not player.current_room:
        return "❗ You must move to a room before suggesting."

    suggestion = {
        "character": character,
        "weapon": weapon,
        "room": player.current_room
    }

    result = engine.refute_suggestion(player_id, suggestion)

    # Only update turn if suggestion was valid
    global_state["turn"] = (global_state["turn"] + 1) % 2

    if result["refuter_id"] is not None:
        return (
            f"🕵️ Player {player_id} suggested: {character}, {weapon}, {player.current_room}\n"
            f"✅ Player {result['refuter_id']} refuted with card: {result['shown_card']}"
        )
    else:
        return (
            f"🕵️ Player {player_id} suggested: {character}, {weapon}, {player.current_room}\n"
            f"❌ No one could refute the suggestion. Maybe it's the truth?"
        )

def accuse(player_id, character, weapon, room):
    if player_id != global_state["turn"]:
        return "⛔ Not your turn"
    player = engine.players[player_id]
    if not player.active:
        return f"Player {player_id} is already eliminated."
    accusation = {
        "character": character,
        "weapon": weapon,
        "room": room
    }
    if accusation == engine.solution:
        return f"🎉 Player {player_id} WINS! Correct accusation: {engine.solution}"
    else:
        player.active = False
        global_state["turn"] = (global_state["turn"] + 1) % 2
        return f"❌ Wrong accusation. Player {player_id} is eliminated."

def show_notebook(player_id):
    player = engine.players[player_id]
    result = []
    result.append("Characters:")
    result += [f"  {c}: {player.notebook.get(c, 'Unknown')}" for c in characters]
    result.append("")
    result.append("Weapons:")
    result += [f"  {w}: {player.notebook.get(w, 'Unknown')}" for w in weapons]
    result.append("")
    result.append("Rooms:")
    result += [f"  {r}: {player.notebook.get(r, 'Unknown')}" for r in rooms]
    return "\n".join(result)

def show_hand(player_id):
    player = engine.players[player_id]
    result = []
    result.append("Characters:")
    result += [f"  - {c}" for c in player.hand if c in characters]
    result.append("")
    result.append("Weapons:")
    result += [f"  - {w}" for w in player.hand if w in weapons]
    result.append("")
    result.append("Rooms:")
    result += [f"  - {r}" for r in player.hand if r in rooms]
    return "\n".join(result)

with gr.Blocks() as demo:
    gr.Markdown("# 🎲 Cluedo - GameEngine UI")

    with gr.Row():
        with gr.Column():
            gr.Markdown("## 👤 Player 0")
            p0_room = gr.Dropdown(rooms, label="Move to Room")
            p0_move_btn = gr.Button("Move")
            p0_move_out = gr.Textbox(label="Move Result")

            p0_char = gr.Dropdown(characters, label="Character")
            p0_weap = gr.Dropdown(weapons, label="Weapon")
            p0_suggest_btn = gr.Button("Suggest")
            p0_suggest_out = gr.Textbox(label="Suggestion Result")

            p0_accuse_char = gr.Dropdown(characters, label="Character (Accuse)")
            p0_accuse_weap = gr.Dropdown(weapons, label="Weapon (Accuse)")
            p0_accuse_room = gr.Dropdown(rooms, label="Room (Accuse)")
            p0_accuse_btn = gr.Button("Accuse")
            p0_accuse_out = gr.Textbox(label="Accuse Result")

            p0_notebook_btn = gr.Button("Show Notebook")
            p0_notebook_out = gr.Textbox(lines=10, label="Notebook")

            p0_hand_btn = gr.Button("Show My Cards")
            p0_hand_out = gr.Textbox(lines=10, label="My Cards")

        with gr.Column():
            gr.Markdown("## 👤 Player 1")
            p1_room = gr.Dropdown(rooms, label="Move to Room")
            p1_move_btn = gr.Button("Move")
            p1_move_out = gr.Textbox(label="Move Result")

            p1_char = gr.Dropdown(characters, label="Character")
            p1_weap = gr.Dropdown(weapons, label="Weapon")
            p1_suggest_btn = gr.Button("Suggest")
            p1_suggest_out = gr.Textbox(label="Suggestion Result")

            p1_accuse_char = gr.Dropdown(characters, label="Character (Accuse)")
            p1_accuse_weap = gr.Dropdown(weapons, label="Weapon (Accuse)")
            p1_accuse_room = gr.Dropdown(rooms, label="Room (Accuse)")
            p1_accuse_btn = gr.Button("Accuse")
            p1_accuse_out = gr.Textbox(label="Accuse Result")

            p1_notebook_btn = gr.Button("Show Notebook")
            p1_notebook_out = gr.Textbox(lines=10, label="Notebook")

            p1_hand_btn = gr.Button("Show My Cards")
            p1_hand_out = gr.Textbox(lines=10, label="My Cards")

    # Bind buttons
    p0_move_btn.click(fn=lambda r: move(0, r), inputs=p0_room, outputs=p0_move_out)
    p1_move_btn.click(fn=lambda r: move(1, r), inputs=p1_room, outputs=p1_move_out)

    p0_suggest_btn.click(fn=lambda c, w: suggest(0, c, w), inputs=[p0_char, p0_weap], outputs=p0_suggest_out)
    p1_suggest_btn.click(fn=lambda c, w: suggest(1, c, w), inputs=[p1_char, p1_weap], outputs=p1_suggest_out)

    p0_accuse_btn.click(fn=lambda c, w, r: accuse(0, c, w, r), inputs=[p0_accuse_char, p0_accuse_weap, p0_accuse_room], outputs=p0_accuse_out)
    p1_accuse_btn.click(fn=lambda c, w, r: accuse(1, c, w, r), inputs=[p1_accuse_char, p1_accuse_weap, p1_accuse_room], outputs=p1_accuse_out)

    p0_notebook_btn.click(fn=lambda: show_notebook(0), outputs=p0_notebook_out)
    p1_notebook_btn.click(fn=lambda: show_notebook(1), outputs=p1_notebook_out)

    p0_hand_btn.click(fn=lambda: show_hand(0), outputs=p0_hand_out)
    p1_hand_btn.click(fn=lambda: show_hand(1), outputs=p1_hand_out)

demo.launch()