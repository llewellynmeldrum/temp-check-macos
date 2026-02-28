# temp-check-macos
![fhb](https://github.com/user-attachments/assets/c9b43397-41f2-4478-a5ca-b6449ad65c3c)

# Requirements
- macOS. Location query uses macOS stuff. In future I'll probably add IP based geoloc for Windows and Linux
- Make a Google For Developers account, and sign up to get a Google Maps API key. Follow the steps [here](https://developers.google.com/maps/documentation/weather/get-api-key). You can set it up for free, I think it will only begin charging you if you run this like 60,000 times in one day. Once you have it, place the API key in a text file called `.API_KEY` in the project root dir.

# Requirements
```bash
python main.py [-g|--gradient] [-c|--coordinates]
```
It should query you and ask for location permissions the first time.

### options:
`-c | --coordinates:`
- shows coordinates found by the CLLocationManager calls

`-g | --gradient`:
- prints out the heat gradient, with corresponding color names for each range.
<img width="670" height="895" alt="image" src="https://github.com/user-attachments/assets/92e42973-9af0-4005-a8a9-ac696ea9fa4e" />


