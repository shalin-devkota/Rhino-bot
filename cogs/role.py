import discord
from discord.ext import commands,tasks



class Role(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.Cog.listener()
    async def on_raw_reaction_add(ctx,payload):
        availableRoles={
            '785966239410421781':784850855207632908,
            '785966621373366303':784850974376198154,
            '785966239356157973':784851937790918677,
            '785966239406489680':784850931572277249,
            '785966621461184553':784850996261945375
        }
        availableConsoles={
            '785969692325052457':784911779792158732,
            '786705223300153394':784911903314542612
        }
        message_id = payload.message_id
        if message_id == 786707330480996373:
            member = payload.member
            reaction = payload.emoji
            reactionID = payload.emoji.id
            guild_id= payload.guild_id
            guild= ctx.client.get_guild(guild_id)
            reactionRole= availableRoles[f'{reactionID}']
            roleToAdd=guild.get_role(reactionRole)
            print (roleToAdd)
            roleExist,roleName = doesMemberHaveRole(member)
            if roleExist == True:
                roleToRemove= discord.utils.get(guild.roles,name=roleName)
                await member.remove_roles(roleToRemove)
                await member.add_roles(roleToAdd)
                await member.send(f"You have been given the {roleToAdd} role. Your previous role has been overwriten.")
            else:
                await member.add_roles(roleToAdd)
                await member.send(f"You have been given the {roleToAdd} role.")
        
            channel = guild.get_channel(784947225779372032)
            message = await channel.fetch_message (message_id)
            await message.remove_reaction(reaction,member)
        elif message_id == 786705905042849812:
            member = payload.member
            reaction = payload.emoji
            reactionID = payload.emoji.id
            guild_id= payload.guild_id
            guild= ctx.client.get_guild(guild_id)
            reactionRole= availableConsoles[f'{reactionID}']
            roleToAdd=guild.get_role(reactionRole)
            await member.add_roles(roleToAdd)

    
       
        

def doesMemberHaveRole(member):
    
    requiredRoles= ['Hash','Center','Corner','Lock','Ball Handler']
    for role in member.roles:
        if role.name in requiredRoles:
            hasRole = True
            roleName = role.name
            break
        else:
            hasRole= False
        
    if hasRole is True:
        return True, roleName
    else:
        return False,None
        
        
        
        

            
           
        

        
    


def setup(client):
    client.add_cog(Role(client))