import aiomysql


class DB:
    def __init__(self, app, credentials):
        self.credentials = credentials
        self.app = app
        self.pool = None


    async def create_pool(self):
        self.pool = await aiomysql.create_pool(**self.credentials, minsize=50, maxsize=5000, pool_recycle=10, loop=self.app.loop)

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER AUTO_INCREMENT, send_token TEXT, discord_id BIGINT, "
                                  "username TEXT, discriminator TEXT, email TEXT, avatar TEXT, is_admin BOOLEAN DEFAULT 0, "
                                  "invite_code TEXT, invited_by INTEGER DEFAULT NULL, em_title TEXT, em_desc TEXT, em_colour TEXT DEFAULT 'FFFFF', "
                                  "em_footer TEXT, em_footer_img TEXT, curr_domain INTEGER DEFAULT 0, curr_subdomain TEXT DEFAULT NULL, PRIMARY KEY(id))")

                await cur.execute("CREATE TABLE IF NOT EXISTS sessions (user INTEGER, session_token TEXT, "
                                  "expiry INTEGER, discord_token TEXT)")

                await cur.execute("CREATE TABLE IF NOT EXISTS images (user INTEGER, image_id TEXT, file_type TEXT, filename TEXT, filesize INTEGER)")

                await cur.execute("CREATE TABLE IF NOT EXISTS  invite_codes (code TEXT, used BOOL DEFAULT false, "
                                  "used_by INTEGER DEFAULT NULL, invited_by INTEGER DEFAULT 0)")

                await cur.execute("CREATE TABLE IF NOT EXISTS domains (id INTEGER AUTO_INCREMENT, domain TEXT, "
                                  "owner INTEGER, is_priv BOOLEAN DEFAULT false, PRIMARY KEY(id))")
                await conn.commit()


    async def select(self, table: str, columns: list, checks: list = None, order: list = None, single=False):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                where_val = ""
                order_val = ""
                where_ans = []

                if checks:
                    where_val = " WHERE "
                    where_ans = []
                    for check, ans in checks:
                        where_val += f"{check} = %s AND "
                        where_ans.append(ans)
                    where_val = where_val[:-4]

                if order:
                    order_val = " ORDER BY "
                    for val in order:
                        order_val += f"{val}, "
                    order_val = order_val[:-2]

                column_names = ""
                for name in columns:
                    column_names += f"{name},"

                column_names = column_names[:-1]

                try:
                    await cur.execute(f"SELECT {column_names} FROM {table}{where_val}{order_val}", tuple(where_ans))
                    if single:
                        output = await cur.fetchone()
                    else:
                        output = await cur.fetchall()

                except Exception as e:
                    print(f"[select] {e}")
                    print(f"SELECT {column_names} FROM {table}{where_val}{order_val}")
                    if checks:
                        print(where_ans)
                    return False
                else:
                    return output


    async def insert(self, table: str = None, columns: list = None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:

                column_names = ""
                column_values = []
                for name, value in columns:
                    column_names += f"{name}, "
                    column_values.append(value)

                table_names = column_names[:-2]

                try:
                    await cur.execute(
                        f"INSERT INTO {table} ({table_names}) VALUES ({('%s, ' * len(columns))[:-2]})",
                        tuple(column_values))
                    await conn.commit()
                except Exception as e:
                    print(f"[insert] {e}")
                    print(f"INSERT INTO {table} ({table_names}) VALUES ({('%s, ' * len(columns))[:-2]})")
                    print(column_values)
                    return False
                else:
                    return True


    async def update(self, table: str = None, columns: list = None, checks: list = None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                where_val = None

                if checks:
                    where_val = "WHERE "
                    for check, ans in checks:
                        where_val += f"{check} = {ans} AND "
                    where_val = where_val[:-4]

                column_names = ""
                column_values = []
                for name, value in columns:
                    column_names += f"{name} = %s,"
                    column_values.append(value)

                column_names = column_names[:-1]

                try:
                    await cur.execute(f"UPDATE {table} SET {column_names} {where_val}", tuple(column_values))
                    await conn.commit()
                except Exception as e:
                    print(f"[update] {e}")
                    print(f"UPDATE {table} SET {column_names} {where_val}")
                    print(str(column_values))
                    return False
                else:
                    return True


    async def remove(self, table: str = None, checks: list = None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                where_val = None

                if checks:
                    where_val = "WHERE "
                    where_ans = []
                    for check, ans in checks:
                        where_val += f"{check} = %s AND "
                        where_ans.append(ans)
                    where_val = where_val[:-4]

                    try:
                        await cur.execute(f"DELETE FROM {table} {where_val}", tuple(where_ans))
                        await conn.commit()

                    except Exception as e:
                        print(f"[drop] {e}")
                    else:
                        return True
                else:
                    return False
