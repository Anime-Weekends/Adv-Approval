from pyrofork import Client, filters
from pyrofork.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID
from modules.database import (
    add_user, get_users, add_admin, remove_admin,
    get_admins, is_admin, get_connected_channels
)
from script import *
import asyncio
import random

app = Client("auto_approver_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("start"))
async def start(_, message: Message):
    user_id = message.from_user.id
    await add_user(user_id)
    await message.reply_photo(
        photo=random.choice(START_IMAGES),
        caption=START_MSG,
        reply_markup=start_buttons
    )


@app.on_message(filters.command("myid"))
async def myid(_, message: Message):
    await message.reply_text(f"`{message.from_user.id}`")


@app.on_message(filters.command("ping"))
async def ping(_, message: Message):
    if message.from_user.id in await get_admins():
        await message.reply("Pong!")


@app.on_message(filters.command("help"))
async def help_cmd(_, message: Message):
    await message.reply_photo(
        photo=random.choice(START_IMAGES),
        caption=HELP_MSG,
        reply_markup=help_buttons
    )


@app.on_message(filters.command("connectedchnls"))
async def connected_channels(_, message: Message):
    user_id = message.from_user.id
    channels = await get_connected_channels(user_id)
    if not channels:
        await message.reply_text("No connected channels found.")
    else:
        text = "**Connected Channels:**\n\n"
        for ch in channels:
            text += f"› `{ch['name']}` (`{ch['id']}`)\n"
        await message.reply(text)


@app.on_message(filters.command("addadmin"))
async def addadmin(_, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("Only the owner can use this command.")
    if len(message.command) < 2:
        return await message.reply("Usage: /addadmin <user_id>")
    user_id = int(message.command[1])
    await add_admin(user_id)
    await message.reply(f"Added `{user_id}` as admin.")


@app.on_message(filters.command("removeadmin"))
async def removeadmin(_, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("Only the owner can use this command.")
    if len(message.command) < 2:
        return await message.reply("Usage: /removeadmin <user_id>")
    user_id = int(message.command[1])
    await remove_admin(user_id)
    await message.reply(f"Removed `{user_id}` from admin list.")


@app.on_message(filters.command("listadmins"))
async def listadmins(_, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("Only the owner can view the admin list.")
    admins = await get_admins()
    text = "**Admin Users:**\n\n"
    for uid in admins:
        text += f"› `{uid}`\n"
    await message.reply(text)


@app.on_message(filters.command("users"))
async def all_users(_, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("Only owner can use this command.")
    users = await get_users()
    await message.reply(f"Total users: `{len(users)}`")


@app.on_message(filters.command("broadcast"))
async def broadcast(_, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("Only owner can broadcast.")
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast.")
    
    users = await get_users()
    sent = 0
    failed = 0
    for uid in users:
        try:
            await message.copy(uid)
            sent += 1
        except:
            failed += 1
        await asyncio.sleep(0.1)
    await message.reply(f"Broadcast complete.\n✅ Sent: `{sent}`\n❌ Failed: `{failed}`")


@app.on_message(filters.command("forward_broadcast"))
async def forward_broadcast(_, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("Only owner can forward broadcast.")
    if not message.reply_to_message:
        return await message.reply("Reply to a message to forward broadcast.")
    
    users = await get_users()
    sent = 0
    failed = 0
    for uid in users:
        try:
            await message.reply_to_message.forward(uid)
            sent += 1
        except:
            failed += 1
        await asyncio.sleep(0.1)
    await message.reply(f"Forward broadcast complete.\n✅ Sent: `{sent}`\n❌ Failed: `{failed}`")


@app.on_message(filters.command("approveall"))
async def approve_all(_, message: Message):
    await message.reply("All users auto approved (placeholder).")


@app.on_message(filters.command("rejectall"))
async def reject_all(_, message: Message):
    await message.reply("All users auto rejected (placeholder).")


app.run()
