import discord
from discord.ext import commands,tasks
import time
import asyncio
import random
import uuid

roomsInQueue = []
busyPlayers=[]
counterLengths = []
timeStamps = []




class Queue(commands.Cog):
    def __init__(self,client):
        self.client=client
        
        
    @commands.command(aliases=['start'])
    async def startqueue(self,ctx):
        if checkMemberRoles(ctx.message.author) == True and isMemberAvailable(ctx.message.author) == True:

            roomID= [str (uuid.uuid4())]

            roomsInQueue.append(roomID)
            
            await ctx.send(embed=discord.Embed(colour=discord.Colour.green(),title="Room created",description=f"Your room has been added in the active pool. It is in position {len(roomsInQueue)}. Use `=join` to join the room!"))
        else:
            if checkMemberRoles(ctx.message.author) == False:
                await ctx.send(embed=discord.Embed(colour=discord.Colour.red(),description=f"You dont have the required roles.",title="Missing Required Roles"))
            elif isMemberAvailable(ctx.message.author) == False:
                await ctx.send(embed=discord.Embed(colour=discord.Colour.red(),description=f"You are already in a queue.",title="Already in a queue."))

    @commands.command()
    async def join(self,ctx):
        timeStamps.append(int(round(time.time())))
        
        
        guild = ctx.message.guild
        

        memberHasRequiredRoles = checkMemberRoles(ctx.message.author)
        
        if memberHasRequiredRoles == True and doesRoomExist() == True and isMemberAvailable(ctx.message.author) == True:
            
            #print(roomsInQueue)
            currentRoom= roomsInQueue[0]
            if len(currentRoom) <= 11:
                currentRoom.append(ctx.message.author)
                
                
                embed=discord.Embed(colour=discord.Colour.green(),description=f"{ctx.message.author} has joined the room!",title="Room joined!")
                if len (timeStamps) == 2:
                    TimeDifference = timeStamps[1]-timeStamps[0]
                    timeStamps.pop(0)
                    if TimeDifference >= 30:
                        await ctx.send("Room was inactive for too long. It has expired. Please start a new one or run the join command again to join the next room in the pool.")
                        roomsInQueue.remove(currentRoom)
                        busyPlayers.clear()
                        return
                embed.set_thumbnail(url=ctx.message.author.avatar_url)
                await ctx.send(embed=embed)
                
                
                busyPlayers
                busyPlayers.append(ctx.message.author.id)
                
                
            if len(currentRoom) == 11:
                playersToMove = currentRoom
                centers,ballHandlers,remainingPlayers,startGame= requiredPlayers(currentRoom)
                if startGame is True:
                    await ctx.send(embed=discord.Embed(colour=discord.Colour.green(),title="Starting Game!",description ="All matchmaking requirements met! Starting Game."))
                    
                    roomsInQueue.remove(currentRoom)
                    
                    teamOne,teamTwo= sortIntoTeams(centers,ballHandlers,remainingPlayers)
                    teamOnenames,teamTwonames= convertToMentions(teamOne,teamTwo)
                    await ctx.send(f"Team One = {teamOnenames}")
                    await ctx.send(f"Team Two = {teamTwonames}")
                    logChannel = guild.get_channel(787821133709574207)
                    await logChannel.send(embed=logMatch(teamOnenames,teamTwonames,guild))
                    await moveToVC (playersToMove,guild,ctx.message.channel)
                    busyPlayers = busyPlayers[8:]
                    print ("Removed from MM hold")
                    
                else:
                    if ballHandlers == 0 and centers== 0:
                        await ctx.send(embed=discord.Embed(colour=discord.Colour.red(),description=f"Matchmaking failed! Not enough centers and ball handlers joined!.Room has expired.",title="Failed"))

                    elif ballHandlers== 0:
                        await ctx.send(embed=discord.Embed(colour=discord.Colour.red(),description=f"Matchmaking failed! Not enough ball handlers joined!.Room has expired.",title="Failed"))
                    else:
                        await ctx.send(embed=discord.Embed(colour=discord.Colour.red(),description=f"Matchmaking failed! Not enough centers joined!.Room has expired.",title="Failed"))
                    roomsInQueue.remove(currentRoom)
            


        else:
            if memberHasRequiredRoles is False:
                
                await ctx.send(embed=discord.Embed(colour=discord.Colour.red(),description=f"You don't have the required roles",title="Missing Roles"))
            elif isMemberAvailable(ctx.message.author) is False:
                await ctx.send(embed=discord.Embed(colour=discord.Colour.red(),description=f"You are already in a queue..",title="Already in a queue"))
            elif doesRoomExist() is False:
                await ctx.send(embed=discord.Embed(colour=discord.Colour.red(),description=f"No rooms available.",title="No available rooms."))
            else:
                await ctx.send("Some other bug")
        

    


