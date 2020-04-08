import discord
from modules.connections import database_file as database_file
import sqlite3

conn = sqlite3.connect(database_file)
c = conn.cursor()
db_admin_list = tuple(c.execute("SELECT user_id FROM admins"))
db_owner_list = tuple(c.execute("SELECT user_id FROM admins WHERE permissions = ?", [str(1)]))
conn.commit()
conn.close()

admin_list = []
for admin_id in db_admin_list:
    admin_list.append(admin_id[0])


owner_list = []
for owner_id in db_owner_list:
    owner_list.append(owner_id[0])


async def is_admin(ctx):
    return str(ctx.author.id) in admin_list


async def is_owner(ctx):
    return str(ctx.author.id) in owner_list


def get_admin_list():
    contents = ""
    for user_id in admin_list:
        contents += f"<@{user_id}>\n"
    return discord.Embed(title="Bot admin list", description=contents, color=0xffffff)


def check_admin(user_id):
    return str(user_id) in admin_list


def check_owner(user_id):
    return str(user_id) in owner_list
