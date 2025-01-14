# Assign city
city="Bandung"

# Obtain the weather report
curl -s wttr.in/$city?T --output weather_report

# Extract current temperature
obs_temp=$(curl -s wttr.in/$city?T | grep -m 1 '°.' | grep -Eo -e '-?[[:digit:]].*' | grep -Eo '^[0-9]+')

morning_temp=$(curl -s wttr.in/$city?T | head -13 | tail -1 | grep '°.' | cut -d 'C' -f1 | grep -Eo -e '-?[[:digit:]].*' | grep -Eo '^[0-9]+')
noon_temp=$(curl -s wttr.in/$city?T | head -13 | tail -1 | grep '°.' | cut -d 'C' -f2 | grep -Eo -e '-?[[:digit:]].*' | grep -Eo '^[0-9]+')
evening_temp=$(curl -s wttr.in/$city?T | head -13 | tail -1 | grep '°.' | cut -d 'C' -f3 | grep -Eo -e '-?[[:digit:]].*' | grep -Eo '^[0-9]+')
night_temp=$(curl -s wttr.in/$city?T | head -13 | tail -1 | grep '°.' | cut -d 'C' -f4 | grep -Eo -e '-?[[:digit:]].*' | grep -Eo '^[0-9]+')

tom_morning_temp=$(curl -s wttr.in/$city?T | head -23 | tail -1 | grep '°.' | cut -d 'C' -f1 | grep -Eo -e '-?[[:digit:]].*' | grep -Eo '^[0-9]+')
tom_noon_temp=$(curl -s wttr.in/$city?T | head -23 | tail -1 | grep '°.' | cut -d 'C' -f2 | grep -Eo -e '-?[[:digit:]].*' | grep -Eo '^[0-9]+')
tom_evening_temp=$(curl -s wttr.in/$city?T | head -23 | tail -1 | grep '°.' | cut -d 'C' -f3 | grep -Eo -e '-?[[:digit:]].*' | grep -Eo '^[0-9]+')
tom_night_temp=$(curl -s wttr.in/$city?T | head -23 | tail -1 | grep '°.' | cut -d 'C' -f4 | grep -Eo -e '-?[[:digit:]].*' | grep -Eo '^[0-9]+')

dat_morning_temp=$(curl -s wttr.in/$city?T | head -33 | tail -1 | grep '°.' | cut -d 'C' -f1 | grep -Eo -e '-?[[:digit:]].*' | grep -Eo '^[0-9]+')
dat_noon_temp=$(curl -s wttr.in/$city?T | head -33 | tail -1 | grep '°.' | cut -d 'C' -f2 | grep -Eo -e '-?[[:digit:]].*' | grep -Eo '^[0-9]+')
dat_evening_temp=$(curl -s wttr.in/$city?T | head -33 | tail -1 | grep '°.' | cut -d 'C' -f3 | grep -Eo -e '-?[[:digit:]].*' | grep -Eo '^[0-9]+')
dat_night_temp=$(curl -s wttr.in/$city?T | head -33 | tail -1 | grep '°.' | cut -d 'C' -f4 | grep -Eo -e '-?[[:digit:]].*' | grep -Eo '^[0-9]+')

# Assign timezone
TZ='Asia/Jakarta'

# Store current date and time
day=$(TZ=$TZ date +%d)
month=$(TZ=$TZ date +%m)
year=$(TZ=$TZ date +%Y)

tom_day=$(TZ=$TZ date --date='1 day' +%d)
tom_month=$(TZ=$TZ date --date='1 day' +%m)
tom_year=$(TZ=$TZ date --date='1 day' +%Y)

dat_day=$(TZ=$TZ date --date='2 days' +%d)
dat_month=$(TZ=$TZ date --date='2 days' +%m)
dat_year=$(TZ=$TZ date --date='2 days' +%Y)

# Log the weather
today_record=$(echo -e "$year,$month,$day,$obs_temp,$morning_temp,$noon_temp,$evening_temp,$night_temp")
tomorrow_record=$(echo -e "$tom_year,$tom_month,$tom_day,$tom_morning_temp,$tom_noon_temp,$tom_evening_temp,$tom_night_temp")
dayAfterTomorrow_record=$(echo -e "$dat_year,$dat_month,$dat_day,$dat_morning_temp,$dat_noon_temp,$dat_evening_temp,$dat_night_temp")

echo "$today_record" >> today_weather_data.csv
echo "$tomorrow_record" >> tomorrow_weather_data.csv
echo "$dayAfterTomorrow_record" >> dayAfterTomorrow_weather_data.csv