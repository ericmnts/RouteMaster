import argparse
import asyncio
import datetime
import json
import os
from importlib import import_module

from worksheets.annotation_utils import get_agent_action_schemas, get_context_schema
from worksheets.modules import generate_next_turn
from worksheets.modules import utils as chat_utils
from worksheets.modules.dialogue import CurrentDialogueTurn

date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

current_dir = os.path.dirname(os.path.realpath(__file__))

domain_choices = os.listdir(os.path.join(current_dir, "agents"))
domain_choices = [x for x in domain_choices if not x.startswith("__")]


def create_parser():
    parser = argparse.ArgumentParser(description="Tipbot")
    parser.add_argument(
        "--domain",
        type=str,
        choices=domain_choices,
        default="tip",
    )
    parser.add_argument(
        "--spec_type",
        type=str,
        choices=["python", "spreadsheet"],
        default="spreadsheet",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Will prompt the user to save the state of the chatbot",
    )

    return parser


def import_domain(domain, spec_type):
    if domain in domain_choices:
        if spec_type == "python":
            bot = import_module(f"worksheets.agents.{domain}.worksheets")
        elif spec_type == "spreadsheet":
            spreadsheet = import_module(f"worksheets.agents.{domain}").spreadsheet
            bot = spreadsheet.gsheet_to_genie(
                bot_name=spreadsheet.botname,
                description=spreadsheet.description,
                prompt_dir=spreadsheet.prompt_dir,
                starting_prompt=spreadsheet.starting_prompt,
                args={},
                api=spreadsheet.api,
                gsheet_id=spreadsheet.gsheet_id_default,
                suql_runner=spreadsheet.suql_runner,
                suql_prompt_selector=spreadsheet.suql_prompt_selector,
            )
        else:
            raise ValueError(f"Spec type {spec_type} not found")

        return bot


def convert_to_json(dialogue: list[CurrentDialogueTurn]):
    json_dialogue = []
    for turn in dialogue:
        json_turn = {
            "user": turn.user_utterance,
            "bot": turn.system_response,
            "turn_context": get_context_schema(turn.context),
            "global_context": get_context_schema(turn.global_context),
            "system_action": get_agent_action_schemas(turn.system_action),
            "user_target_sp": turn.user_target_sp,
            "user_target": turn.user_target,
            "user_target_suql": turn.user_target_suql,
        }
        json_dialogue.append(json_turn)
    return json_dialogue


async def main(**args):
    bot = import_domain(args["domain"], args["spec_type"])
    quit_commands = ["exit", "exit()"]

    save_file_name = f"log_json/chatbot_state_{date_str}.json"

    try:
        while True:
            if len(bot.dlg_history) == 0:
                chat_utils.print_chatbot(bot.starting_prompt)
            user_utterance = None
            if user_utterance is None:
                user_utterance = chat_utils.input_user()
            if user_utterance == quit_commands:
                break

            await generate_next_turn(user_utterance, bot)
            chat_utils.print_complete_history(bot.dlg_history)
    except Exception as e:
        print(e)

        import traceback

        traceback.print_exc()
    finally:
        with open(save_file_name, "w") as f:
            json.dump(convert_to_json(bot.dlg_history), f, indent=4)


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    asyncio.run(main(**args.__dict__))
