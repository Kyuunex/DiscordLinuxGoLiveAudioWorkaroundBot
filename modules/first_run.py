import sqlite3
from modules.connections import database_file as database_file
import os


async def add_admins(self):
    from modules import permissions
    async with await self.db.execute("SELECT * FROM admins") as cursor:
        admin_list = await cursor.fetchall()

    if not admin_list:
        app_info = await self.application_info()
        if app_info.team:
            for team_member in app_info.team.members:
                await self.db.execute("INSERT INTO admins VALUES (?, ?)", [str(team_member.id), "1"])
                print(f"Added {team_member.name} to admin list")
        else:
            await self.db.execute("INSERT INTO admins VALUES (?, ?)", [str(app_info.owner.id), "1"])
            print(f"Added {app_info.owner.name} to admin list")
        await self.db.commit()

        permissions.load_admins_from_db()


def ensure_tables():
    conn = sqlite3.connect(database_file)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS config (setting, parent, value, flag)")
    c.execute("CREATE TABLE IF NOT EXISTS admins (user_id, permissions)")
    conn.commit()
    conn.close()
