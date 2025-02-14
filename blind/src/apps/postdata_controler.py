from pyrogram import Client
from pyrogram.types.bots_and_keyboards.callback_query import CallbackQuery

from blind.src.apps.llm import llmactions
from blind.src.utils.utilities import printTest

@Client.on_callback_query()
async def controler(client:Client, CallbackQuery:CallbackQuery):    
        
    data = CallbackQuery.data
    function_name = data.split("-")[0]
    postdata = 0 if len(data.split("-")) == 1 else data.split("-")[1]

    OWNER_MESSAGE = CallbackQuery.message.reply_to_message.from_user.id if CallbackQuery.message.reply_to_message else CallbackQuery.from_user.id

    if OWNER_MESSAGE == CallbackQuery.from_user.id:
        postdata = int(postdata) if str(postdata).isdigit() else postdata

        if function_name == "cuvoAction":
            await llmactions.main(client, CallbackQuery, postdata)

        elif function_name == "rm":
            await CallbackQuery.message.delete()

        else:
            await client.answer_callback_query(
                callback_query_id=CallbackQuery.id,
                text=f"""⚠️ Function not set.\nFunction: {function_name}, postdata: {postdata}""",
                show_alert="true"
            )
    else:
        await client.answer_callback_query(
            callback_query_id=CallbackQuery.id,
            text=f"""⚠️ This button belongs to another user.\nFunction: {function_name}, postdata: {postdata}""",
            show_alert="true"
        )