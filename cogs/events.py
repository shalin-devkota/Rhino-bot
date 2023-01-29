import discord
from discord.ext import commands,tasks
from datetime import datetime
import json
import asyncio
import random



class Events(commands.Cog):
    def __init__(self,client):
        self.client=client

   
       


    @commands.Cog.listener()
    async def on_ready (self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game("Finding games"))
        print("Bot is ready")

    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        
        print(f"{member} has joined a server.")
       

   

        
        
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        print(f"{member} has left a server.")

    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        if before.channel and not after.channel:
            if before.channel.category.id == 797452712136409128 and len(before.channel.members)== 0:
                await before.channel.delete()


    @commands.Cog.listener()
    async def on_message(self,message):
        try:
            if message.channel.id== 786705671697334292 and message.author.id!= 700341764380295219:
                await message.author.edit(nick=message.content)
                await message.author.send(f"Your nickname has been set to {message.content}")
        except discord.errors.Forbidden:
            await message.author.send("You are probably an admin/mod. If yes, then this is expected. Please set your nickname manually. If you are not an admin/mod, please contact the server staff/ the developer and reprot this bug. Thank you!")

            


def setup(client):
    client.add_cog(Events(client))

