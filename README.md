# bot_monitor

<b>STATUS: RUNNING</b>
</br></br>
A Bot that monitor Gaia chain when something happened to a specific validator, and send alert through Telegram.
It sends alert every 15 seconds, if there is something happened during that time.
</br>
You can search this bot on Telegram by: @ForboleGaiaBot
</br>
Available commands:

/start - say hi !!!
</br>

/help - link to this github repository
</br>

/subscribe - subscribe a validator by its hexcosmosvaladdr</br>
Usage: /subscribe [hexcosmosvaladdr...]</br>

/unsubscribe - unsubscribe a validator by its hexcosmosvaladdr</br>
Usage: /unsubscribe [hexcosmosvaladdr...]</br>

/mute - mute a validator with a specific type</br>
Usage: /mute [hexcosmosvaladdr...] [absent|slashed|revoked]
</br>

/unmute - unmute a validator with a specific type</br>
Usage: /unmute [hexcosmosvaladdr...] [absent|slashed|revoked]
</br>

---deprecate---</br>
/hack - convert a cosmosvaladdr to hex</br>
Usage: /hack [cosmosvaladdr...]
</br>
