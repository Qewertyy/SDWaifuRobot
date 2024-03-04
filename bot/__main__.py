import bot

if __name__ == "__main__":
    import bot.modules
    bot.executor.start_polling(bot.dp, skip_updates=True)