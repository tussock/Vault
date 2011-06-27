#!/bin/bash

find vault -name "*.py" -print | fgrep -v .svn > vault/i18n/sourcefiles
xgettext --language=Python --keyword=_ --from-code=UTF-8 -o vault/i18n/vault.pot -f vault/i18n/sourcefiles

for lang in en_US es; do
	mkdir -p vault/i18n/$lang/LC_MESSAGES
	msginit --no-translator --input=vault/i18n/vault.pot --locale=lang --output=vault/i18n/$lang/LC_MESSAGES/Vault.po
done
