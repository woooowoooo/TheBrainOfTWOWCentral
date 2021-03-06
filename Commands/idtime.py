import discord, datetime

def HELP(PREFIX):
	return {
		"COOLDOWN": 1,
		"MAIN": "Finds the time corresponding to a Discord snowflake (ID).",
		"FORMAT": "[id] (id2) (mode)",
		"CHANNEL": 0,
		"USAGE": f"""Using `{PREFIX}idtime` will return the time corresponding to the provided Discord 
		snowflake. "message" or "user" can replace numeric IDs to use the ID of your message or your account 
		respectively. Two IDs can be included instead of one to calculate the difference in time between 
		them. A mode (timestamp, unix) can be specified at the end to display the resulting time in.
		""".replace("\n", "").replace("\t", ""),
		"CATEGORY" : "Utility"
	}

PERMS = 0 # Non-members
ALIASES = []
REQ = []

async def MAIN(message, args, level, perms, SERVER):
	if level == 1:
		await message.channel.send("Include the ID you would like to find the time of.")
	else:
		snowflake_list = []
		format_list = []
		unix_list = []
		if level > 1:
			mode = "n/a"
			for elem in args[1:]:
				try:
					snowflake_list.append(int(elem))
				except ValueError:
					if elem == "message":
						snowflake_list.append(message.id)
					elif elem == "user":
						snowflake_list.append(message.author.id)
					else:
						mode = elem
						break
			if mode not in ["timestamp", "unix"]:
				mode = "timestamp"
		else:
			snowflake_list = [int(args[1])]
			mode = "timestamp"
		output = ""
		snowflake_list = snowflake_list[:2]
		for snowflake in snowflake_list:
			if snowflake > 18446744073709551615 or snowflake < 0:
				snowflake_list.remove(snowflake)
				continue
			snowflaketime = bin(snowflake)[2:].zfill(64)
			snowflaketime = snowflaketime[:42]
			snowflaketime = (int(snowflaketime, 2) + 1420070400000)/1000
			unix_list.append(snowflaketime)
			if mode == "timestamp":
				ft = str(datetime.datetime.fromtimestamp(snowflaketime))
				if ft.endswith("000"):
					ft = ft[:-3]
				else:
					ft = ft + ".000"
				format_list.append(ft + " UTC")
			elif mode == "unix":
				format_list.append(str(snowflaketime))
		for i in range(len(snowflake_list)):
			output += (str(snowflake_list[i]) + " → **" + format_list[i] + "**")
			output += "\n"
		if len(snowflake_list) > 1:
			ds = abs(unix_list[0] - unix_list[1])
			diff = []
			for increment in [86400, 3600, 60]:
				diff.append(round(ds - ds % increment) // increment)
				ds = ds % increment
			diff.append(round(ds, 3))
			diff[0] = str(diff[0])
			diff[1] = str(diff[1]).zfill(2)
			diff[2] = str(diff[2]).zfill(2)
			sec = str(diff[3]).split(".")
			diff[3] = sec[0].zfill(2) + "." + sec[1].ljust(3, '0')
			output += "Difference: **" + (":".join(diff)).lstrip("0:") + "**"
		elif len(snowflake_list) == 0:
			await message.channel.send("Invalid ID.")
			return
		await message.channel.send(output)
	return