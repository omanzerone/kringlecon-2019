import json
ipsAttacked = set()  
useragent_fromAttack_ip  = list()
logs = json.load(open("http.log"))
for log in logs:
	if ("'" in log['uri'] or "'" in log['username'] or
		"'" in log['user_agent'] or "<" in log['uri'] or
		"<" in log['host'] or "pass" in log['uri'] or
		":;" in log['uri'] or "};" in log['uri']):
		ipsAttacked.add(log['id.orig_h'])
		useragent_fromAttack_ip.append(log['user_agent'])
for log in logs:
    if log['user_agent'] in useragent_fromAttack_ip and log['id.orig_h'] not in ipsAttacked:
        useragent_fromAttack_ip.append(log['user_agent'])
user_agent_out_of_attacked_list=set()

count_useragent_attacked = { x : useragent_fromAttack_ip.count(x) for x in useragent_fromAttack_ip }
print (count_useragent_attacked)
for i in count_useragent_attacked:
	if count_useragent_attacked[i] >= 6:
		user_agent_out_of_attacked_list.add(i)
for log in logs:
	if log['user_agent'] in useragent_fromAttack_ip and log['user_agent'] not in user_agent_out_of_attacked_list and log['id.orig_h'] not in useragent_fromAttack_ip :
		ipsAttacked.add(log['id.orig_h'])
#print(ipsAttacked)
#print(len(ipsAttacked))

print(",".join(ipsAttacked))

