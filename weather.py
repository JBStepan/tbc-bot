
import discord
from discord.ext import commands
from discord.ext import tasks
import requests

web_urls = [
    "https://radar.weather.gov/ridge/standard/KDVN_loop.gif",
    "https://www.spc.noaa.gov/products/outlook/day1otlk_2000.gif",
    "https://www.spc.noaa.gov/products/outlook/day1probotlk_2000_torn.gif",
    "https://www.spc.noaa.gov/products/outlook/day1probotlk_2000_wind.gif",
    "https://www.spc.noaa.gov/products/outlook/day1probotlk_2000_hail.gif",
    "https://www.spc.noaa.gov/products/fire_wx/day1otlk_fire.gif",
    "https://www.wpc.ncep.noaa.gov//noaa/noaa.gif"
]

file_urls = [
    "weather/outlook.png",
    "weather/torn.png",
    "weather/wind.png",
    "weather/hail.png",
    "weather/fire.png",
    "weather/fronts.png",
    "weather/radar.gif"
]

# A class to orginaize all the weather variables 
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
    
    ##############
    #  Commands  #
    ##############

    @commands.slash_command()
    async def weather(self, ctx: discord.ApplicationContext):
        weather_json = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key=6e90f3caf7ef4e2eb4a234529211712&q=Iowa City&days=1&aqi=no&alerts=yes").json()
        weather = await to_weather(weather_json)
        embed = await to_embed(weather)

        await ctx.respond(embeds=[embed])
    
    @commands.slash_command()
    async def download_weather(self, ctx: discord.ApplicationContext):
        for url in range(web_urls.__len__()):
            img_data = requests.get(web_urls[url]).content
            with open(file_urls[url], "wb") as file:
                file.write(img_data)
                
        await ctx.respond("Done.")

    @commands.slash_command()
    async def weather_images(self, ctx: discord.ApplicationContext):
        files = []
        for i in range(file_urls.__len__()):
            files.append(discord.File(file_urls[i]))
        await ctx.respond(files=files)
    
    ###########
    #  Tasks  #
    ###########

    @tasks.loop(hours=1)
    async def download_weather_images(self):
        for url in range(web_urls.__len__()):
            img_data = requests.get(web_urls[url]).content
            with open(file_urls[url], "wb") as file:
                file.write(img_data)

def setup(bot: discord.Bot):
    bot.add_cog(Weather(bot))