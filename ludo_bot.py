import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

players = []
positions = {}
turn_index = 0
game_started = False

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players
    user = update.effective_user.first_name
    if game_started:
        await update.message.reply_text("Game already started. Wait for next round.")
        return
    if user not in players and len(players) < 4:
        players.append(user)
        positions[user] = 0
        await update.message.reply_text(f"{user} joined the game! 🎮")
    else:
        await update.message.reply_text("You're already in or game is full.")

async def startgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game_started
    if len(players) < 2:
        await update.message.reply_text("Need at least 2 players to start.")
    else:
        game_started = True
        await update.message.reply_text(f"Game started! {players[0]} goes first 🎲")

async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global turn_index
    user = update.effective_user.first_name
    if not game_started:
        await update.message.reply_text("Game hasn’t started yet. Use /startgame.")
        return
    if players[turn_index] != user:
        await update.message.reply_text(f"Not your turn, {user}. It's {players[turn_index]}'s turn.")
        return
    dice = random.randint(1, 6)
    positions[user] += dice
    await update.message.reply_text(f"{user} rolled a {dice} 🎲 and moved to position {positions[user]}")
    turn_index = (turn_index + 1) % len(players)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    board = "\n".join([f"{p}: {positions[p]} steps" for p in players])
    await update.message.reply_text(f"📍 Current Positions:\n{board}")

TOKEN = os.getenv("8037587323:AAHSp9yOOCEVL6bw2dpZtEiQ1Bjlxe-vMuo")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("join", join))
app.add_handler(CommandHandler("startgame", startgame))
app.add_handler(CommandHandler("roll", roll))
app.add_handler(CommandHandler("status", status))
app.run_polling()
