# token_app
bot_service - shrouded-shore-63902.herokuapp.com\
user_service - thawing-harbor-07479.herokuapp.com\
ether_service - afternoon-sierra-39285.herokuapp.com

# ngrok (to bind telegram server with localhost 8002 (bot_service))
1. Download ngrok https://ngrok.com/download
2. Unpack to some new dir (not in project dir)
3. cd -> to dir with ngrok
4. Run ./ngrok http 8002
5. Copy row with url with https (example: https://2245-87-71-220-26.ngrok.io)
6. DO NOT CLOSE TERMINAL AND DO NOT EXIT (ctrl-c). It will kill the process.
7. Replace value for WEB_HOOK_URL in .env.dev (.env.test)
8. Run bot_service

# bot usage (test mode):
1. Install etherium wallet (for example MetaMask)
2. Press “Wallet” on the top of application and choose Ropsten Test Network
3. On main page Press import Tokens
4. In field Token Address paste 0x3E7061EF2Fb4cB3dd405E3Ea68F619CCd73a41e1
5. Press import

# bot commands:
AUTH commands:\
/signin - registration of wallet address (public key) in the bot\
/login - for login needs to set private key of wallet\
/logout - log out

ERC20 commands:\
https://eips.ethereum.org/EIPS/eip-20 \
/balance - Returns the account balance of address owner\
/transfer - Transfers  amount of tokens to address (recipient)\
/transfer_from - Transfers amount of tokens from address sender to address recipient\
/approve - Allows spender to withdraw from your account multiple times, up to the defined amount\
/allowance - Returns the amount which spender is still allowed to withdraw from recipient\

