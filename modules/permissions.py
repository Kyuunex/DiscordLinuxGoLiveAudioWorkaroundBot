from modules.connections import database_file as database_file
import sqlite3


admin_list = []
owner_list = []


def load_admins_from_db():
    conn = sqlite3.connect(database_file)
    c = conn.cursor()
    db_admin_list = tuple(c.execute("SELECT user_id FROM admins"))
    db_owner_list = tuple(c.execute("SELECT user_id FROM admins WHERE permissions = ?", [str(1)]))
    conn.commit()
    conn.close()

    for admin_id in db_admin_list:
        admin_list.append(int(admin_id[0]))

    for owner_id in db_owner_list:
        owner_list.append(int(owner_id[0]))


load_admins_from_db()


async def is_admin(ctx):
    return int(ctx.author.id) in admin_list


async def is_owner(ctx):
    return int(ctx.author.id) in owner_list


def check_admin(user_id):
    return int(user_id) in admin_list


def check_owner(user_id):
    return int(user_id) in owner_list


async def channel_ban_members(ctx):
    return (ctx.channel.permissions_for(ctx.author)).ban_members


async def channel_manage_messages(ctx):
    return (ctx.channel.permissions_for(ctx.author)).manage_messages


async def channel_manage_guild(ctx):
    return (ctx.channel.permissions_for(ctx.author)).manage_guild
