async def owner_staff(ctx):
    if ctx.author.id == 392502213341216769 or ctx.author.id == 406629388059410434: return True
    if ctx.guild.get_role(789593786287915010) in ctx.author.roles: return True
    return False