def convertToMentions(teamOne,teamTwo):
    for i in range (len(teamOne)):
        teamOne[i] = f'<@{teamOne[i]}>'
    for i in range (len(teamTwo)):
        teamTwo[i] = f'<@{teamTwo[i]}>'

    return teamOne,teamTwo



def requiredPlayers(currentRoom):
    centerCount = 0
    ballHandlerCount = 0
    centerHolder= []
    ballHandlerHolder = []
    for i in range (1,len(currentRoom)):
        
        currentMember= currentRoom[i]
        memberRolesList= getMemberRolesInAList(currentMember)
        if 'Center' in memberRolesList:
            centerCount+=1
            centerHolder.append(currentMember.id)
            
        elif 'Ball Handler' in memberRolesList:
            ballHandlerCount += 1
            ballHandlerHolder.append(currentMember.id)
        if centerCount== 2 and ballHandlerCount== 2:
            break        
    
    if centerCount >=2 and ballHandlerCount >= 2:
        return centerHolder, ballHandlerHolder, currentRoom, True
    else:
        return centerHolder,ballHandlerHolder,currentRoom,False

        



def sortIntoTeams(centers,ballHandlers,currentPlayers):
    
    teamOne= []
    teamTwo=[]
    teamTwo.append(ballHandlers[0])
    teamTwo.append(centers[1])
    currentPlayers.pop(0)
    remainingPlayers =[]
    
    currentPlayers= getMemberIDs(currentPlayers)
    
    for i in currentPlayers:
        if i in centers or i in ballHandlers:
            pass
        else:
            remainingPlayers.append(i)
            
            
            

    teamOne= remainingPlayers
    

    for i in range(0,2):
        teamMember= random.choice(remainingPlayers)
        remainingPlayers.remove(teamMember)
        teamTwo.append(teamMember)
    
    teamOne.append(centers[0])
    teamOne.append(ballHandlers[1])
    


    return teamOne,teamTwo


def getMemberIDs(remainingPlayers):
    remainingPlayersIDs= []
    for i in range(len(remainingPlayers)):
        remainingPlayersIDs.append(remainingPlayers[i].id)
    return remainingPlayersIDs


def isMemberAvailable(member):
    if member.id in busyPlayers:
        return False
    else:
        return True


def doesRoomExist():
    if len(roomsInQueue) > 0:
        return True
    else:
        return False
    


def checkMemberRoles(member):
    requiredRoles = ['Ball Handler','Hash','Lock','Corner','Center']
    for i in range(len(member.roles)):
        if member.roles[i].name in requiredRoles:
            return True
                
        
    else:
        return False
        

def getMemberRolesInAList(member):
    memberRolesList =[]
    memberRoles = member.roles
    for role in memberRoles:
        memberRolesList.append(role.name)
    
    return memberRolesList

async def moveToVC(playersToMove,guild,textChannel):
    
    category= guild.get_channel(797452712136409128)
    channelToMoveTo = await guild.create_voice_channel(f'Lobby {len(category.channels)}',category= category,user_limit = 10)
    for player in playersToMove:
        try:
            await player.move_to(channelToMoveTo)
        except:
            await textChannel.send(f'{player.mention} please join a {channelToMoveTo.name}. Your game will start soon.')
        
def logMatch(teamOne,teamTwo,guild):
    embed=discord.Embed(
        colour= discord.Colour.green(),
        title = "Match logged",
        description = f"Team One: {teamOne} \n Team Two: {teamTwo}"
    )
    return embed


    
        



def setup(client):
    client.add_cog(Queue(client))