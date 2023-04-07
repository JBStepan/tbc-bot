
import discord
from discord.ext import commands
import requests
import os

class WeatherClass:
    def __init__(self, current_temp: int, humidity: int, condition: str, feelslike: int, condition_img: str, wind: int, pressure: int, visable: int) -> None:
        self.current_temp = current_temp
        self.humidity = humidity
        self.condition = condition
        self.feelslike = feelslike
        self.visable = visable
        self.pressure = pressure
        self.condition_img = condition_img
        self.wind = wind
    
async def to_weather(json):
    cur_temp = int(json["current"]["temp_f"])
    feelslike = int(json["current"]["feelslike_f"])
    humidity = int(json["current"]["humidity"])
    condition = json["current"]["condition"]["text"]
    condition_img = json["current"]["condition"]["icon"]
    wind_speed = int(json["current"]["wind_mph"])
    pressure = int(json["current"]["pressure_mb"]) 
    visable = int(json["current"]["vis_miles"])  

    return WeatherClass(cur_temp, humidity, condition, feelslike, condition_img, wind_speed, pressure, visable) 
    
async def to_embed(weather: WeatherClass):
    embed =  discord.Embed()\
    .add_field(name="Temp", value=f"**{weather.current_temp}F**", inline=True)\
    .add_field(name="Feelslike", value=f"**{weather.feelslike}F**", inline=True)\
    .add_field(name="Humidity", value=f"**{weather.humidity}%**", inline=True)\
    .set_thumbnail(url=weather.condition_img.replace("//", "https://"))

    embed.url = "https://forecast.weather.gov/MapClick.php?lat=41.65782000000007&lon=-91.52652999999998"
    embed.title = "Weather in Iowa City"
    embed.description = f"It is currently {weather.condition}"

    return embed
    

class Weather(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    
    @commands.slash_command()
    async def weather(self, ctx: discord.ApplicationContext):
        weather_json = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key=6e90f3caf7ef4e2eb4a234529211712&q=Iowa City&days=1&aqi=no&alerts=yes").json()
        weather = await to_weather(weather_json)
        embed = await to_embed(weather)

        await ctx.respond(embeds=[embed])
    
    @commands.slash_commawnd()
    async def threat_weather(self, ctx: discord.ApplicationContext):
        await ctx.respond("https://www.spc.noaa.gov/products/outlook/day1otlk_2000.gif https://www.spc.noaa.gov/products/outlook/day1probotlk_2000_torn.gif https://www.spc.noaa.gov/products/outlook/day1probotlk_2000_wind.gif https://www.spc.noaa.gov/products/outlook/day1probotlk_2000_hail.gif")


def setup(bot: discord.Bot):
    bot.add_cog(Weather(bot))

