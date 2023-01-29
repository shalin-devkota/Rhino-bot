import discord
from discord.ext import commands,tasks
import asyncio
import tweepy
 

class Twitter(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.channel.id== 784961379140501504:
            if 'youtube.com/' in message.content or 'twitch.tv/' in message.content:
              tweet(message.content)
            else:
                await message.author.send("Please include your youtube or twitch link in your self-promotion message. Do not use URL shorteners.")
            
        
            
def tweet(message):
    import tweepy 
    
    # personal details 
    consumer_key =""
    consumer_secret =""
    access_token =""
    access_token_secret =""
    
    # authentication of consumer key and secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    
    # authentication of access token and secret 
    auth.set_access_token(access_token, access_token_secret) 
    api = tweepy.API(auth) 
    
    # update the status 
    api.update_status(status =message) 
    print('tweeted')
    
        


        
                
            
def setup(client):
    client.add_cog(Twitter(client))