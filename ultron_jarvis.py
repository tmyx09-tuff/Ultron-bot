"""
Ultron + Jarvis Robot Brain (Educational AI Robot Prototype)
----------------------------------------------------------------
This script gives you:
- Jarvis = mission controller
- Ultron = brain/planner/executor
- RobotHardware = simulation layer for robot actions
- Safety rules = blocks unsafe commands
- Fallback AI logic = works without API

This is a safe educational prototype for robot behavior,
not a real weapon system or dangerous autonomous control.
"""

import os
import json
import subprocess
import time
from typing import Dict, List, Any, Optional


# ------------------------------------------------------------
# 1) SAFETY POLICY
# ------------------------------------------------------------
class SafetyPolicy:
    SAFE_COMMANDS = {
        "ls", "pwd", "echo", "date", "whoami", "python --version"
    }

    @staticmethod
    def is_allowed_command(command: str) -> bool:
        cmd = command.strip()
        if not cmd:
            return False
        if cmd in SafetyPolicy.SAFE_COMMANDS:
            return True
        if cmd.startswith("echo "):
            return True
        if cmd.startswith("python "):
            return True
        return False

    @staticmethod
    def is_allowed_action(action: str) -> bool:
        allowed = {
            "move", "speak", "scan", "grab", "release",
            "photo", "battery", "status", "final", "command"
        }
        return action in allowed


# ------------------------------------------------------------
# 2) ROBOT HARDWARE
# ------------------------------------------------------------
class RobotHardware:
    """Replace these with real motors, sensors, and drivers."""

    def move(self, direction: str = "forward", speed: float = 0.6) -> str:
        return f"Robot moved {direction} at speed {speed}"

    def speak(self, text: str = "I am ready") -> str:
        print(f"[SPEAK] {text}")
        return f"Spoke: {text}"

    def scan_environment(self) -> Dict[str, Any]:
        return {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "obstacles": ["chair", "desk", "box"],
            "lights_on": True,
            "people_detected": 1
        }

    def grab_object(self, object_name: str = "box") -> str:
        return f"Grabbed object: {object_name}"

    def release_object(self) -> str:
        return "Released object"

    def take_photo(self) -> str:
        return "Captured a photo"

    def get_battery(self) -> float:
        return 88.7

    def run_command(self, command: str) -> str:
        if not SafetyPolicy.is_allowed_command(command):
            return "Command blocked by safety policy."

        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout.strip() or result.stderr.strip() or "Command executed successfully."
            return output
        except Exception as e:
            return f"Command execution error: {e}"


# ------------------------------------------------------------
# 3) MEMORY
# ------------------------------------------------------------
class Memory:
    def __init__(self):
        self.history: List[str] = []
        self.tasks: List[str] = []

    def add_history(self, item: str):
        self.history.append(item)

    def add_task(self, goal: str):
        self.tasks.append(goal)

    def recent(self, limit: int = 5) -> List[str]:
        return self.history[-limit:]


