# bot_monitor

### STATUS: STOP :no_entry:  (maintenance)

A Bot that monitor Gaia chain when something happened to a specific validator, and send alert through Telegram.
It sends alert every 15 seconds, if there is something happened during that time.

You can search this bot on Telegram by: @ForboleGaiaBot
</br>
Available commands:

`/start` - say hi !!!

`/help` - link to this github repository

`/subscribe` - subscribe a validator by its hexcosmosvaladdr</br>
Usage: `/subscribe [hexcosmosvaladdr...]`

`/unsubscribe` - unsubscribe a validator by its hexcosmosvaladdr</br>
Usage: `/unsubscribe [hexcosmosvaladdr...]`

`/mute` - mute a validator with a specific type</br>
Usage: `/mute [hexcosmosvaladdr...] [absent|slashed|revoked]`

`/unmute` - unmute a validator with a specific type</br>
Usage: `/unmute [hexcosmosvaladdr...] [absent|slashed|revoked]`

#### Deprecated
`/hack` - convert a cosmosvaladdr to hex</br>
Usage: `/hack [cosmosvaladdr...]`
