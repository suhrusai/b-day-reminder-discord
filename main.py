import sys
import os
from Helpers.TimeHelper import today_in_tz
from Services.DiscordService import DiscordService
from Services.BirthdayService import BirthdayService
from dotenv import load_dotenv


async def main():
    # Initialize services
    BirthdayService()
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

    # Validate the token
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in environment variables.")
        sys.exit(1)

    client = DiscordService.client

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

        try:
            if today_in_tz().day == 1:
                try:
                    await DiscordService.delete_recent_notifications("monthly")
                except Exception as e:
                    print("Failed to delete previous monthly messages")
                    print(e)
                await DiscordService.send_birthday_notifications("monthly")
            try:
                await DiscordService.delete_recent_notifications("daily")
            except Exception as e:
                print("Failed to delete previous daily messages")
                print(e)
            await DiscordService.send_birthday_notifications("daily")
        except Exception as e:
            print(f"Error during notifications: {e}")
        finally:
            await client.close()
            sys.exit(0)

    try:
        await client.start(TOKEN)
    except Exception as e:
        print(f"Error during client startup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())