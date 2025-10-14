# Network Access Guide

## How to Access the App from Another Computer

This guide explains how to use your laptop as a server and access the EFI IT Issue Tracker from other devices on your network.

---

## Quick Start (3 Steps)

### Step 1: Start the Server on Your Laptop

1. On your **server laptop** (the one with the application), double-click `start.bat`
2. You'll see output like this:

```
============================================================
Application URLs:
  - Local access:   http://127.0.0.1:5000
  - Network access: http://192.168.1.100:5000

Share this URL with others on your network:
  http://192.168.1.100:5000
============================================================
```

3. **Write down the Network IP address** (e.g., `192.168.1.100:5000`)

### Step 2: Check Windows Firewall (One-Time Setup)

The first time you run the server, Windows may ask if you want to allow network access:

1. When the Windows Security Alert appears, check **both boxes**:
   - ✅ Private networks (home or work)
   - ✅ Public networks
2. Click **Allow access**

**If you didn't see this prompt**, you may need to manually add a firewall rule:

1. Press `Windows + R`, type `wf.msc`, press Enter
2. Click "Inbound Rules" → "New Rule"
3. Select "Port" → Next
4. Select "TCP" → Enter port `5000` → Next
5. Select "Allow the connection" → Next
6. Check all three boxes (Domain, Private, Public) → Next
7. Name it "EFI Issue Tracker" → Finish

### Step 3: Access from Another Device

1. Make sure both devices are on the **same WiFi network** or connected to the same router
2. On the other laptop/device, open any web browser (Chrome, Edge, Firefox, etc.)
3. Type the Network URL in the address bar:
   ```
   http://192.168.1.100:5000
   ```
   (Replace `192.168.1.100` with your actual IP address from Step 1)

4. Press Enter - you should see the login page!

---

## Troubleshooting

### Problem: "This site can't be reached" or "Unable to connect"

**Solution 1: Check if both devices are on the same network**
- Server laptop WiFi: `YourWiFiName`
- Other laptop WiFi: `YourWiFiName` (must be the same!)

**Solution 2: Check Windows Firewall**
- Follow Step 2 above to add a firewall rule
- Or temporarily disable firewall to test (Settings → Windows Security → Firewall → Turn off)

**Solution 3: Verify the server is running**
- Make sure `start.bat` is still running on the server laptop
- You should see Flask output in the command window

**Solution 4: Use the correct IP address**
- The IP address changes if you connect to a different WiFi network
- Restart `start.bat` to see the current IP address

### Problem: "Connection refused" or "Reset connection"

**Check the port number**
- Make sure you include `:5000` at the end of the URL
- Correct: `http://192.168.1.100:5000`
- Wrong: `http://192.168.1.100`

### Problem: IP address shows as "Unable to detect"

**Manually find your IP address:**
1. Press `Windows + R`, type `cmd`, press Enter
2. Type `ipconfig` and press Enter
3. Look for "IPv4 Address" under your active network adapter
4. Example: `IPv4 Address. . . . . . . . . . . : 192.168.1.100`

---

## How It Works

### Server Laptop (Your Laptop)
- Runs the Flask application
- Acts as a web server
- IP Address: `192.168.1.100` (example)
- Port: `5000`

### Client Laptop (Other Laptop)
- Opens web browser
- Connects to server laptop's IP address
- Uses the app just like a website

```
[Server Laptop]  ←→  WiFi Router  ←→  [Client Laptop]
  192.168.1.100                         Opens browser
  Running app.py                        Goes to 192.168.1.100:5000
```

---

## Important Notes

### Security
- Only devices on your local network can access the app
- Devices outside your network (on the internet) **cannot** access it
- This is safe for use within your office/home network

### Keep Server Running
- The server laptop must stay on with `start.bat` running
- If you close the command window, the server stops
- Other devices will lose access until you restart the server

### Dynamic IP Addresses
- Your laptop's IP address may change when you:
  - Restart your laptop
  - Connect to a different WiFi network
  - Reconnect to the same network
- If the IP changes, restart `start.bat` to see the new IP address
- Share the new URL with other users

### Multiple Users
- Multiple people can access the app at the same time
- Each person logs in with their own username/password
- All changes are saved to the database on the server laptop

---

## Advanced: Using a Fixed IP Address (Optional)

If you want your laptop to always use the same IP address:

### Method 1: Reserve IP in Router
1. Log into your router's admin panel (usually http://192.168.1.1)
2. Find "DHCP Reservation" or "Static IP" settings
3. Add your laptop's MAC address and assign a fixed IP
4. Consult your router's manual for specific steps

### Method 2: Windows Static IP
1. Open Settings → Network & Internet → WiFi → Properties
2. Under "IP settings" click Edit
3. Choose "Manual" → Enable IPv4
4. Enter:
   - IP address: `192.168.1.100` (or any available IP)
   - Subnet mask: `255.255.255.0`
   - Gateway: `192.168.1.1` (your router's IP)
   - DNS: `8.8.8.8` (Google DNS)
5. Save

---

## Using on Mobile Devices

The app is fully mobile responsive! You can access it from:
- Smartphones (iPhone, Android)
- Tablets (iPad, Android tablets)

Just open the browser on your mobile device and enter the same URL:
```
http://192.168.1.100:5000
```

Make sure your mobile device is connected to the same WiFi network!

---

## Need Help?

### Check these first:
1. ✅ Server laptop is running `start.bat`
2. ✅ Both devices on the same WiFi network
3. ✅ Windows Firewall allows port 5000
4. ✅ Using the correct IP address with `:5000`
5. ✅ Typing `http://` before the IP address

### Still stuck?
- Restart both laptops
- Restart your WiFi router
- Try accessing from the server laptop first using `http://127.0.0.1:5000`
- Check the command window for error messages
