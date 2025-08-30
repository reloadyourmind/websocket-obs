-- Reaper Integration for OBS Remote Control
-- This script allows Reaper to control OBS input devices remotely

local obs_server_url = "http://192.168.1.100:5000"  -- Change to your OBS server IP
local devices = {}
local selected_device = nil

-- HTTP request function
function http_request(url, method, data)
    local cmd = string.format('curl -s -X %s "%s"', method, url)
    if data then
        cmd = cmd .. string.format(' -H "Content-Type: application/json" -d \'%s\'', data)
    end
    
    local handle = io.popen(cmd)
    local result = handle:read("*a")
    handle:close()
    
    return result
end

-- Get devices from OBS
function get_obs_devices()
    local response = http_request(obs_server_url .. "/api/devices", "GET")
    local success, data = pcall(function() return reaper.JSON_Parse(response) end)
    
    if success and data.devices then
        devices = data.devices
        return true
    end
    return false
end

-- Toggle device
function toggle_device(device_name)
    local response = http_request(obs_server_url .. "/api/toggle/" .. device_name, "POST")
    local success, data = pcall(function() return reaper.JSON_Parse(response) end)
    return success and data.success
end

-- Set device volume
function set_device_volume(device_name, volume_db)
    local data = string.format('{"volume_db": %f}', volume_db)
    local response = http_request(obs_server_url .. "/api/volume/" .. device_name, "POST", data)
    local success, result = pcall(function() return reaper.JSON_Parse(response) end)
    return success and result.success
end

-- Main menu
function show_main_menu()
    local menu = "OBS Remote Control\n\n"
    menu = menu .. "1. Refresh devices\n"
    menu = menu .. "2. Select device\n"
    menu = menu .. "3. Toggle selected device\n"
    menu = menu .. "4. Set volume\n"
    menu = menu .. "5. Exit\n\n"
    
    local choice = reaper.GetUserInputs("OBS Remote Control", 1, "Choose option (1-5):", "")
    
    if choice == "1" then
        if get_obs_devices() then
            reaper.ShowMessageBox("Devices refreshed successfully!", "Success", 0)
        else
            reaper.ShowMessageBox("Failed to get devices", "Error", 0)
        end
        show_main_menu()
    elseif choice == "2" then
        show_device_selection()
    elseif choice == "3" then
        if selected_device then
            if toggle_device(selected_device) then
                reaper.ShowMessageBox("Device toggled successfully!", "Success", 0)
            else
                reaper.ShowMessageBox("Failed to toggle device", "Error", 0)
            end
        else
            reaper.ShowMessageBox("No device selected", "Error", 0)
        end
        show_main_menu()
    elseif choice == "4" then
        if selected_device then
            show_volume_control()
        else
            reaper.ShowMessageBox("No device selected", "Error", 0)
            show_main_menu()
        end
    elseif choice == "5" then
        return
    else
        show_main_menu()
    end
end

-- Device selection menu
function show_device_selection()
    if #devices == 0 then
        if not get_obs_devices() then
            reaper.ShowMessageBox("No devices available", "Error", 0)
            show_main_menu()
            return
        end
    end
    
    local menu = "Select Device:\n\n"
    for i, device in ipairs(devices) do
        local status = device.muted and "MUTED" or "ACTIVE"
        menu = menu .. string.format("%d. %s (%s) - %s\n", i, device.name, device.input_kind, status)
    end
    menu = menu .. "\n0. Back to main menu"
    
    local choice = reaper.GetUserInputs("Device Selection", 1, "Choose device (0-%d):", #devices)
    local device_index = tonumber(choice)
    
    if device_index and device_index > 0 and device_index <= #devices then
        selected_device = devices[device_index].name
        reaper.ShowMessageBox("Selected: " .. selected_device, "Success", 0)
        show_main_menu()
    elseif device_index == 0 then
        show_main_menu()
    else
        show_device_selection()
    end
end

-- Volume control
function show_volume_control()
    local current_volume = 0
    for _, device in ipairs(devices) do
        if device.name == selected_device then
            current_volume = device.volume_db
            break
        end
    end
    
    local volume_input = reaper.GetUserInputs("Volume Control", 1, 
        string.format("Set volume for %s (current: %.1f dB):", selected_device, current_volume), 
        tostring(current_volume))
    
    local new_volume = tonumber(volume_input)
    if new_volume then
        if set_device_volume(selected_device, new_volume) then
            reaper.ShowMessageBox("Volume set successfully!", "Success", 0)
        else
            reaper.ShowMessageBox("Failed to set volume", "Error", 0)
        end
    end
    show_main_menu()
end

-- Initialize and start
reaper.ClearConsole()
reaper.ShowMessageBox("OBS Remote Control initialized", "Info", 0)
show_main_menu()