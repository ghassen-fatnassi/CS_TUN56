@echo off
setlocal enabledelayedexpansion

:loop
rem Get the current timestamp in seconds (this will be used as the filename)
for /f "tokens=2 delims==" %%I in ('"wmic os get localdatetime /value"') do set datetime=%%I
set timestamp=%datetime:~0,4%%datetime:~4,2%%datetime:~6,2%-%datetime:~8,2%%datetime:~10,2%%datetime:~12,2%

rem Get the list of all interfaces
for /f "tokens=1* delims=." %%A in ('tshark -D') do (
    set interface_num=%%A
    set interface_name=%%B

    rem Filter for IoT-related interfaces (e.g., Wi-Fi, Bluetooth)
    if "!interface_name!"=="Wi-Fi" ( 
        set iot_device=true
    ) else if "!interface_name!"=="Bluetooth" (
        set iot_device=true
    ) else if "!interface_name!"=="Zigbee" (
        set iot_device=true
    ) else (
        set iot_device=false
    )

    if "!iot_device!"=="true" (
        rem Capture network traffic for 4 seconds on each IoT-related interface and save to a file
        tshark -i !interface_num! -a duration:4 -w ".\script_test\capture_!interface_num!_%timestamp%.pcap" > nul 2>&1

        rem Check if the file was created and contains data
        if exist ".\script_test\capture_!interface_num!_%timestamp%.pcap" (
            for %%F in (".\script_test\capture_!interface_num!_%timestamp%.pcap") do if %%~zF gtr 0 (
                echo Traffic captured on IoT interface !interface_name! and saved as capture_!interface_num!_%timestamp%.pcap
            ) else (
                del ".\script_test\capture_!interface_num!_%timestamp%.pcap"
                echo No traffic detected on IoT interface !interface_name!, file deleted.
            )
        ) else (
            echo No file created on IoT interface !interface_name!, skipping...
        )
    ) else (
        echo Interface !interface_name! is not IoT-related, skipping...
    )
)

rem Wait 4 seconds before the next capture
timeout /t 4 /nobreak > nul
goto loop
