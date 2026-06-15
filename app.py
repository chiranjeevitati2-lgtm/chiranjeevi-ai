# filename: app.py

from ollama import chat
from memory_utils import load_memory, save_memory, build_system_prompt

# Load memory and build system prompt once
memory = load_memory()
system_prompt = build_system_prompt(memory)

print(" Chiranjeevi AI")
print("\nCommands:")
print("remember ...")
print("show memories")
print("add task ...")
print("show tasks")
print("save note ...")
print("show notes")
print("exit")

while True:
    user = input("\nYou: ").strip()

    # Exit
    if user.lower() == "exit":
        print("\n👋 Goodbye Chiranjeevi!")
        break

    # Remember
    if user.lower().startswith("remember "):
        fact = user[9:].strip()
        if fact:
            memory.setdefault("memories", []).append(fact)
            save_memory(memory)
            print("\nAI: Memory saved.")
        else:
            print("\nAI: Please provide something to remember.")
        continue

    # Show Memories
    if user.lower() == "show memories":
        memories = memory.get("memories", [])
        if not memories:
            print("\nAI: No memories found.")
        else:
            print("\nMemories:")
            for i, m in enumerate(memories, 1):
                print(f"{i}. {m}")
        continue

    # Add Task
    if user.lower().startswith("add task "):
        task = user[9:].strip()
        if task:
            memory.setdefault("daily_tasks", []).append(task)
            save_memory(memory)
            print("\nAI: Task added.")
        else:
            print("\nAI: Please provide a task description.")
        continue

    # Show Tasks
    if user.lower() == "show tasks":
        tasks = memory.get("daily_tasks", [])
        if not tasks:
            print("\nAI: No tasks found.")
        else:
            print("\nYour Tasks:")
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")
        continue

    # Save Note
    if user.lower().startswith("save note "):
        note = user[10:].strip()
        if note:
            memory.setdefault("notes", []).append(note)
            save_memory(memory)
            print("\nAI: Note saved.")
        else:
            print("\nAI: Please provide a note to save.")
        continue

    # Show Notes
    if user.lower() == "show notes":
        notes = memory.get("notes", [])
        if not notes:
            print("\nAI: No notes found.")
        else:
            print("\nNotes:")
            for i, note in enumerate(notes, 1):
                print(f"{i}. {note}")
        continue

    # AI Chat
    response = chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user,
            },
        ],
    )

    print("\nAI:", response["message"]["content"])