# bot_monitor

A Bot that monitor Gaia chain when something happened to a specific validator, and send alert through Telegram.
It sends alert every 15 seconds, if there is something happened during that time.

Available commands:

/start - say hi !!!
</br>

/help - link to this github repository
</br>

/subscribe - subscribe a validator by its cosmosvaladdr</br>
Usage: /subscribe </br>
  --> then provide validator address
</br>

/mute - mute a validator with a specific type</br>
Usage: /mute [cosmosvaladdr...] [absent|slashed|revoked]
</br>

/unmute - unmute a validator with a specific type</br>
Usage: /unmute [cosmosvaladdr...] [absent|slashed|revoked]
</br>

/hack - convert a cosmosvaladdr to hex</br>
Usage: /hack [cosmosvaladdr...]
</br>