# ------------------------------------------------------------
# 4) ULTRON BRAIN
# ------------------------------------------------------------
class UltronBrain:
    def __init__(self, hardware: RobotHardware, memory: Optional[Memory] = None):
        self.hardware = hardware
        self.memory = memory or Memory()
        self.skills = {
            "move": self._skill_move,
            "speak": self._skill_speak,
            "scan": self._skill_scan,
            "grab": self._skill_grab,
            "release": self._skill_release,
            "photo": self._skill_photo,
            "battery": self._skill_battery,
            "command": self._skill_command,
            "status": self._skill_status,
            "final": self._skill_final,
        }

    def _skill_move(self, direction: str = "forward", speed: float = 0.6):
        return self.hardware.move(direction, speed)

    def _skill_speak(self, text: str = "I am ready"):
        return self.hardware.speak(text)

    def _skill_scan(self):
        return self.hardware.scan_environment()

    def _skill_grab(self, object_name: str = "box"):
        return self.hardware.grab_object(object_name)

    def _skill_release(self):
        return self.hardware.release_object()

    def _skill_photo(self):
        return self.hardware.take_photo()

    def _skill_battery(self):
        return self.hardware.get_battery()

    def _skill_command(self, command: str = "echo hello"):
        return self.hardware.run_command(command)

    def _skill_status(self):
        return {
            "task_count": len(self.memory.tasks),
            "recent_actions": self.memory.recent(5),
            "available_skills": list(self.skills.keys())
        }

    def _skill_final(self, answer: str = "Task completed."):
        return answer

    def _fallback_plan(self, goal: str) -> Dict[str, Any]:
        """
        Local rule-based planner. Works without any AI API.
        """
        g = goal.lower()

        if "move" in g or "walk" in g or "go" in g:
            direction = "forward"
            if "left" in g:
                direction = "left"
            elif "right" in g:
                direction = "right"
            elif "back" in g:
                direction = "backward"
            return {"action": "move", "args": {"direction": direction, "speed": 0.6}}

        if "say" in g or "talk" in g or "speak" in g or "hello" in g:
            return {"action": "speak", "args": {"text": f"Understood. I will {goal}."}}

        if "scan" in g or "look" in g or "inspect" in g:
            return {"action": "scan", "args": {}}

        if "photo" in g or "camera" in g or "vision" in g:
            return {"action": "photo", "args": {}}

        if "battery" in g or "charge" in g:
            return {"action": "battery", "args": {}}

        if "grab" in g:
            obj = "box"
            if "cup" in g:
                obj = "cup"
            elif "book" in g:
                obj = "book"
            return {"action": "grab", "args": {"object_name": obj}}

        if "release" in g:
            return {"action": "release", "args": {}}

        if "status" in g or "info" in g:
            return {"action": "status", "args": {}}

        if "run" in g or "command" in g:
            return {"action": "command", "args": {"command": "echo command executed"}}

        return {
            "action": "final",
            "args": {"answer": f"Task completed: {goal}"}
        }

    def _llm_plan(self, goal: str) -> Dict[str, Any]:
        """
        Optional AI integration:
        If OPENAI_API_KEY exists, try OpenAI.
        Otherwise use fallback planner.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return self._fallback_plan(goal)

        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

            prompt = f"""
You are Ultron, a robot brain.
Available actions:
- move(direction, speed)
- speak(text)
- scan()
- grab(object_name)
- release()
- photo()
- battery()
- command(command)
- status()
- final(answer)

User goal:
{goal}

Return JSON only:
{{
  "action": "skill_name",
  "args": {{ ... }}
}}
"""

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Return only valid JSON with the next robot action."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )

            text = response.choices[0].message.content
            return json.loads(text)

        except Exception as e:
            print(f"[AI ERROR] {e}")
            return self._fallback_plan(goal)

    def run_goal(self, goal: str) -> str:
        self.memory.add_task(goal)
        self.memory.add_history(f"Goal received: {goal}")

        for step in range(10):
            plan = self._llm_plan(goal)
            action = plan.get("action", "final")

            if action not in self.skills:
                plan = self._fallback_plan(goal)
                action = plan.get("action", "final")

            if not SafetyPolicy.is_allowed_action(action):
                self.memory.add_history(f"Blocked unsafe action: {action}")
                return f"Action blocked: {action}"

            args = plan.get("args", {})
            skill = self.skills.get(action)

            if skill is None:
                return f"Unknown action: {action}"

            try:
                result = skill(**args)
                self.memory.add_history(f"Step {step + 1}: {action} -> {result}")
                print(f"[ULTRON] {action} -> {result}")

                if action in ["speak", "scan", "battery", "photo", "release", "status"]:
                    return str(result)

                if action == "final":
                    return str(result)

            except TypeError as e:
                return f"Invalid arguments for {action}: {e}"

        return "Goal processing timed out."


# ------------------------------------------------------------
# 5) JARVIS CONTROLLER
# ------------------------------------------------------------
class JarvisController:
    def __init__(self, brain: UltronBrain):
        self.brain = brain

    def issue_goal(self, goal: str) -> str:
        print(f"\n[JARVIS] Received goal: {goal}")
        return self.brain.run_goal(goal)


# ------------------------------------------------------------
# 6) MAIN PROGRAM
# ------------------------------------------------------------
if __name__ == "__main__":
    hardware = RobotHardware()
    brain = UltronBrain(hardware)
    jarvis = JarvisController(brain)

    print("=== ULTRON + JARVIS DEMO ===")
    print("Commands you can try:")
    print(" - Move forward")
    print(" - Say hello to everyone")
    print(" - Scan the room")
    print(" - Take a photo")
    print(" - Check battery")
    print(" - Grab the box")
    print(" - Status")
    print(" - exit")
    print()

    while True:
        user_input = input("Jarvis> ").strip()
        if user_input.lower() in ["exit", "quit", "stop"]:
            print("Jarvis is shutting down.")
            break

        result = jarvis.issue_goal(user_input)
        print(f"\n[RESULT] {result}\n")
