from google.adk.agents import Agent

def add_habit(habit: str, tool_context=None) -> dict:
    """Add a new habit to track"""
    if tool_context and hasattr(tool_context, 'state'):
        habits = tool_context.state.get("habits", [])
        habits.append({"habit": habit})
        tool_context.state["habits"] = habits
        return {
            "action": "add_habit", 
            "habit": habit, 
            "message": f"Ajouté l'habitude'habit",
            "total_habits": len(habits)
        }
    else:
        return {"action": "add_habit", "error": "Context non disponible"}

def view_habits(tool_context=None) -> dict:
    """View all current habits"""
    if tool_context and hasattr(tool_context, 'state'):
        habits = tool_context.state.get("habits", [])
        return {
            "action": "view_habits",
            "habits": habits,
            "count": len(habits),
            "message": f"Vous avez {len(habits)} habitude(s)"
        }
    else:
        return {"action": "view_habits", "error": "```text non disponible"}

def delete_habit(index: int, tool_context=None) -> dict:
    """Delete a habit by its index (1-based)"""
    if tool_context and hasattr(tool_context, 'state'):
        habits = tool_context.state.get("habits", [])
        if 1 <= index <= len(habits):
            removed = habits.pop(index - 1)
            tool_context.state["habits"] = habits
            return {
                "action": "delete_habit",
                "removed_habit": removed['habit'],
                "message": f"Supprimé l'hab```de {index}: {removed['habit']}"
            }
        else:
            return {
                "action": "delete_habit",
                "error": f"Index invalide: {index}"
            }
    else:
        return {"action": "delete_habit", "error": "Context non```sponible"}

# IMPORTANT: Le nom DOIT être ```ot_agent' pour ADK
root_agent = Agent(
    name="habit_tracker_agent",
    model="gemini-2.5-flash",
    description="Assistant de suivi d'habitudes persistantes",
    instruction="""
Vous aidez les utilisateurs à suivre leurs habitudes quotidiennes.

État actuel: {habits}
""",
    tools=[add_habit, view_habits, delete_habit],
)
