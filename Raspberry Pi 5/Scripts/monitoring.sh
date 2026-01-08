#!/bin/bash

# Temperatura w °C
temp=$(vcgencmd measure_temp 2>/dev/null | tr -d "temp='C" )
if [ -z "$temp" ]; then
  temp=$(awk '{printf "%.1f", $1/1000}' /sys/class/thermal/thermal_zone0/temp)
fi

# CPU usage – średnia z ~1 sekundy
cpu_idle_1=$(awk '/^cpu / {print $5}' /proc/stat)
cpu_total_1=$(awk '/^cpu / {sum=$2+$3+$4+$5+$6+$7+$8+$9+$10; print sum}' /proc/stat)
sleep 1
cpu_idle_2=$(awk '/^cpu / {print $5}' /proc/stat)
cpu_total_2=$(awk '/^cpu / {sum=$2+$3+$4+$5+$6+$7+$8+$9+$10; print sum}' /proc/stat)

cpu=$(
  awk -v idle1="$cpu_idle_1" -v idle2="$cpu_idle_2" -v total1="$cpu_total_1" -v total2="$cpu_total_2" \
    'BEGIN {
       idle  = idle2  - idle1;
       total = total2 - total1;
       if (total <= 0) { printf "0.0"; exit }
       printf "%.1f", (1 - idle/total) * 100
     }'
)


# RAM usage w %
mem=$(free -m | awk 'NR==2{printf "%.0f", $3*100/$2 }')

# Uptime w sekundach -> godziny (zaokrąglone w dół)
uptime_seconds=$(awk '{print int($1)}' /proc/uptime)
uptime_hours=$(( uptime_seconds / 3600 ))

# Najbardziej obciążający proces (CPU)
read top_cpu_usage top_cpu_cmd <<< "$(ps -eo %cpu,comm --sort=-%cpu | sed -n '2p')"

printf '{
  "temp": %.1f,
  "temp_unit": "C",
  "cpu": %.1f,
  "cpu_unit": "percent",
  "mem": %d,
  "mem_unit": "percent",
  "uptime_hours": %d,
  "uptime_unit": "hours",
  "top_cpu_usage": %.1f,
  "top_cpu_cmd": "%s"
}
' "$temp" "$cpu" "$mem" "$uptime_hours" "$top_cpu_usage" "$top_cpu_cmd"
