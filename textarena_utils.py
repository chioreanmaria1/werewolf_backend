from __future__ import annotations

import re
from dataclasses import dataclass

THINK_RE = re.compile(r"<think>(.*?)</think>", re.DOTALL | re.IGNORECASE)
ACTION_RE = re.compile(r"<action>(.*?)</action>", re.DOTALL | re.IGNORECASE)
BRACKET_ACTION_RE = re.compile(r"\[\d+\]")


@dataclass
class ParsedResponse:
    raw_text: str
    reasoning: str
    action: str

# Here you have the possibility to enhance the observation prompt from the system
def build_agent_prompt(observation: str) -> str:
    matches = re.findall('\[GAME\](.*)(?=\n|$)', observation)
    order = matches[-1].strip()
    if "Voting phase" in order:
        order = "You MUST vote. You MUST NOT discuss. You MUST NOT explain. You MUST NOT output anything except a valid bracketed number."
    elif "Discuss" in order:
        order = """You MUST discuss. Think privately. Output ONLY your public statement. Do NOT reveal hidden reasoning. Do NOT reveal your role. DO it only if you are a DETECTIVE and you have information to share. Otherwise, output NOTHING. 
        If you are a MAFIA, you can share false information, but do NOT reveal your role. If you are a VILLAGER, you can share true information, but do NOT reveal your role. In either case, DO NOT reveal your role or private reasoning.
        Special roles like DOCTOR OR DETECTIVE exist, but YOU have to decide if they are trustworthy or not based on the information you have. You can choose to share information or stay silent, but you MUST NOT reveal your role or private reasoning.
        """
    else:
        order = "You MUST perform your role action. Output ONLY one valid bracketed number. Do NOT explain."
    return f"{observation}\n\n{order}"


def parse_model_response(raw_text: str) -> ParsedResponse:
    # reasoning_match = THINK_RE.search(raw_text)
    # action_match = ACTION_RE.search(raw_text)

    #reasoning = reasoning_match.group(1).strip() if reasoning_match else ""
    reasoning = ""
    
    #bracket_match = BRACKET_ACTION_RE.search(raw_text)
    #action = bracket_match.group(0) if bracket_match else raw_text.strip().splitlines()[0]
    action = raw_text

    return ParsedResponse(raw_text=raw_text, reasoning=reasoning, action=action)
