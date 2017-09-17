# LLDB-CommonCrypto
Some macOS programs use [CommonCrypto](https://opensource.apple.com/source/CommonCrypto/CommonCrypto-36064/CommonCrypto/CommonCryptor.h) to hide something.
Maybe it is useful to capture the argumetents passed to CCCryptorCreate.

## Requirement
- mac OS

## Development

1. `$ sudo easy_install pip`
2. `$ pip install --upgrade setuptools --user python pipenv`
3. Add `$HOME/Library/Python/2.7/bin` to $PATH
4. To activate this project's virtualenv, run the following: `pipenv shell`


## Future work

Capture more arguments of functions CommonCrypto has provided.
